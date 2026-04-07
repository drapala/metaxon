#!/usr/bin/env python3
"""
track-skill-usage.py — PostToolUse hook for Skill tool invocations.

Reads hook JSON from stdin, appends one record to outputs/reports/skill-usage.jsonl.
Usage tokens are 0 at hook time — parse-session-logs.py reconciles them later.

Hook context (stdin JSON):
  {
    "hook_event": "PostToolUse",
    "tool_name": "Skill",
    "tool_input": {"skill": "challenge", "args": "..."},
    "tool_response": "...",
    "session_id": "...",
    "usage": {...}    # may or may not be present
  }
"""

import json
import sys
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PRICING_PATH = PROJECT_ROOT / "config" / "pricing.yaml"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "reports" / "skill-usage.jsonl"

DEFAULT_MODEL = "claude-sonnet-4-6"


def load_pricing():
    try:
        import yaml

        with open(PRICING_PATH) as f:
            return yaml.safe_load(f)["models"]
    except Exception:
        return {}


def calc_cost(usage: dict, model: str, pricing: dict) -> float:
    p = pricing.get(model, pricing.get(DEFAULT_MODEL, {}))
    if not p:
        return 0.0
    input_cost = usage.get("input_tokens", 0) / 1_000_000 * p.get("input_per_1m", 0)
    output_cost = usage.get("output_tokens", 0) / 1_000_000 * p.get("output_per_1m", 0)
    cache_read = (
        usage.get("cache_read_input_tokens", 0)
        / 1_000_000
        * p.get("cache_read_per_1m", 0)
    )
    cache_create = (
        usage.get("cache_creation_input_tokens", 0)
        / 1_000_000
        * p.get("cache_creation_per_1m", 0)
    )
    return round(input_cost + output_cost + cache_read + cache_create, 6)


def calc_oracle_cost(pricing: dict) -> dict | None:
    """Check if a gate3 output exists from today's session and extract oracle costs."""
    gates_dir = PROJECT_ROOT / "outputs" / "gates"
    if not gates_dir.exists():
        return None

    today = datetime.date.today().isoformat()
    # Find any gate3 file modified today
    for gate_file in sorted(
        gates_dir.glob("gate3-*.yaml"), key=lambda f: f.stat().st_mtime, reverse=True
    ):
        if datetime.date.fromtimestamp(gate_file.stat().st_mtime).isoformat() == today:
            try:
                import yaml

                data = yaml.safe_load(gate_file.read_text())
                models_used = []
                total_oracle_cost = 0.0
                verdicts = []

                for model_key in ["gpt-4o", "gemini-2.0-flash"]:
                    if model_key in data:
                        models_used.append(model_key)
                        model_data = data[model_key]
                        # Try to read usage if present
                        model_usage = model_data.get("usage", {})
                        total_oracle_cost += calc_cost(model_usage, model_key, pricing)
                        verdict = model_data.get("verdict", "")
                        if verdict:
                            verdicts.append(verdict)

                if not models_used:
                    return None

                agreement = len(set(verdicts)) == 1 if verdicts else False
                overall = (
                    verdicts[0]
                    if agreement and verdicts
                    else ("SPLIT" if len(set(verdicts)) > 1 else None)
                )

                return {
                    "models": models_used,
                    "cost_usd": round(total_oracle_cost, 6),
                    "verdict": overall,
                    "agreement": agreement,
                }
            except Exception:
                return None
    return None


def main():
    try:
        raw = sys.stdin.read()
        ctx = json.loads(raw) if raw.strip() else {}
    except Exception:
        ctx = {}

    tool_input = ctx.get("tool_input", {})
    skill = tool_input.get("skill", "")
    if not skill:
        sys.exit(0)

    usage = ctx.get("usage", {})
    model = tool_input.get("model", DEFAULT_MODEL) or DEFAULT_MODEL
    session_id = ctx.get("session_id", "")
    command = skill  # skill name is the command

    pricing = load_pricing()
    cost_usd = calc_cost(usage, model, pricing)

    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "session_id": session_id,
        "command": command,
        "skill": skill,
        "model": model,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
        "duration_ms": ctx.get("duration_ms", 0),
        "status": ctx.get("status", "success"),
        "cost_usd": cost_usd,
        "outcome": None,
        "oracle": None,
        "source": "hook",
    }

    # Enrich oracle data for challenge commands
    if skill in ("challenge", "challenge-external", "auto-promote"):
        record["oracle"] = calc_oracle_cost(pricing)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
