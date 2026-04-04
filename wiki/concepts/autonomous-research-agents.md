---
title: "Autonomous Research Agents"
sources:
  - path: raw/papers/deep-research-survey-autonomous-agents.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [deep-research, agent-pipeline, survey]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Autonomous research agents are LLM-powered systems that transform a research question into a comprehensive, fact-grounded report through a 4-stage pipeline: planning, question developing, web exploration, and report generation. The Deep Research survey (2025) provides the canonical taxonomy of approaches, benchmarks, and open challenges.

## Conteúdo

### The 4-Stage Pipeline

#### 1. Planning
Transforming a research question into a structured plan of subgoals.

Key approaches: world model simulation (WebDreamer, WebPilot), learnable planning (AgentSquare, MindSearch, SimpleDeepSearcher).

**Open challenge:** Plans lack robustness to ambiguous questions. Hallucinated steps propagate errors downstream.

#### 2. Question Developing
Converting subgoals into search queries optimized for retrieval.

Two paradigms:
- **Reward-optimized** (RL-based): DeepResearcher, Search-R1, ZeroSearch. Format rewards enforce syntax; answer rewards (F1-based) improve relevance.
- **Supervision-driven**: ManuSearch, Search-o1. Multi-agent systems with separate planning, searching, extraction agents. More controllable but limited by demonstration quality.

**Open challenge:** Generated queries are too narrow for open-ended problems.

#### 3. Web Exploration
Retrieving relevant information from online sources.

Two categories:
- **Browser-based agents**: WebGPT, Selenium-based. Fail on visually-complex layouts.
- **Multimodal agents**: WebVoyager (59% task success with GPT-4V), MM-ReAct.
- **API-based**: OpenAI/Bing, Grok/xAI, Gemini/Google, Perplexity/Sonar.

**Open challenge:** Web agents are flexible but slow; APIs are fast but inflexible. Hybrid architectures needed.

#### 4. Report Generation
Synthesizing retrieved information into coherent, factually-grounded output.

Two dimensions:
- **Structure control**: planning-based outlines, constraint-guided formats
- **Factual integrity**: faithful modeling, conflict resolution across contradicting sources

**Open challenge:** Most methods optimize single stages, not the full pipeline. Few handle conflicting sources well.

### Commercial Deep Research Systems

| System | Search Infrastructure |
|--------|----------------------|
| OpenAI DeepResearch | Microsoft Bing |
| Grok DeepSearch | xAI crawler + X posts |
| Gemini DeepResearch | Google proprietary |
| Perplexity DeepResearch | Bing-style index + Sonar API |

### Benchmarks

| Benchmark | Coverage | Key Metrics |
|-----------|----------|-------------|
| DeepResearch Bench | Full pipeline | Pairwise Agreement Rate |
| DeepResearchGym | Full pipeline | KPR, Precision, Recall, Clarity |
| MedBrowseComp | Full pipeline | Accuracy (biomedical) |
| Humanity's Last Exam | Planning + QD + WE | Accuracy, Calibration Error |

### 5 Open Challenges

1. **Multi-tool integration**: beyond search engines → APIs, databases, code repos
2. **Factuality**: hallucinations when aggregating inconsistent sources
3. **Multimodal reasoning**: text-only pipelines can't handle charts, PDFs, images
4. **Workflow generalization**: high compute costs, sparse reward signals
5. **Personalization**: no persistent user modeling or dynamic adaptation

### Relevance to Knowledge Bases

Karpathy's follow-up tweet captures the connection: "every question to a frontier LLM spawns a team of LLMs to automate the whole thing: iteratively construct an entire ephemeral wiki, lint it, loop a few times, then write a full report." An LLM knowledge base is a persistent instance of what deep research agents do ephemerally.

## Interpretação

Nenhuma interpretação significativa neste artigo — conteúdo é factual direto das fontes.

## Conexões

- [[multi-agent-orchestration]] — multi-agent systems share the same coordination patterns
- [[hybrid-search]] — web exploration stage benefits from hybrid retrieval approaches
- [[llm-knowledge-base]] — persistent KB is a durable instance of what deep research does ephemerally
- [[self-improving-agents]] — pipeline could use Reflexion for iterative query refinement

## Fontes

- [Deep Research Survey](../../raw/papers/deep-research-survey-autonomous-agents.md) — canonical survey: 4-stage pipeline taxonomy, benchmarks, commercial systems, open challenges
