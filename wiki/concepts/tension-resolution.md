---
title: "Tension Resolution"
sources:
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/calm-llm-judge-biases.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/carmo-context-aware-reward-modelling.md
    type: paper
    quality: primary
  - path: raw/papers/synapse-episodic-semantic-memory.md
    type: paper
    quality: primary
  - path: raw/papers/knowledge-conflicts-llms-survey.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [meta-kb, quality, contradictions, design]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Tension resolution is the process of detecting and contextualizing contradictions between wiki articles. Five mechanisms from ingested papers inform the design: Reflexion (grounded verification required), CALM (self-enhancement bias makes self-judgment unreliable), ERL (resolutions should become reusable heuristics), CARMO (dynamic criteria beat static rubrics), Synapse (graph topology discovers non-obvious conflicts). Key principle: real tensions should be documented with conditional resolution, not forcefully harmonized.

## Conteúdo

### Why Not a Standalone /tensions Command

A /tensions command is the same pipeline as /review with "contradiction" instead of "overlap." Creating it before proving /review works violates blueprint principle 1 ("prove the loop before building the system"). Tension detection belongs in /review passada 1; resolution belongs in passada 2.

### The 5 Mechanisms

**1. Reflexion → Grounded Verification Required**

Self-reflection without grounded feedback degrades to 52% (ablation). Tension resolution that relies purely on LLM judgment (without checking raw/) will fail. The LLM may "resolve" contradictions by picking the claim that sounds more plausible, not the one that's actually supported.

**Rule:** Every tension resolution MUST verify against raw/ sources. If raw/ sources themselves disagree, the tension is real and should be documented, not forcefully resolved. Note: raw/ verification provides data grounding but not interpretation grounding — the same LLM reading raw/ may confirm its own misinterpretation (see [[autonomous-kb-failure-modes]] "The Layer 3 Circularity Problem").

**2. CALM → Self-Enhancement Bias Is the Central Risk**

The LLM that wrote both contradictory articles will prefer whichever formulation matches its own generation patterns (up to 16.1% error). "Resolution" may mean rewriting both articles in the LLM's style, losing the nuance that made the original formulations distinct.

**Rule:** raw/ is immutable. Resolution cannot ignore sources. Human patches (`> [!patch]`) remain the bias-free correction channel.

**3. ERL → Resolutions Become Heuristics**

A resolved tension should generate a reusable heuristic with trigger conditions, not just a point fix. Heuristics (+7.8%) vastly outperform trajectory-level fixes (-1.9%).

**Template:** "When [condition A], [claim X] applies; when [condition B], [claim Y] applies. The apparent contradiction resolves because [reason]."

**4. CARMO/SALC → Dynamic Criteria Per Tension**

Static "do these contradict? yes/no" is too binary. Each tension needs context-specific evaluation criteria considering: source types, claim domains, scale conditions, temporal context.

**Example:** "LC > RAG" vs "QMD hybrid is essential" → dynamic criteria recognize this is scale-contingent (LC at <200 articles, hybrid at 200+), not a real contradiction.

**5. Synapse → Graph-Based Discovery**

Contradictory articles may share no keywords or embedding similarity — they're semantically distant but logically conflicting. Wikilink graph traversal (follow bidirectional backlinks) is more likely to surface tensions than flat _index.md search.

**Discovery method:** For each pair of articles sharing 2+ raw/ sources, compare key claims. Graph adjacency (shared wikilinks) surfaces candidates; raw/ verification confirms.

**6. Knowledge Conflicts Survey → Formal Conflict Taxonomy**

The Knowledge Conflicts survey (Xu et al., 2024) provides the academic formalization of our tension types with three categories that map directly:

| Conflict Type | Definition | KB Equivalent |
|--------------|-----------|---------------|
| **Context-Memory** | External context contradicts model's parametric knowledge | Wiki article contradicts what the LLM "knows" from training → authority bias risk |
| **Inter-Context** | Multiple external sources contradict each other | Two wiki articles contradict each other → our tension detection in /review item 9 |
| **Intra-Memory** | Internal inconsistencies within model parameters | LLM generates different responses to same question phrased differently |

Critical finding: even GPT-4 shows **13% inconsistency rate** on paraphrased queries (intra-memory conflict). This directly validates our circuit breaker: don't trust a single /ask response on important claims.

**LLM behavior under conflict:** models show strong confirmation bias toward parametric knowledge, favor semantically coherent info, and are susceptible to misleading prompts. Implications: our /ask Layer 3 verification may be undermined by the LLM's tendency to confirm its own wiki interpretations.

### Resolution Protocol

When a tension is detected:

1. **Verify against raw/** — which claim is supported by which source?
2. **If only one supported:** generate `> [!patch]` with correction + source
3. **If both supported (contingent tension):** document as "Known Tension" in the more general article, with:
   - Both claims stated precisely
   - Conditions under which each applies
   - ERL-style heuristic with trigger conditions
   - Sources for each side
4. **NEVER force artificial consistency** — real tensions are knowledge, not errors

### Known Tensions in This Wiki

| Articles | Tension | Resolution |
|----------|---------|------------|
| [[retrieval-augmented-generation]] vs [[llm-knowledge-base]] | "LC > RAG 56.3% vs 49%" vs "QMD/hybrid essential" | Scale-contingent: LC sufficient at <200 articles, hybrid needed at 200+. Both claims correct in their domain. |
| [[self-improving-agents]] vs [[llm-as-judge]] | "Self-reflection improves agents" vs "Self-assessment unreliable (JudgeBench: near random)" | Grounding-contingent: reflection WITH external feedback works (Reflexion +22%); reflection WITHOUT ground truth fails (52%). Our Layer 3 raw/ verification provides the grounding. |
| [[agent-memory-architectures]] vs [[multi-agent-orchestration]] | "Single-agent maintains coherent reasoning" (Cognition) vs "Multi-agent outperforms on broad queries" (Anthropic) | Task-contingent: single-agent wins for deep sequential reasoning (one context thread); multi-agent wins for broad exploration (parallel compression reduces path-dependence). Coordination cost determines crossover. Verified: tim-kellogg raw/ confirms both claims and the Cognition critique ("too dispersed"). |
| [[retrieval-augmented-generation]] (RAPTOR) vs [[agent-memory-architectures]] (HippoRAG) | "Summarization tree retrieval" vs "Knowledge graph + PageRank retrieval" | Architecture-contingent: RAPTOR requires tree rebuild on new content; HippoRAG incrementally adds edges. RAPTOR better for static corpora, HippoRAG for evolving KBs. Our /ingest is incremental → HippoRAG pattern closer to our architecture. |
| [[agent-memory-architectures]] (engineering taxonomy) vs [[agent-memory-architectures]] (CoALA cognitive taxonomy) | "Factual/experiential/working" vs "Episodic/semantic/procedural" | Framework-contingent: engineering categories optimize for building systems; cognitive categories have decades of experimental validation. Neither is wrong. Episodic ≈ experiential-case, semantic ≈ factual, procedural ≈ experiential-skill. Working = working. |
| [[agent-memory-architectures]] (concept segmentation) vs [[agent-memory-architectures]] (EM-LLM surprise segmentation) | "Segment by concept (LLM judgment)" vs "Segment by Bayesian surprise (statistical signal)" | Method-contingent: surprise-based aligns 25-35x better with human perception; concept-based is pragmatic for KBs. Not exclusive — concepts refined using surprise as secondary signal. |

## Interpretação

Ver seções marcadas com (⚠️) no Conteúdo acima — conteúdo interpretativo está inline por razões de coesão narrativa.

## Conexões

- [[self-improving-agents]] — Reflexion's grounded feedback loop is the resolution mechanism
- [[llm-as-judge]] — self-enhancement bias is the central risk in LLM-mediated resolution
- [[kb-architecture-patterns]] — ERL validates heuristic-based resolution over point fixes
- [[memory-consolidation]] — /review is the operational context where tension resolution runs

## Fontes

- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — self-reflection without grounded feedback degrades to 52%; verification essential
- [CALM](../../raw/papers/calm-llm-judge-biases.md) — self-enhancement bias up to 16.1%; same model writing and judging is unreliable
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — heuristics > trajectories (+7.8% vs -1.9%); resolutions should be reusable
- [CARMO/SALC](../../raw/papers/carmo-context-aware-reward-modelling.md) — dynamic criteria outperform static rubrics; context-specific evaluation
- [Knowledge Conflicts Survey](../../raw/papers/knowledge-conflicts-llms-survey.md) — 3 formal conflict types (context-memory, inter-context, intra-memory), GPT-4 13% inconsistency rate
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — graph topology discovers non-obvious conflicts (Contextual Isolation problem)
