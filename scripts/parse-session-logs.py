#!/usr/bin/env python3
"""
parse-session-logs.py — Fallback parser for Claude Code session JSONL.

Reads ~/.claude/projects/-Users-drapala-projects-llm-kb/*.jsonl (most recent),
groups by Skill tool_use blocks, reconstructs per-skill token deltas,
and appends to outputs/reports/skill-usage.jsonl (same schema as track-skill-usage.py).

Records are tagged "source": "parsed" to distinguish from hook-sourced records.

Usage:
  python3 scripts/parse-session-logs.py [--session PATH] [--date YYYY-MM-DD]
"""

import json
import sys
import datetime
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PRICING_PATH = PROJECT_ROOT / "config" / "pricing.yaml"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "reports" / "skill-usage.jsonl"
SESSIONS_DIR = Path.home() / ".claude" / "projects" / "-Users-drapala-projects-llm-kb"
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


def load_existing_hook_skills(date_str: str) -> set:
    """Return set of (session_id, skill, ts_prefix) already captured by hook."""
    seen = set()
    if not OUTPUT_PATH.exists():
        return seen
    with open(OUTPUT_PATH) as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get("source") == "hook" and r.get("ts", "").startswith(date_str):
                    seen.add((r.get("session_id", ""), r.get("skill", "")))
            except Exception:
                pass
    return seen


def parse_session(path: Path, pricing: dict, target_date: str) -> list[dict]:
    """Parse a session JSONL and extract Skill invocations with token deltas."""
    records = []

    entries = []
    with open(path) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except Exception:
                pass

    if not entries:
        return records

    # Extract session_id from first entry
    session_id = ""
    for e in entries:
        if "sessionId" in e:
            session_id = e["sessionId"]
            break
        if "session_id" in e:
            session_id = e["session_id"]
            break

    # Walk entries to find Skill tool_use blocks and their surrounding usage
    # Strategy: for each Skill tool_use, take the usage from the next assistant
    # message after the tool_result — that's the accumulated cost up to that point.
    # Use delta between the usage before the Skill call and after.

    skill_invocations = []  # list of (index, skill_name, args, tool_use_id)

    for i, entry in enumerate(entries):
        msg = entry.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if (
                isinstance(block, dict)
                and block.get("type") == "tool_use"
                and block.get("name") == "Skill"
            ):
                inp = block.get("input", {})
                skill_name = inp.get("skill", "")
                args = inp.get("args", "")
                tool_use_id = block.get("id", "")
                if skill_name:
                    skill_invocations.append(
                        {
                            "entry_idx": i,
                            "skill": skill_name,
                            "args": args,
                            "tool_use_id": tool_use_id,
                        }
                    )

    if not skill_invocations:
        return records

    # For each skill invocation, find usage snapshot before and after
    def get_usage_at(idx: int) -> dict | None:
        """Get most recent usage dict at or before entry idx."""
        for j in range(idx, -1, -1):
            u = entries[j].get("message", {}).get("usage", {})
            if u:
                return u
        return None

    def get_usage_after(idx: int) -> dict | None:
        """Get first usage dict strictly after entry idx (post tool_result)."""
        # Find the tool_result for this skill, then get next assistant usage
        for j in range(idx + 1, len(entries)):
            u = entries[j].get("message", {}).get("usage", {})
            if u:
                return u
        return None

    def usage_delta(before: dict | None, after: dict | None) -> dict:
        if not before or not after:
            return {}
        keys = [
            "input_tokens",
            "output_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
        ]
        return {k: max(0, after.get(k, 0) - before.get(k, 0)) for k in keys}

    existing = load_existing_hook_skills(target_date)

    for inv in skill_invocations:
        skill = inv["skill"]
        idx = inv["entry_idx"]

        # Skip if already captured by hook
        if (session_id, skill) in existing:
            continue

        before_usage = get_usage_at(idx - 1) if idx > 0 else None
        after_usage = get_usage_after(idx)
        delta = usage_delta(before_usage, after_usage)

        model = DEFAULT_MODEL
        cost = calc_cost(delta, model, pricing)

        # Approximate timestamp from entry
        ts_raw = entries[idx].get("timestamp", "")
        if ts_raw:
            ts = ts_raw if ts_raw.endswith("Z") else ts_raw + "Z"
        else:
            ts = datetime.datetime.utcnow().isoformat() + "Z"

        # Only include records from target date
        if target_date and not ts.startswith(target_date):
            continue

        record = {
            "ts": ts,
            "session_id": session_id,
            "command": skill,
            "skill": skill,
            "model": model,
            "input_tokens": delta.get("input_tokens", 0),
            "output_tokens": delta.get("output_tokens", 0),
            "cache_read_input_tokens": delta.get("cache_read_input_tokens", 0),
            "cache_creation_input_tokens": delta.get("cache_creation_input_tokens", 0),
            "duration_ms": 0,
            "status": "success",
            "cost_usd": cost,
            "outcome": None,
            "oracle": None,
            "source": "parsed",
        }
        records.append(record)

    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--session", help="Path to session JSONL (default: most recent)"
    )
    parser.add_argument(
        "--date",
        default=datetime.date.today().isoformat(),
        help="Filter by date YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args()

    if args.session:
        session_path = Path(args.session)
    else:
        candidates = sorted(
            SESSIONS_DIR.glob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True
        )
        if not candidates:
            print("No session JSONL found.", file=sys.stderr)
            sys.exit(1)
        session_path = candidates[0]

    pricing = load_pricing()
    records = parse_session(session_path, pricing, args.date)

    if not records:
        print(f"No new Skill invocations found for {args.date}.")
        sys.exit(0)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "a") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"Appended {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
