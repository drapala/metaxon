"""
Single Brain — FastAPI

Endpoints:
  GET  /health
  GET  /stats
  GET  /search?q=<query>[&network=observation|opinion][&limit=10][&mode=hybrid|vector|bm25]
  POST /ingest        body: {"file": "wiki/concepts/foo.md"}  (file optional)
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from api.core import run_ingest, search, stats

app = FastAPI(title="Single Brain KB", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def get_stats():
    return stats()


@app.get("/search")
def search_kb(
    q: str = Query(..., description="Query string"),
    network: str | None = Query(None, description="observation | opinion"),
    limit: int = Query(10, ge=1, le=50),
    mode: str = Query("hybrid", description="hybrid | vector | bm25"),
):
    if network and network not in ("observation", "opinion"):
        raise HTTPException(400, "network must be 'observation' or 'opinion'")
    if mode not in ("hybrid", "vector", "bm25"):
        raise HTTPException(400, "mode must be 'hybrid', 'vector', or 'bm25'")
    return search(q, network=network, limit=limit, mode=mode)


class IngestRequest(BaseModel):
    file: str | None = None


@app.post("/ingest")
def trigger_ingest(body: IngestRequest = IngestRequest()):
    result = run_ingest(file=body.file)
    if result["returncode"] != 0:
        raise HTTPException(500, detail=result["stderr"])
    return result
