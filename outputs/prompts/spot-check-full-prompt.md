# Independent Review Prompt — Spot-Check 3 Wiki Articles Against Raw Sources

## Instructions

You are an independent reviewer. You did NOT write these wiki articles. Your job is to find errors, misinterpretations, and unjustified claims.

Below are 3 wiki articles from an LLM-compiled knowledge base, each followed by the raw source papers they cite. The wiki articles were written by an LLM that compiled the raw sources — you are checking its work.

For EACH article, evaluate:

### 1. Factual Accuracy
- Does the article accurately represent the numbers, results, and claims from the raw sources?
- Are any statistics wrong, exaggerated, or taken out of context?
- Flag specific claims with the exact quote from raw/ that confirms or contradicts.

### 2. Interpretation Fidelity
- Does the article's synthesis faithfully represent what the papers actually argue?
- Are there claims in the wiki that SOUND like they come from the sources but are actually the LLM's own interpretation?
- Watch for: overstatements ("proves" vs "suggests"), false generalization (result on one benchmark stated as universal), and missing caveats that the original paper included.

### 3. Semantic Convergence Check
- Does the article's writing style differ from the raw sources, or has it been homogenized into a single academic voice?
- Karpathy's source is an informal tweet thread. Does the article preserve that informality or rewrite it as formal prose?
- If all three articles sound identical in tone despite citing very different source types (tweets, academic papers, repo READMEs), that's a problem.

### 4. Missing Nuance
- What did the original papers say that the wiki articles DON'T mention?
- Are there important limitations, caveats, or failure cases from the papers that were dropped?

### 5. Unjustified Connections
- The articles contain [[wikilinks]] connecting concepts. Are any of these connections claimed but not actually supported by the underlying sources?
- Is the article making the sources say something they don't?

## Output Format

For each article, provide:
```
ARTICLE: [name]
VERDICT: ACCURATE / MOSTLY ACCURATE / INACCURATE

FACTUAL ERRORS: [list with specific quotes from raw/ that contradict]
INTERPRETATION ISSUES: [list of claims that go beyond what sources say]
MISSING NUANCE: [what the sources say that the article omits]
STYLE: [preserved / homogenized]
UNJUSTIFIED CONNECTIONS: [wikilinks that aren't supported by sources]

SEVERITY: [critical / moderate / minor]
```

Be harsh. The purpose is to find what's wrong, not to confirm the wiki is good. If everything looks correct, say so — but err on the side of flagging suspicious interpretations.

---

## Articles and Sources to Review
=== ARTICLE: kb-architecture-patterns (post-fix) ===

---
title: "KB Architecture Patterns"
sources:
  - path: raw/articles/karpathy-llm-knowledge-bases.md
    type: note
    quality: tertiary
  - path: raw/articles/elvis-personal-kb-agents.md
    type: note
    quality: tertiary
  - path: raw/articles/paulo-silveira-open-claw-pkm.md
    type: article
    quality: secondary
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/papers/long-context-vs-rag-evaluation.md
    type: paper
    quality: primary
  - path: raw/papers/raptor-recursive-abstractive-retrieval.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [taxonomy, architecture, patterns]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Four distinct architectural patterns for LLM-powered knowledge bases have emerged from practitioners and research. They differ in who controls synthesis (LLM vs human), how retrieval scales (index vs search vs RAG), and where the bottleneck sits (ingest quality vs context budget vs editorial judgment).

## Conteúdo

### Pattern 1: LLM-as-Compiler

**Originator:** Karpathy (April 2026)

**Architecture:** `raw/ → LLM compiles wiki/ → LLM does Q&A → outputs filed back`

**Key characteristics:**
- LLM is the sole writer; human rarely touches wiki directly
- Index files + brief summaries sufficient at ~100 articles / ~400K words
- Outputs (reports, slides) cycle back to enrich the wiki
- Linting via periodic LLM health checks

**Strengths:** Closed loop, incremental, works without RAG at small scale.
**Weaknesses:** Scale limited by context window. No explicit source verification. Quality depends on ingest prompt.

**When to use:** Solo researcher, <200 articles, single domain.

### Pattern 2: Agent-as-Curator

**Originator:** Elvis/DAIR.ai (April 2026)

**Architecture:** `Automated curation → hybrid search (QMD) → MCP visual artifacts → actionable insights`

**Key characteristics:**
- Tuned Skill automates paper discovery and filtering
- [[hybrid-search|QMD]] provides BM25 + vector + reranking over the corpus
- MCP tools power interactive visualizations inside agent orchestrator
- Focus on actionability: "research questions are only as good as the insights agents have access to"

**Strengths:** Scales to 100s of papers via semantic search. Automated curation removes human bottleneck. Visual artifacts surface non-obvious patterns.
**Weaknesses:** Complex setup (QMD, MCP, orchestrator). Depends on external tooling.

**When to use:** Heavy paper consumption, 200+ sources, need for visual exploration.

### Pattern 3: Human-in-the-Loop

**Originator:** Paulo Silveira / Open Claw (March 2026)

**Architecture:** `Multi-modal capture → LLM classifies → human writes final output`

**Key characteristics:**
- Telegram as universal input (voice, text, photos, links)
- Whisper transcribes audio; Claude Sonnet classifies into concepts
- Human retains editorial control over final synthesis
- Anti-slop philosophy: "letting machines generate final drafts creates generic-feeling content"

**Strengths:** Preserves authorial voice. No idea lost. Historical pattern (Zettelkasten, Dostoevsky's dictation).
**Weaknesses:** Doesn't scale. Synthesis bottleneck is human.

**When to use:** Personal brand writing, high-stakes content, when voice matters more than throughput.

### Pattern 4: Bandwidth-Aware Retrieval

**Originator:** Claude Code internals (March 2026)

**Architecture:** `Layered retrieval with progressive escalation + circuit breakers`

**Key characteristics:**
- 3+ layers: lightweight index (always loaded) → article content (on-demand) → raw sources (spot-check)
- Progressive compaction: micro → snip → auto → collapse
- Circuit breakers prevent thrashing (max 3 consecutive failures)
- Principle: "never read more than you need at each layer"

**Strengths:** Token-efficient, production-proven. Graceful degradation under pressure.
**Weaknesses:** Designed for conversations, not knowledge bases. No notion of source quality.

**When to use:** Any KB retrieval system. This is a universal pattern, not an alternative to the others — it's how retrieval should work within any of the above.

### Comparison Matrix

| Pattern | Who synthesizes | Retrieval | Scale | Bottleneck |
|---------|----------------|-----------|-------|------------|
| LLM-as-Compiler | LLM | Index-based (LC) | ~200 articles | Ingest quality |
| Agent-as-Curator | LLM + tools | Hybrid search | 1000+ papers | Tooling setup |
| Human-in-the-Loop | Human | LLM classification | ~50 outputs | Human time |
| Bandwidth-Aware | (meta-pattern) | Layered escalation | Any | Context budget |

## Interpretação

### RAPTOR Analogy for _index.md

RAPTOR's summary nodes contribute 23-57% of useful retrieved content. Our _index.md with ~150 char pointers serves a similar function — but this is an analogy, not a validation. RAPTOR operates on document chunks with embeddings; our _index operates on concept pointers read by an LLM. The mechanism is different even if the abstraction-level pattern resembles.

| RAPTOR Level | KB Equivalent (analogy) |
|-------------|--------------------------|
| Raw chunks (leaf nodes) | raw/ sources |
| Cluster summaries (mid-level) | wiki/concepts/ articles |
| Root summaries (top-level) | _index.md pointers |

### ERL's Heuristics Result Applied to KB

ERL shows heuristics (+7.8%) > trajectories (-1.9%) on Gaia2. Our wiki articles resemble heuristics (distilled principles by concept). But ERL tested on agent task execution, not knowledge compilation — the transfer is plausible but not directly validated.

### KAIROS-Review Parallel

The KAIROS cycle (orient → gather → consolidate → prune) resembles a /review cycle. Both consolidate knowledge, but KAIROS operates on ephemeral conversational memory; /review on durable compiled knowledge. The parallel suggests borrowing KAIROS's trigger gates (time-based, session-based) for /review automation.

## Conexões

- [[llm-knowledge-base]] — Pattern 1 is the core architecture of this KB
- [[hybrid-search]] — Pattern 2's retrieval layer; our Fase 2-3 upgrade path
- [[context-management]] — Pattern 4 formalized; our /ask already implements 3 layers
- [[memory-consolidation]] — KAIROS cycle parallels /review; trigger gates transferable
- [[retrieval-augmented-generation]] — Academic evidence that LC > RAG at small scale (Pattern 1 validated)
- [[self-improving-agents]] — ERL validates concept articles > raw sources; Reflexion parallels our patch system
- [[tension-resolution]] — framework for detecting and resolving contradictions between articles, informed by 5 papers

## Fontes

- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — Pattern 1: the original architecture
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — Pattern 2: automated curation + QMD + visual artifacts
- [Paulo Silveira — Open Claw](../../raw/articles/paulo-silveira-open-claw-pkm.md) — Pattern 3: human-in-the-loop, anti-slop philosophy
- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — Pattern 4: compaction hierarchy, circuit breakers
- [LC vs RAG Paper](../../raw/papers/long-context-vs-rag-evaluation.md) — Validates Pattern 1 at small scale (LC 56.3% vs RAG 49.0%)
- [RAPTOR Paper](../../raw/papers/raptor-recursive-abstractive-retrieval.md) — Validates _index.md as manual RAPTOR tree; summary nodes contribute 23-57% of retrieval
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — Heuristics > trajectories: concept articles validated as superior to raw source dumps

=== ARTICLE: autonomous-kb-failure-modes (post-fix) ===

---
title: "Autonomous KB Failure Modes"
sources:
  - path: raw/papers/calm-llm-judge-biases.md
    type: paper
    quality: primary
  - path: raw/papers/judgebench-evaluating-llm-judges.md
    type: paper
    quality: primary
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/synapse-episodic-semantic-memory.md
    type: paper
    quality: primary
  - path: raw/papers/multiagent-debate-factuality.md
    type: paper
    quality: primary
  - path: raw/papers/model-collapse-recursive-training.md
    type: paper
    quality: primary
  - path: raw/papers/wikipedia-era-llms-risks.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [meta-kb, failure-analysis, safety, original-insight]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

An LLM-operated KB without human intervention degrades silently over ~30 days through 4 failure modes: semantic convergence (articles homogenize), authority bias cascade (errors crystallize via circular validation), index bloat (growth without quality gate), and forced tension resolution (nuance eliminated). The system appears healthy on all automated metrics while quality erodes — the KB equivalent of reward hacking.

## Conteúdo

### Failure Mode 1: Semantic Convergence (Week 1-2)

**Mechanism:** Self-enhancement bias (CALM: 16.1% error) + unsupervised /review = LLM rewrites articles in its preferred style each review cycle. "Convert vague to precise" and "deduplicate" are opportunities to homogenize.

**Academic formalization: Model Collapse** (Shumailov et al., Nature 2024). Recursive self-consumption destroys distributional diversity — "tails of the original content distribution disappear." Applied to KBs: when an LLM compiles wiki from its own synthesis, diversity narrows and nuance disappears. The mitigation from the paper: "if data accumulates and models train on a mixture of real and synthetic data, model collapse no longer occurs." For us: /review must always re-read raw/ (real data), never operate only on wiki/ (synthetic data).

**Empirical validation: Wikipedia risks** (Huang et al., 2025). "AI-revised Wikipedia content lowered RAG performance, particularly in factual accuracy." Stylistic homogenization detected at Wikipedia scale: sentences becoming "more AI-like, with longer, more complex sentences." Our KB is a micro-scale version of the same phenomenon.

**Why invisible:** Wiki gets *more consistent*, not less. All /review metrics stay green. Problem is qualitative: wiki loses perspective diversity that justifies having multiple sources.

**Evidence:** ERL shows random heuristic inclusion degrades after 40-60 items. When all articles use same formulations, _index.md loses discriminative power. Note: this 40-60 threshold also applies to _index.md scaling — see [[raptor-vs-flat-retrieval]] Gap 3 for the connection between ERL's selection limit and the practical threshold for sub-index migration.

**Breaks:** /ask on subtle topics returns generic answers. Distinctions from original sources (Karpathy writes differently than an academic paper) are lost.

### Failure Mode 2: Authority Bias Cascade (Week 2-3)

**Mechanism:** Authority bias (CALM) makes LLM trust cited claims more. Wiki articles cite raw/. When /ask verifies wiki against raw/ (Layer 3), it tends to *confirm* because raw/ was the original source — circular validation loop.

**Compounding:** Without human reading raw/ with fresh eyes, /ingest misinterpretations crystallize. JudgeBench: self-assessment on difficult problems is near-random. If original interpretation was plausibly wrong, LLM "verifies" and agrees with itself.

**Evidence:** Reflexion ablation — self-reflection without *independent* grounded feedback degrades to 52%. raw/ is grounded but read by the same LLM. Ground truth needs independent evaluator.

### Failure Mode 3: Index Bloat (Week 2-4)

**Mechanism:** Automated /ingest without human quality gate. Confidence scoring (high/medium/low) is self-assessment (failure mode 2 applies). Tertiary sources create low-value articles that occupy _index.md space.

**Breaks:** _index.md approaches migration trigger (~200 entries). /ask spends more tokens on orientation, less on depth. ERL shows indiscriminate inclusion is counterproductive.

**Evidence:** Tim Kellogg — "compression becomes cognitive work." Without human deciding what deserves wiki vs. stays in raw/, agent treats everything as equally important.

### Failure Mode 4: Forced Tension Resolution (Week 3-4)

**Mechanism:** /review item 9 detects tensions and attempts resolution. Without human validating that a tension is *real* (contingent), agent tends to force consistency by eliminating one claim.

**Breaks:** Wiki becomes dogmatic. Loses conditional reasoning ("when to use LC vs RAG?") because the condition was eliminated.

**Evidence:** Tension-resolution protocol says "NEVER force artificial consistency" but agent judges what's "artificial" via self-evaluation (near-random per JudgeBench).

### Degradation Timeline

```
Day 1-7:   Works well. Same phase benchmarks measure. (Honeymoon)
Day 7-14:  Semantic convergence starts. Invisible to automated metrics.
Day 14-21: Authority bias crystallizes errors. Tensions force-resolved.
Day 21-30: Wiki looks healthy (0 warnings) but /ask answers are generic
           and occasionally plausibly wrong. Degradation undetectable
           without external ground truth test.
```

### The Core Problem

The system optimizes visible metrics (0 warnings, correct links, cited sources) while real quality erodes. This is the KB equivalent of reward hacking documented by CARMO.

### Mitigations

| Failure | Mitigation | Automatable? |
|---------|-----------|-------------|
| Semantic convergence | Style divergence metric: compare article text to raw/ source style | Yes — could be a /review check |
| Authority cascade | Human re-reads 2-3 random articles/week against raw/ | No — needs independent evaluator |
| Index bloat | Human quality gate on /ingest, or hard cap on articles per week | Partially — cap is automatic, judgment is not |
| Forced tension | Require human `> [!patch]` before any tension resolution is applied | Yes — rule change in /review |

### The Layer 3 Circularity Problem

The /ask protocol treats raw/ verification (Layer 3) as grounded feedback: "Para claims importantes: vá à fonte original em raw/ para verificar." But this conflates two types of grounding:

- **Data grounding** (what raw/ provides): the original text is immutable and available
- **Interpretation grounding** (what raw/ does NOT provide): the same LLM that wrote the wiki reads raw/ and evaluates its own interpretation

In Reflexion's terms, grounded feedback means **executable tests** — unit tests that pass or fail independently of the agent's judgment. raw/ read by the same LLM is closer to self-reflection without tests (the 52% degradation case). The data is external; the interpretation is not.

This means Layer 3 is necessary but insufficient. It catches factual errors (wrong numbers, misattributed claims) but cannot catch interpretive errors (correct facts assembled into wrong conclusions). The /ask protocol should be understood as: Layer 3 provides data verification, not interpretation verification. See [[llm-as-judge]] for why the same model cannot reliably judge its own interpretive work (self-enhancement bias 16.1%).

### Architectural Insight

The blueprint's existing mechanisms (raw/ immutable, patches humanos, retrieval cético, confidence scoring) are correct — but they were designed as **guardrails with human in the loop**. Without human, the agent can satisfy all rules while circumventing their intent: verify raw/ and agree with itself, assign high confidence to own work, resolve tensions "following protocol."

The fix is not more rules — it's **external ground truth**. At least one verification channel must be independent of the LLM that maintains the wiki. Concretely, this means either: (1) a different model for /review than for /ingest, (2) human spot-checks, or (3) executable validation (tests, type-checks, API calls that return ground truth).

### Multiagent Debate as Middle Ground

Du et al. (2023) propose a fourth option: multiagent debate. Multiple LLM instances generate independent evaluations, read each other's responses, and debate across rounds to converge toward consensus. This significantly enhances factual validity and reduces hallucinations.

**Applied to /review:** instead of one LLM evaluating its own wiki, spawn 2-3 independent evaluations of each article, then debate disagreements. This mitigates self-enhancement bias without requiring a human — the "independent evaluator" is another instance of the same model, but with a different conversation history and evaluation context.

**Tension with single-agent:** Tim Kellogg documents Cognition's critique that multi-agent creates "fragile systems" with "dispersed decision-making." Multiagent debate fixes bias but adds coordination cost and context fragmentation. Neither single-agent nor multi-agent /review dominates — the choice depends on whether bias risk (single) or coordination fragility (multi) is the bigger threat for the specific article being reviewed.

## Conexões

- [[llm-as-judge]] — self-enhancement bias (16.1%) and authority bias are the root causes
- [[self-improving-agents]] — Reflexion without grounded feedback degrades to 52%; applies to autonomous /review
- [[tension-resolution]] — forced resolution is failure mode 4; protocol already says "never force" but enforcement requires human
- [[memory-consolidation]] — /review and /dream operate on the wiki; both susceptible to convergence
- [[kb-architecture-patterns]] — all 4 patterns assume human-in-the-loop for quality; none designed for full autonomy
- [[raptor-vs-flat-retrieval]] — ERL's 40-60 item selection limit applies to both semantic convergence detection and index scaling thresholds
- [[reflexion-weighted-knowledge-graphs]] — adaptive topology could mitigate failure mode 1 if edge weights incorporate external signal

## Fontes

- [CALM](../../raw/papers/calm-llm-judge-biases.md) — self-enhancement 16.1%, authority bias, circular validation risk
- [JudgeBench](../../raw/papers/judgebench-evaluating-llm-judges.md) — self-assessment near random on hard tasks, reliability inflated by benchmark difficulty
- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — without independent grounding, self-reflection degrades to 52%
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — random inclusion degrades after 40-60; indiscriminate growth is counterproductive
- [Model Collapse](../../raw/papers/model-collapse-recursive-training.md) — recursive self-consumption destroys diversity (Nature 2024); mixture of real+synthetic data prevents collapse
- [Wikipedia Risks](../../raw/papers/wikipedia-era-llms-risks.md) — AI-revised content lowers RAG performance; stylistic homogenization detected empirically
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — Cognitive Tunneling: hub suppression as analogy for convergence

=== ARTICLE: llm-knowledge-base (post-fix) ===

---
title: "LLM Knowledge Base"
sources:
  - path: raw/articles/karpathy-llm-knowledge-bases.md
    type: note
    quality: tertiary
  - path: raw/articles/elvis-personal-kb-agents.md
    type: note
    quality: tertiary
  - path: raw/articles/paulo-silveira-open-claw-pkm.md
    type: article
    quality: secondary
  - path: raw/papers/wikipedia-era-llms-risks.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [core-concept, knowledge-management, wiki, obsidian]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

An LLM Knowledge Base is a personal knowledge system where raw sources are "compiled" by an LLM into an interlinked markdown wiki, then queried via the same LLM for Q&A with source citation. The pattern emerged in April 2026 from practitioners (Karpathy, Elvis/DAIR.ai) who independently converged on the same architecture: raw/ → ingest → wiki/ → ask.

## Conteúdo

### The Core Loop

```
raw/ (immutable sources)
  → /ingest (LLM compiles concepts)
    → wiki/ (interlinked .md articles)
      → /ask (retrieval + Q&A with citations)
        → outputs/ (reports, slides, visualizations)
          → optionally filed back into wiki/
```

Key insight from Karpathy: "a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge." The LLM shifts from code tool to knowledge compiler.

### Karpathy's Architecture (April 2026)

- **raw/**: articles, papers, repos, datasets, images indexed into a directory
- **Wiki**: LLM incrementally "compiles" .md files with summaries, backlinks, concepts, articles, cross-links
- **Ingest**: Obsidian Web Clipper for articles → markdown; hotkey to download images locally
- **IDE**: Obsidian as frontend (view raw, wiki, visualizations). "The LLM writes and maintains all of the data of the wiki, I rarely touch it directly."
- **Q&A**: At ~100 articles / ~400K words, LLM answers complex questions without fancy RAG. Auto-maintained index files + brief summaries sufficient at this scale.
- **Output**: Markdown files, Marp slides, matplotlib images — all viewable in Obsidian. Outputs often filed back into wiki.
- **Linting**: LLM health checks find inconsistent data, impute missing data, suggest new article candidates.
- **Scaling vision**: "synthetic data generation + finetuning to have your LLM 'know' the data in its weights instead of just context windows"

### Elvis/DAIR.ai's Extensions

Elvis builds on the same pattern with key additions:

- **Automated curation**: a tuned Skill that finds high-signal research papers daily, replacing manual review
- **QMD indexing**: uses Tobi Lütke's [[hybrid-search|QMD]] for semantic search over the paper collection
- **Visual artifacts**: interactive artifact generator using MCP tools inside an agent orchestrator, visualizing insights from 100s of papers
- **Actionability focus**: "the research is only as good as the research questions. And the research questions are only as good as the insights the agents have access to."
- **Strong claim**: "everyone should be building both their own agent harnesses and their personal knowledge bases. Those are going to be a huge differentiator."

### Paulo Silveira's Human-in-the-Loop Variant (Open Claw)

A contrasting approach from Paulo Silveira (March 2026): the LLM assists with capture and classification, but humans maintain editorial control.

**Pipeline:** Telegram (voice/text/photos/links) → Whisper transcription → journaling → Claude Sonnet classification into concepts → drafts for blog posts. Storage in Git vault with Journal + Concepts + Drafts.

**Key philosophical difference:** "Eu poderia tentar deixar essa concatenação de ideias e reestruturação do texto para a máquina... Não farei." Silveira argues that full LLM rewriting creates generic "slop." The LLM organizes; the human writes.

**Historical context:** References Zettelkasten, personal wikis, and Dostoevsky dictating to his wife as stenographer. The pattern is old; the tools are new.

**Trade-off:** Capture time doesn't decrease, but no idea is lost. The bottleneck shifts from capture to synthesis — exactly where human judgment adds the most value.

### The "Ephemeral Wiki" Vision

Karpathy's follow-up: "every question to a frontier grade LLM spawns a team of LLMs to automate the whole thing: iteratively construct an entire ephemeral wiki, lint it, loop a few times, then write a full report. Way beyond a `.decode()`."

This connects to [[autonomous-research-agents]] — a persistent KB is a durable instance of what deep research agents do ephemerally.

### Index-Based Retrieval (Why Not RAG?)

Karpathy's surprising finding: at ~small scale (~100 articles), auto-maintained index files + brief summaries are sufficient. No need for embeddings or vector databases. The LLM "reads all the important related data fairly easily."

This maps to a 3-layer bandwidth-aware retrieval pattern:
1. Lightweight index (always loaded)
2. Article content (on-demand)
3. Raw sources (spot verification)

See [[context-management]] for the formal hierarchy and [[retrieval-augmented-generation]] for when RAG becomes necessary.

### Risks of LLM-Compiled Knowledge (challenging source)

The "Wikipedia in the Era of LLMs" study (Huang et al., 2025) provides empirical evidence that LLM-compiled content degrades the knowledge it compiles:

- AI-revised Wikipedia content **lowered RAG performance**, particularly in factual accuracy
- Feedback loop risk: "RAG systems could end up retrieving AI-generated information to fact-check AI-generated responses"
- Stylistic homogenization detected: sentences becoming "more AI-like, with longer, more complex sentences"
- If the wiki feels too synthetic, the human stops engaging — reducing the human-in-the-loop correction mechanism

This directly challenges the LLM-as-Compiler pattern. The mitigation: raw/ immutability ensures the "real data" is always accessible, but only if /review and /ask always re-read raw/ rather than trusting wiki alone. See [[autonomous-kb-failure-modes]] for the full degradation timeline.

## Conexões

- [[retrieval-augmented-generation]] — the academic framing of when LC vs RAG is needed
- [[hybrid-search]] — QMD as the upgrade path when flat index retrieval hits limits
- [[memory-consolidation]] — the KB's /review cycle mirrors the dream consolidation pattern
- [[autonomous-research-agents]] — KB is persistent deep research; deep research is ephemeral KB
- [[kb-architecture-patterns]] — taxonomy of 4 KB patterns; this KB implements Pattern 1
- [[obsidian-agent-workflow]] — the frontend layer for viewing and navigating the wiki
- [[autonomous-kb-failure-modes]] — what goes wrong when the compilation loop runs unsupervised

## Fontes

- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — original tweet defining the architecture: raw/ → compile → wiki/ → Q&A → lint
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — extensions: automated curation, QMD search, visual artifacts, actionability
- [Paulo Silveira — Open Claw](../../raw/articles/paulo-silveira-open-claw-pkm.md) — human-in-the-loop variant: LLM classifies, human writes. Anti-slop philosophy
- [Wikipedia Risks](../../raw/papers/wikipedia-era-llms-risks.md) — (challenging) AI-revised content lowers RAG performance, stylistic homogenization empirically detected

=== RAW: model-collapse ===
---
source: https://arxiv.org/abs/2305.17493
authors: Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Yarin Gal, Nicolas Papernot, Ross Anderson
date: 2023-05-27
type: paper
arxiv: "2305.17493"
venue: Nature 2024
stance: challenging
---

# The Curse of Recursion: Training on Generated Data Makes Models Forget (Model Collapse)

## Abstract

Use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. This "Model Collapse" occurs across multiple architectures (VAEs, GMMs, LLMs). As AI-generated text populates the internet, data quality concerns become critical. Data collected about genuine human interactions will be increasingly valuable.

## Key Finding

Model collapse = recursive self-consumption destroys distributional diversity. Tails disappear first — rare but important information is lost. The model converges to a narrow, homogeneous output.

## Direct Challenge to LLM-KB Architecture

This is the academic formalization of our "semantic convergence" failure mode (autonomous-kb-failure-modes). When an LLM writes wiki articles, then reads those articles to write more articles or answer questions, and the answers feed back into the wiki — this is recursive self-consumption on knowledge, not weights.

The analogy:
- Model collapse (weights): train on own output → distribution narrows → tails disappear
- Wiki collapse (knowledge): compile from own synthesis → diversity narrows → nuance disappears

Our raw/ immutability principle is the mitigation: raw/ is "real data" (human-written sources), wiki/ is "generated data" (LLM-compiled). As long as /ingest always reads raw/ (not wiki/) to generate articles, the recursive loop is broken. But /review reads wiki/ to improve wiki/ — that's the recursive path.

## Mitigation from the Paper

"If data accumulates and models train on a mixture of real and synthetic data, model collapse no longer occurs." Applied to KB: always mix raw/ sources (real) with existing wiki (synthetic) when doing /review. Never let /review operate only on wiki/ without re-reading raw/.

=== RAW: wikipedia-risks ===
---
source: https://arxiv.org/abs/2503.02879
authors: Siming Huang, Yuliang Xu, Mingmeng Geng, Yao Wan, Dongping Chen
date: 2025-03-04
type: paper
arxiv: "2503.02879"
stance: challenging
---

# Wikipedia in the Era of LLMs: Evolution and Risks

## Abstract

Comprehensive analysis of how LLMs affect Wikipedia. Articles show ~1% impact in certain categories. Contaminated training data could inflate benchmarks and compromise RAG effectiveness. "LLMs have not yet fully changed Wikipedia's language and knowledge structures" but future risks warrant careful consideration.

## Key Findings Relevant to LLM KBs

1. **AI-revised Wikipedia content lowered RAG performance, particularly in factual accuracy.** If our wiki articles are LLM-compiled and later used as retrieval context for /ask, the same degradation applies.

2. **Feedback loop risk:** "RAG systems could end up retrieving AI-generated information to fact-check AI-generated responses." Our Layer 3 verification (wiki → check against raw/) is designed to break this loop, but only if raw/ stays human-authored.

3. **Stylistic homogenization detected:** Wikipedia sentences becoming "more AI-like, with longer, more complex sentences but fewer auxiliary verbs." Our semantic convergence concern is validated at Wikipedia scale.

4. **Human contributor decline:** "once more than half of online activity is transacted by AI, human users may decide to leave." For a personal KB, this translates to: if the wiki feels too synthetic, the human stops engaging with it.

## Direct Challenge

This paper argues that LLM-compiled knowledge systems degrade the quality of the very knowledge they compile. Our KB is a micro-scale Wikipedia compiled by LLM — the same risks apply, perhaps more acutely because we have one compiler (not many) and no community review process.

=== RAW: karpathy ===
---
source: https://x.com/karpathy/status/1907507437397045572
author: Andrej Karpathy
date: 2026-04-02
type: note
---

# LLM Knowledge Bases

Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it. So:

## Data ingest

I index source documents (articles, papers, repos, datasets, images, etc.) into a raw/ directory, then I use an LLM to incrementally "compile" a wiki, which is just a collection of .md files in a directory structure. The wiki includes summaries of all the data in raw/, backlinks, and then it categorizes data into concepts, writes articles for them, and links them all. To convert web articles into .md files I like to use the Obsidian Web Clipper extension, and then I also use a hotkey to download all the related images to local so that my LLM can easily reference them.

## IDE

I use Obsidian as the IDE "frontend" where I can view the raw data, the compiled wiki, and the derived visualizations. Important to note that the LLM writes and maintains all of the data of the wiki, I rarely touch it directly. I've played with a few Obsidian plugins to render and view data in other ways (e.g. Marp for slides).

## Q&A

Where things get interesting is that once your wiki is big enough (e.g. mine on some recent research is ~100 articles and ~400K words), you can ask your LLM agent all kinds of complex questions against the wiki, and it will go off, research the answers, etc. I thought I had to reach for fancy RAG, but the LLM has been pretty good about auto-maintaining index files and brief summaries of all the documents and it reads all the important related data fairly easily at this ~small scale.

## Output

Instead of getting answers in text/terminal, I like to have it render markdown files for me, or slide shows (Marp format), or matplotlib images, all of which I then view again in Obsidian. You can imagine many other visual output formats depending on the query. Often, I end up "filing" the outputs back into the wiki to enhance it for further queries. So my own explorations and queries always "add up" in the knowledge base.

## Linting

I've run some LLM "health checks" over the wiki to e.g. find inconsistent data, impute missing data (with web searchers), find interesting connections for new article candidates, etc., to incrementally clean up the wiki and enhance its overall data integrity. The LLMs are quite good at suggesting further questions to ask and look into.

## Extra tools

I find myself developing additional tools to process the data, e.g. I vibe coded a small and naive search engine over the wiki, which I both use directly (in a web ui), but more often I want to hand it off to an LLM via CLI as a tool for larger queries.

## Further explorations

As the repo grows, the natural desire is to also think about synthetic data generation + finetuning to have your LLM "know" the data in its weights instead of just context windows.

## Follow-up

> Oh and in the natural extrapolation, you could imagine that every question to a frontier grade LLM spawns a team of LLMs to automate the whole thing: iteratively construct an entire ephemeral wiki, lint it, loop a few times, then write a full report. Way beyond a `.decode()`.

## TLDR

Raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM. I think there is room here for an incredible new product instead of a hacky collection of scripts.
