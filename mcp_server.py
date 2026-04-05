#!/usr/bin/env python3
"""
Single Brain — MCP Server (stdio)

Tools exposed to agents:
  kb_search  — semantic search over the KB
  kb_ingest  — re-ingest wiki articles into the vector DB
  kb_stats   — current DB stats

To register in Claude Code (~/.claude/settings.json):
  "mcpServers": {
    "llm-kb": {
      "command": "/Users/drapala/projects/llm-kb/.venv/bin/python",
      "args": ["/Users/drapala/projects/llm-kb/mcp_server.py"],
      "cwd": "/Users/drapala/projects/llm-kb"
    }
  }
"""

import sys
from pathlib import Path

# Ensure project root is on path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP

from api.core import run_ingest, search, stats

mcp = FastMCP("llm-kb")


@mcp.tool()
def kb_search(
    query: str,
    network: str = "",
    limit: int = 10,
) -> list[dict]:
    """
    Semantic search over the LLM knowledge base.

    Args:
        query: Natural language query
        network: Filter by namespace — "observation" (promoted wiki) or "opinion" (quarantined/emergent). Empty = search all.
        limit: Max results (1-50, default 10)
    """
    return search(query, network=network or None, limit=min(limit, 50))


@mcp.tool()
def kb_ingest(file: str = "") -> dict:
    """
    Re-ingest wiki articles into the vector DB.

    Args:
        file: Relative path to a specific article (e.g. "wiki/concepts/foo.md").
              If empty, re-ingests all articles.
    """
    return run_ingest(file=file or None)


@mcp.tool()
def kb_stats() -> dict:
    """Return current stats: total chunks, breakdown by network, unique articles."""
    return stats()


if __name__ == "__main__":
    mcp.run()
