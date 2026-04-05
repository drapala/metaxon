"""
Shared logic: DB connection, embed, hybrid search, ingest trigger.
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

# Hybrid search weights (must sum to 1.0)
W_VECTOR = 0.6
W_BM25 = 0.4
RRF_K = 60  # RRF constant — higher = less steep rank penalty


@lru_cache(maxsize=1)
def get_table():
    db = lancedb.connect(str(DB_PATH))
    t = db.open_table(TABLE_NAME)
    # Ensure FTS index exists (no-op if already created)
    try:
        t.create_fts_index("content", replace=False)
    except Exception:
        pass
    return t


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def _rrf_merge(
    vector_rows: list[dict],
    bm25_rows: list[dict],
    limit: int,
) -> list[dict]:
    """Reciprocal Rank Fusion over two ranked lists. Returns merged top-N."""
    scores: dict[str, float] = {}
    by_id: dict[str, dict] = {}

    for rank, row in enumerate(vector_rows):
        rid = row["id"]
        scores[rid] = scores.get(rid, 0) + W_VECTOR / (RRF_K + rank + 1)
        by_id[rid] = row

    for rank, row in enumerate(bm25_rows):
        rid = row["id"]
        scores[rid] = scores.get(rid, 0) + W_BM25 / (RRF_K + rank + 1)
        by_id.setdefault(rid, row)

    merged = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [
        {**by_id[rid], "score": round(rrf_score, 6)}
        for rid, rrf_score in merged[:limit]
    ]


def search(
    query: str,
    network: str | None = None,
    limit: int = 10,
    mode: str = "hybrid",  # "hybrid" | "vector" | "bm25"
) -> list[dict]:
    """
    Hybrid search (vector + BM25 via RRF).
    mode='vector' for pure semantic, mode='bm25' for keyword-only.
    """
    table = get_table()
    fetch = limit * 3  # over-fetch before merging

    def _where(q):
        return q.where(f"network = '{network}'") if network else q

    def _fmt(rows: list[dict], score_key: str = "_distance") -> list[dict]:
        return [
            {
                "id": r["id"],
                "title": r["title"],
                "source": r["source"],
                "network": r["network"],
                "created": r["created"],
                "score": float(r.get(score_key, 0)),
                "content": r["content"][:500],
            }
            for r in rows
        ]

    if mode == "vector":
        vector = embed(query)
        rows = _where(
            table.search(vector)
            .limit(limit)
            .select(
                ["id", "content", "title", "source", "network", "created", "_distance"]
            )
        ).to_list()
        return _fmt(rows)

    if mode == "bm25":
        rows = _where(
            table.search(query, query_type="fts")
            .limit(limit)
            .select(["id", "content", "title", "source", "network", "created"])
        ).to_list()
        return _fmt(rows, score_key="_score")

    # hybrid: RRF fusion
    vector = embed(query)
    vec_rows = _fmt(
        _where(
            table.search(vector)
            .limit(fetch)
            .select(
                ["id", "content", "title", "source", "network", "created", "_distance"]
            )
        ).to_list()
    )
    try:
        bm25_rows = _fmt(
            _where(
                table.search(query, query_type="fts")
                .limit(fetch)
                .select(["id", "content", "title", "source", "network", "created"])
            ).to_list(),
            score_key="_score",
        )
    except Exception:
        bm25_rows = []  # FTS unavailable, degrade gracefully

    return _rrf_merge(vec_rows, bm25_rows, limit)


def run_ingest(file: str | None = None) -> dict:
    """Re-run the ingest pipeline. Returns stdout summary."""
    script = ROOT / "scripts" / "single-brain" / "ingest.py"
    cmd = [sys.executable, str(script)]
    if file:
        # resolve to absolute so ingest.py's path.relative_to(ROOT) works
        cmd += ["--file", str((ROOT / file).resolve())]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    # Invalidate table cache so next search picks up new data
    get_table.cache_clear()

    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip() if result.returncode != 0 else None,
    }


def stats() -> dict:
    """Basic DB stats including chunk size distribution."""
    table = get_table()
    df = table.to_pandas()
    df["tokens"] = df["content"].str.split().str.len()
    return {
        "total_chunks": len(df),
        "by_network": df["network"].value_counts().to_dict(),
        "unique_articles": df["source"].nunique(),
        "chunk_tokens": {
            "mean": float(round(df["tokens"].mean(), 1)),
            "median": float(round(df["tokens"].median(), 1)),
            "min": int(df["tokens"].min()),
            "max": int(df["tokens"].max()),
            "pct_under_50": float(round((df["tokens"] < 50).mean() * 100, 1)),
            "heading_only": int(df["content"].str.match(r"^#{1,4} .{0,80}$").sum()),
        },
    }
