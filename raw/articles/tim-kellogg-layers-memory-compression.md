---
source: https://timkellogg.me/blog/2025/06/15/compression
author: Tim Kellogg
date: 2025-06-15
type: article
---

# Layers of Memory, Layers of Compression

## Core Thesis

All approaches to agent memory — layered hierarchies, multi-agent distribution, intentional compression — are fundamentally solving the same rate-distortion problem: maximize useful signal within fixed context windows while minimizing information loss.

## Letta's Layered Memory (4 Blocks)

Conceptually similar to CPU cache levels:

| Block | Analogy | Capacity | Fidelity |
|-------|---------|----------|----------|
| **Core Memory** | L1 cache | Minimal tokens | Zero distortion on critical facts |
| **Message Buffer** | L2 cache | Fixed rolling window | Older context suffers distortion |
| **Archival Memory** | Disk | Practically unbounded | High distortion via embedding/summary |
| **Recall Memory** | DMA | On-demand retrieval | Rehydrates archived knowledge |

System works through continuous assembly: each turn combines core knowledge + message buffer + retrieved snippets. Full buffers trigger archival of oldest interactions.

### Rate-Distortion Framework

With fixed context windows, maximizing fidelity requires balancing:
- **Rate** (token inclusion)
- **Distortion** (detail loss)

Compression becomes cognitive work: summarizing before archival forces understanding; searching archives requires reasoning about importance.

## Single-Agent vs. Multi-Agent Compression

### Single-Agent (Letta / Cognition approach)
One cognitive entity manages compressed memories across time through structured hierarchy. Cognition recommends a dedicated model that condenses conversation history into key details and decisions, persisting as backbone context. Maintains one coherent reasoning thread.

### Multi-Agent (Anthropic approach)
Parallel subagents each compress different problem aspects independently. Lead agent coordinates and integrates condensed findings. Separation of concerns reduces path-dependence.

Testing confirmed multi-agent approaches outperformed single-agent on broad queries requiring extensive source exploration.

### The Coordination Challenge (Cognition's critique)
Current multi-agent implementations produce fragile systems because context cannot be adequately shared. Each subagent interprets tasks with only partial information. As Walden Yan explains: decision-making becomes "too dispersed" and "context isn't able to be shared thoroughly enough."

## Conclusion: Compression is Cognition

Intelligence faces information bottlenecks. Whether through layered memory hierarchies, multi-agent task distribution, or intentional compression, effective systems must aggressively filter and abstract information while remaining capable of recovering relevant details.

Extending AI cognition requires engineering intentional forgetting. Memory becomes meaningful precisely because it isn't perfect recording — it's prioritized, lossy, and alive.
