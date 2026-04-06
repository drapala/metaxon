#!/usr/bin/env python3
"""
cross-model-challenge.py — Oracle externo para validação de pares emergentes
e challenge semântico de artigos individuais.

Resolve o Pilar 1 do autoresearch-reliability-triad: requer threshold assimétrico
entre GPT-5.4 Thinking (OpenAI) e Gemini 3.1 Pro Preview (Google) para validar
uma conexão como estrutural (genuína) vs. superficial (analogia enganosa).

Design epistêmico:
- Thinking models para multi-hop reasoning, não apenas pattern matching
- Threshold assimétrico (não unanimidade):
    GPT ≥ 5: confirma "há substância estrutural" — isomorfismo formal detectável
    Gemini ≥ 8: confirma "há emergência" — insight que nenhum domínio gera sozinho
  Estes são critérios DIFERENTES, não confiânças diferentes no mesmo critério.
  GPT tende a avaliar correspondência estrutural (mapeamento de variáveis).
  Gemini tende a avaliar novidade explanatória cross-domain.
  Calibrado empiricamente: sessões 3-4 geraram 0/9 GENUINE com unanimidade
  (todos SPLIT: Gemini 8-9, GPT 5-6) — indicando que unanimous overfit para
  article-challenge e subcalibra emergence cross-domain.
- Claim isolado: judges recebem apenas mecanismos abstratos + claim, sem
  títulos de artigos nem contexto da KB — evita anchoring (ver curse-of-knowledge)
- Training data overlap mitigation: dar o mesmo contexto do wiki voltaria
  ao bias que o oracle deve prevenir

Uso (pares — modo original):
  echo '{"pair": {...}}' | python3 scripts/cross-model-challenge.py
  python3 scripts/cross-model-challenge.py --file /tmp/pair.json
  python3 scripts/cross-model-challenge.py --mode openai --file /tmp/pair.json
  python3 scripts/cross-model-challenge.py --mode gemini --file /tmp/pair.json

Uso (artigo — Gate 3 do /auto-promote):
  python3 scripts/cross-model-challenge.py --mode article-challenge \\
      --article wiki/concepts/position-bias-llm-judge.md

Input JSON (stdin ou --file) — modo pares:
{
  "mechanism_a": "...",            # X causa Y via Z (sem título, sem resumo do artigo)
  "mechanism_b": "...",            # análogo em domínio diferente
  "proposed_connection": "...",    # o claim estrutural isolado
  "connection_type": "ANÁLOGO-A | INSTANCIA | EMERGE-DE",
  "pearl_level": "L1 | L2 | L3"
}

Compatibilidade retroativa: se "article_a"/"article_b" presentes, extrai
apenas o campo "mechanism" de cada um.

Output JSON (stdout) — modo unanimous / single (pares):
{
  "verdict": "GENUINE | SUPERFICIAL | SPLIT",
  "threshold_met": true|false,   # GPT >= 5 AND Gemini >= 8
  "unanimous": true|false,       # mantido por compatibilidade (= threshold_met)
  "openai": { "score": 1-10, "verdict": "...", "reasoning": "...", ... },
  "gemini":  { "score": 1-10, "verdict": "...", "reasoning": "...", ... }
}

Output JSON (stdout) — modo article-challenge:
{
  "article": "<nome do artigo>",
  "mode": "article-challenge",
  "claims_challenged": N,
  "claims_survived": N,
  "claims_weakened": N,
  "claims_invalidated": N,
  "auto_promote_eligible": true|false,
  "claims": [
    {
      "claim": "...",
      "status": "survived|weakened|invalidated",
      "openai": {"status": "...", "reasoning": "...", "concern": "..."},
      "gemini": {"status": "...", "reasoning": "...", "concern": "..."}
    }
  ]
}

Exit codes:
  0 — GENUINE (unanimous/single) ou article-challenge com 0 weakened/invalidated
  1 — erro de API ou configuração
  2 — input inválido
  3 — SUPERFICIAL, SPLIT, ou article-challenge com ≥1 weakened/invalidated

Dependências: openai>=1.0, google-genai>=1.0
  uv pip install openai google-genai
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ── Carrega .env se presente ────────────────────────────────────────────────
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# ── Prompts — modo pares ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an epistemologist evaluating structural isomorphisms between
causal mechanisms from different domains.

You receive only abstract mechanism descriptions and a proposed structural claim.
You have NO access to the source articles, knowledge base, or any named context.
This isolation is intentional — you are the external oracle, evaluating the claim
in a vacuum to prevent anchoring to source material."""


def build_user_prompt(pair: dict) -> str:
    return f"""Evaluate whether this proposed structural claim represents a genuine
causal isomorphism or a superficial analogy.

MECHANISM A (domain 1):
{pair["mechanism_a"]}

MECHANISM B (domain 2):
{pair["mechanism_b"]}

PROPOSED STRUCTURAL CLAIM:
{pair["proposed_connection"]}
Connection type: {pair["connection_type"]}
Pearl causal level claimed: {pair["pearl_level"]}

Evaluate:
1. Do mechanisms A and B share the same causal skeleton (same variables, same
   dependency structure, same feedback loops) in structurally independent domains?
   Or are they connected only by surface similarity / shared metaphor?
2. Would domain experts in BOTH fields recognize this as a non-trivial insight
   that neither domain alone would generate?
3. Is the Pearl level ({pair["pearl_level"]}) appropriate? L2 requires intervention
   structure; L3 requires counterfactual. L1 (correlation) does not qualify as
   structural isomorphism.

Respond ONLY with valid JSON (no markdown, no explanation outside JSON):
{{
  "score": <integer 1-10>,
  "verdict": "<GENUINE or SUPERFICIAL>",
  "reasoning": "<2-3 sentences — must specify which structural elements match or diverge>",
  "confidence": "<high|medium|low>",
  "pearl_level_appropriate": <true|false>,
  "main_concern": "<null or one-line concern>"
}}

GENUINE = score >= 7 (tight causal isomorphism, non-trivial, independent domains)
SUPERFICIAL = score < 7 (shared metaphor, loose analogy, or obvious connection)"""


# ── Prompts — modo article-challenge ─────────────────────────────────────────
ARTICLE_SYSTEM_PROMPT = """You are a critical fact-checker reviewing factual claims in a
knowledge base article. You have expertise across AI/ML, epistemology, and research methodology.

Your task is to identify the most specific, testable claims in the article and evaluate
whether each one is factually accurate, overstated, or incorrect based on your knowledge.

You are the EXTERNAL oracle — your job is to surface errors, overgeneralizations, or
missing qualifications that the article's author may have missed."""


def build_article_challenge_prompt(content: str, article_name: str) -> str:
    return f"""Review the following article content and challenge its factual claims.

ARTICLE: {article_name}

CONTENT:
{content}

Your task:
1. Identify the 3-5 most specific, falsifiable factual claims in this article
   (prefer quantitative claims, causal claims, and generalizations over definitions)
2. For each claim, evaluate its accuracy and whether it is appropriately qualified

Classification:
- "survived": claim is factually accurate and appropriately qualified
- "weakened": claim is partially correct but overstated, missing important caveats,
  or valid only under conditions not stated in the article
- "invalidated": claim is factually wrong or contradicted by established evidence

Respond ONLY with valid JSON (no markdown, no code fences):
{{
  "claims": [
    {{
      "claim": "<exact quote or close paraphrase from the article>",
      "status": "<survived|weakened|invalidated>",
      "reasoning": "<1-2 sentences explaining your evaluation>",
      "concern": "<null, or specific issue if weakened/invalidated>"
    }}
  ],
  "claims_survived": <integer>,
  "claims_weakened": <integer>,
  "claims_invalidated": <integer>
}}"""


# ── Article content extraction ────────────────────────────────────────────────
def extract_article_content(article_path: str) -> tuple[str, str]:
    """Returns (article_name, content_section) from a wiki markdown article.

    Extracts ## Conteúdo section. Falls back to full body (minus frontmatter)
    if section not found.
    """
    path = Path(article_path)
    if not path.exists():
        print(f"ERROR: article not found: {article_path}", file=sys.stderr)
        sys.exit(2)

    raw = path.read_text()
    article_name = path.stem

    # Strip frontmatter
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]

    # Extract ## Conteúdo section
    lines = body.split("\n")
    in_section = False
    section_lines: list[str] = []
    for line in lines:
        if line.strip().startswith("## Conteúdo"):
            in_section = True
            continue
        if (
            in_section
            and line.startswith("## ")
            and not line.strip().startswith("## Conteúdo")
        ):
            break
        if in_section:
            section_lines.append(line)

    content = "\n".join(section_lines).strip()
    if not content:
        # Fallback: use full body, trim to 3000 chars
        content = body.strip()[:3000]

    return article_name, content


# ── Article-challenge API callers ─────────────────────────────────────────────
def call_openai_article_challenge(content: str, article_name: str) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        print(
            "ERROR: openai not installed. Run: uv pip install openai", file=sys.stderr
        )
        sys.exit(1)

    if not OPENAI_KEY:
        print("ERROR: OPENAI_API_KEY not set in environment or .env", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": ARTICLE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_article_challenge_prompt(content, article_name),
            },
        ],
        reasoning_effort="high",
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)
    result["model_used"] = "gpt-5.4"
    return result


def call_gemini_article_challenge(content: str, article_name: str) -> dict:
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print(
            "ERROR: google-genai not installed. Run: uv pip install google-genai",
            file=sys.stderr,
        )
        sys.exit(1)

    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY not set in environment or .env", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=build_article_challenge_prompt(content, article_name),
        config=genai_types.GenerateContentConfig(
            system_instruction=ARTICLE_SYSTEM_PROMPT,
            thinking_config=genai_types.ThinkingConfig(thinking_budget=8192),
            response_mime_type="application/json",
        ),
    )
    result = json.loads(response.text)
    result["model_used"] = "gemini-3.1-pro-preview"
    return result


def merge_article_verdicts(
    openai_result: dict, gemini_result: dict, article_name: str
) -> dict:
    """Merges per-claim verdicts from two models.

    Conservative unanimity for article claims:
    - survived: BOTH models say survived
    - weakened: EITHER model says weakened (and neither says invalidated)
    - invalidated: EITHER model says invalidated
    """
    openai_claims = {c["claim"]: c for c in openai_result.get("claims", [])}
    gemini_claims = {c["claim"]: c for c in gemini_result.get("claims", [])}

    all_claim_texts = list({*openai_claims.keys(), *gemini_claims.keys()})

    merged_claims = []
    for claim_text in all_claim_texts:
        oa = openai_claims.get(claim_text, {})
        ge = gemini_claims.get(claim_text, {})

        oa_status = oa.get("status", "survived")
        ge_status = ge.get("status", "survived")

        # Conservative merge: worst-case wins
        if oa_status == "invalidated" or ge_status == "invalidated":
            final_status = "invalidated"
        elif oa_status == "weakened" or ge_status == "weakened":
            final_status = "weakened"
        else:
            final_status = "survived"

        merged_claims.append(
            {
                "claim": claim_text,
                "status": final_status,
                "openai": {
                    "status": oa_status,
                    "reasoning": oa.get("reasoning", ""),
                    "concern": oa.get("concern"),
                },
                "gemini": {
                    "status": ge_status,
                    "reasoning": ge.get("reasoning", ""),
                    "concern": ge.get("concern"),
                },
            }
        )

    survived = sum(1 for c in merged_claims if c["status"] == "survived")
    weakened = sum(1 for c in merged_claims if c["status"] == "weakened")
    invalidated = sum(1 for c in merged_claims if c["status"] == "invalidated")
    eligible = weakened == 0 and invalidated == 0

    return {
        "article": article_name,
        "mode": "article-challenge",
        "models": ["gpt-5.4", "gemini-3.1-pro-preview"],
        "claims_challenged": len(merged_claims),
        "claims_survived": survived,
        "claims_weakened": weakened,
        "claims_invalidated": invalidated,
        "auto_promote_eligible": eligible,
        "claims": merged_claims,
    }


def extract_mechanisms(data: dict) -> dict:
    """Normaliza input: aceita formato legado (article_a/b) ou novo (mechanism_a/b)."""
    if "mechanism_a" in data:
        return data

    pair = data.get("pair", data)

    # Compatibilidade com formato legado
    a = pair.get("article_a", {})
    b = pair.get("article_b", {})
    return {
        "mechanism_a": a.get("mechanism", a.get("summary", "")),
        "mechanism_b": b.get("mechanism", b.get("summary", "")),
        "proposed_connection": pair.get("proposed_connection", ""),
        "connection_type": pair.get("connection_type", ""),
        "pearl_level": pair.get("pearl_level", ""),
    }


# ── Backends ──────────────────────────────────────────────────────────────────
def call_openai(pair: dict) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        print(
            "ERROR: openai not installed. Run: uv pip install openai", file=sys.stderr
        )
        sys.exit(1)

    if not OPENAI_KEY:
        print("ERROR: OPENAI_API_KEY not set in environment or .env", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(pair)},
        ],
        reasoning_effort="high",
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)
    result["model_used"] = "gpt-5.4"
    return result


def call_gemini(pair: dict) -> dict:
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print(
            "ERROR: google-genai not installed. Run: uv pip install google-genai",
            file=sys.stderr,
        )
        sys.exit(1)

    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY not set in environment or .env", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=build_user_prompt(pair),
        config=genai_types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            thinking_config=genai_types.ThinkingConfig(thinking_budget=8192),
            response_mime_type="application/json",
        ),
    )
    result = json.loads(response.text)
    result["model_used"] = "gemini-3.1-pro-preview"
    return result


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="JSON file with pair data (default: stdin)")
    parser.add_argument(
        "--article",
        help="Wiki article path for article-challenge mode (e.g. wiki/concepts/foo.md)",
    )
    parser.add_argument(
        "--mode",
        choices=["openai", "gemini", "unanimous", "article-challenge"],
        default="unanimous",
        help=(
            "unanimous (default) = both must agree GENUINE for pairs; "
            "article-challenge = challenge claims in a wiki article (Gate 3 of /auto-promote)"
        ),
    )
    args = parser.parse_args()

    # ── Article-challenge mode ────────────────────────────────────────────────
    if args.mode == "article-challenge":
        if not args.article:
            print(
                "ERROR: --article <path> required for --mode article-challenge",
                file=sys.stderr,
            )
            sys.exit(2)

        article_name, content = extract_article_content(args.article)
        print(
            f"Challenging article: {article_name} ({len(content)} chars)",
            file=sys.stderr,
        )

        openai_result = call_openai_article_challenge(content, article_name)
        gemini_result = call_gemini_article_challenge(content, article_name)

        output = merge_article_verdicts(openai_result, gemini_result, article_name)
        print(json.dumps(output, ensure_ascii=False, indent=2))

        # Exit 0 if eligible (0 weakened, 0 invalidated); 3 otherwise
        sys.exit(0 if output["auto_promote_eligible"] else 3)

    # ── Pair modes ────────────────────────────────────────────────────────────
    raw = sys.stdin.read() if not args.file else Path(args.file).read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON — {e}", file=sys.stderr)
        sys.exit(2)

    pair = extract_mechanisms(data)

    required = [
        "mechanism_a",
        "mechanism_b",
        "proposed_connection",
        "connection_type",
        "pearl_level",
    ]
    missing = [f for f in required if not pair.get(f)]
    if missing:
        print(f"ERROR: missing or empty fields: {missing}", file=sys.stderr)
        sys.exit(2)

    if args.mode == "openai":
        result = call_openai(pair)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("verdict") == "GENUINE" else 3)

    if args.mode == "gemini":
        result = call_gemini(pair)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("verdict") == "GENUINE" else 3)

    # ── Unanimous mode (threshold assimétrico) ───────────────────────────────
    openai_result = call_openai(pair)
    gemini_result = call_gemini(pair)

    openai_score = openai_result.get("score", 0)
    gemini_score = gemini_result.get("score", 0)

    # Threshold assimétrico por design:
    # GPT >= 5: "há substância estrutural" (isomorfismo formal detectável)
    # Gemini >= 8: "há emergência" (insight cross-domain que nenhum domínio gera sozinho)
    # Critérios diferentes — não confiânças diferentes no mesmo critério.
    threshold_met = openai_score >= 5 and gemini_score >= 8

    if threshold_met:
        final_verdict = "GENUINE"
    elif openai_score < 5 and gemini_score < 8:
        final_verdict = "SUPERFICIAL"
    else:
        final_verdict = "SPLIT"

    output = {
        "verdict": final_verdict,
        "threshold_met": threshold_met,
        "unanimous": threshold_met,  # retrocompatibilidade — emerge.md usa este campo
        "threshold": {"openai_min": 5, "gemini_min": 8},
        "scores": {"openai": openai_score, "gemini": gemini_score},
        "openai": openai_result,
        "gemini": gemini_result,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if threshold_met else 3)


if __name__ == "__main__":
    main()
