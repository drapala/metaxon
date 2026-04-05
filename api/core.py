"""
Shared logic: DB connection, embed, search, ingest trigger.
Imported by both FastAPI (api/main.py) and MCP server (mcp_server.py).
"""

from __future__ import annotations

import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import lancedb
import ollama

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "outputs" / "single-brain" / "db"
EMBED_MODEL = "nomic-embed-text"
TABLE_NAME = "fragments"


@lru_cache(maxsize=1)
def get_table():
    db = lancedb.connect(str(DB_PATH))
    return db.open_table(TABLE_NAME)


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def search(
    query: str,
    network: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Vector search. Returns list of dicts with content, title, source, network, score."""
    table = get_table()
    vector = embed(query)

    results = (
        table.search(vector)
        .limit(limit)
        .select(["id", "content", "title", "source", "network", "created", "_distance"])
    )

    if network:
        results = results.where(f"network = '{network}'")

    rows = results.to_list()

    return [
        {
            "id": r["id"],
            "title": r["title"],
            "source": r["source"],
            "network": r["network"],
            "created": r["created"],
            "score": float(r.get("_distance", 0)),
            "content": r["content"][:500],  # truncate for API responses
        }
        for r in rows
    ]


def run_ingest(file: str | None = None) -> dict:
    """Re-run the ingest pipeline. Returns stdout summary."""
    script = ROOT / "scripts" / "single-brain" / "ingest.py"
    cmd = [sys.executable, str(script)]
    if file:
        cmd += ["--file", file]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip() if result.returncode != 0 else None,
    }


def stats() -> dict:
    """Basic DB stats."""
    table = get_table()
    df = table.to_pandas()
    return {
        "total_chunks": len(df),
        "by_network": df["network"].value_counts().to_dict(),
        "unique_articles": df["source"].nunique(),
    }
