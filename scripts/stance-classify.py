#!/usr/bin/env python3
"""
stance-classify.py — LLM-based stance classification for /ingest pipeline.

Assigns confirming | challenging | neutral to a raw source using Claude Haiku.
Stance is relative to the KB's core claims (as described in the prompt context).

Usage:
    python3 scripts/stance-classify.py --source <path-to-raw-file> [--debug]

Exit codes:
    0 — classification successful (outputs YAML-formatted result)
    1 — API error or unclassifiable (treat as neutral, review manually)
    2 — usage error

Cost: ~$0.001 per paper (Haiku, 500-token input, 50-token output)
Model: claude-haiku-4-5-20251001
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Load .env from project root automatically
_ENV = Path(__file__).parent.parent / ".env"
if _ENV.exists():
    for _line in _ENV.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

MODEL = "claude-haiku-4-5-20251001"
MAX_SOURCE_CHARS = 2000  # abstract + intro, enough for stance signal

# What this KB is about — used as context for the LLM judge
KB_CORE_CLAIMS = """
This knowledge base (KB) is about AI/ML systems, specifically:
1. LLM-based knowledge bases and agents that self-improve
2. Retrieval-Augmented Generation (RAG), hybrid search, memory architectures
3. LLMs-as-judges: evaluation bias, self-enhancement, position bias
4. Autonomous research pipelines: failure modes, safeguards, epistemic integrity
5. Scientific research programmes (Lakatos), groupthink, heuristics and biases
6. Cross-domain analogies: procurement/corruption dynamics, stigmergic coordination,
   viable systems, rational inattention — used as conceptual lenses for AI design

Stance definitions relative to KB claims:
- confirming: paper supports, validates, extends, or replicates a claim already in the KB
- challenging: paper refutes, contradicts, shows limitations of, or presents evidence
  against a claim in the KB
- neutral: paper introduces a new topic unrelated to existing KB claims, or is from a
  domain too distant to have a directional stance (e.g. pure economics, pure biology)

For Zone 3 domains (law, public administration, biology, pure physics): neutral by default
unless the paper explicitly challenges an AI/ML claim.
"""

SYSTEM_PROMPT = f"""You are a stance classifier for an academic knowledge base.

{KB_CORE_CLAIMS}

## Precise definitions

**confirming**: The paper presents NEW empirical evidence or replicated experiments that DIRECTLY SUPPORT a specific claim already in the KB. The paper must add evidence, not just be on the same topic.
Example: "A new study measures LLM self-preference bias at 73% on a different dataset" — confirms the KB's claim that self-enhancement bias exists.

**challenging**: The paper presents evidence that CONTRADICTS, LIMITS, or REFUTES a claim in the KB. The paper argues the KB's position is wrong, incomplete, or overstated.
Example: "Self-preference bias is an artifact of prompt format, not intrinsic to LLMs" — challenges KB claims about self-enhancement.

**neutral**: The paper introduces a new concept WITHOUT taking a position on existing KB claims. This includes:
- Surveys and reviews (they describe, don't take a stance)
- Zone 3 domain papers (economics, psychology, philosophy, biology used as lenses)
- Papers on new topics not yet in the KB
- Papers that present a method without validating/contradicting KB claims
Example: Kahneman & Tversky on heuristics — neutral because KB uses it as a lens, the paper itself doesn't argue about LLM judges.
Example: Reflexion RL paper — neutral because it presents a method, doesn't argue for/against KB claims.

## Key rule
Being about the same topic ≠ confirming. A paper must PROVIDE EVIDENCE FOR or AGAINST a specific KB claim.
Default to neutral when unsure.

Respond ONLY with a JSON object, no other text:
{{"stance": "confirming|challenging|neutral", "confidence": 0.0-1.0, "reason": "one sentence citing which KB claim is confirmed/challenged, or why neutral"}}"""


def extract_head(path: Path) -> str:
    """Extract first MAX_SOURCE_CHARS of text from file."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return result.stdout[:MAX_SOURCE_CHARS]
        except Exception:
            pass
        return ""
    try:
        return path.read_text(errors="replace")[:MAX_SOURCE_CHARS]
    except Exception:
        return ""


def fetch_kb_context(source_text: str, debug: bool = False) -> str:
    """
    Query the KB vector search to find relevant wiki claims for this source.
    Imports api/core.py search() directly — no HTTP server required.
    Falls back to empty string if KB is unavailable.
    """
    try:
        import sys as _sys

        _root = Path(__file__).parent.parent
        if str(_root) not in _sys.path:
            _sys.path.insert(0, str(_root))
        from api.core import search  # noqa: PLC0415

        lines = [ln.strip() for ln in source_text.splitlines() if ln.strip()]
        title = next((ln.lstrip("#").strip() for ln in lines if ln.startswith("#")), "")
        summary = " ".join(lines[1:5])[:250]
        query = f"{title} {summary}".strip()[:350]

        results = search(query, limit=3)
        snippets = [
            f"- [{r.get('title', '')}]: {r.get('content', '')[:220]}"
            for r in results[:3]
        ]
        ctx = "\n".join(snippets)
        if debug and ctx:
            print(f"# KB context ({len(results)} hits):\n{ctx[:400]}", file=sys.stderr)
        return ctx
    except Exception as e:
        if debug:
            print(f"# KB context unavailable: {e}", file=sys.stderr)
        return ""


def classify_with_llm(text: str, kb_context: str = "", debug: bool = False) -> dict:
    """Call Claude Haiku to classify stance. Returns dict with stance/confidence/reason."""
    try:
        import anthropic
    except ImportError:
        return {
            "stance": "neutral",
            "confidence": 0.3,
            "reason": "anthropic not installed",
            "needs_human_review": True,
        }

    client = anthropic.Anthropic()

    user_content = f"Source text (first {MAX_SOURCE_CHARS} chars):\n\n{text}"
    if kb_context:
        user_content += f"\n\n## Relevant KB claims (from wiki):\n{kb_context}\n\nUse these to determine if the source confirms or challenges specific KB claims."

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
        )
        raw = response.content[0].text.strip()
        if debug:
            print(f"# LLM raw: {raw}", file=sys.stderr)

        # Strip markdown code fences if present
        import json
        import re as _re

        clean = _re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=_re.DOTALL).strip()
        parsed = json.loads(clean)
        stance = parsed.get("stance", "neutral")
        confidence = float(parsed.get("confidence", 0.5))
        reason = parsed.get("reason", "")

        # Validate stance value
        if stance not in ("confirming", "challenging", "neutral"):
            stance = "neutral"
            confidence = 0.4

        return {
            "stance": stance,
            "confidence": confidence,
            "reason": reason,
            "needs_human_review": confidence < 0.7,
        }

    except Exception as e:
        if debug:
            print(f"# LLM error: {e}", file=sys.stderr)
        return {
            "stance": "neutral",
            "confidence": 0.3,
            "reason": f"api_error: {type(e).__name__}",
            "needs_human_review": True,
        }


def main():
    parser = argparse.ArgumentParser(description="LLM-based stance classification")
    parser.add_argument("--source", required=True, help="Path to raw source file")
    parser.add_argument("--debug", action="store_true", help="Show LLM raw output")
    args = parser.parse_args()

    path = Path(args.source)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(2)

    text = extract_head(path)
    if not text.strip():
        print("stance: neutral")
        print("confidence: 0.30")
        print("reason: empty_or_unreadable")
        print("needs_human_review: true")
        sys.exit(0)

    kb_context = fetch_kb_context(text, debug=args.debug)
    result = classify_with_llm(text, kb_context=kb_context, debug=args.debug)

    print(f"stance: {result['stance']}")
    print(f"confidence: {result['confidence']:.2f}")
    print(f"reason: {result['reason']}")
    print(f"needs_human_review: {'true' if result['needs_human_review'] else 'false'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
