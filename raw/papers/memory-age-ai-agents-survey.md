---
source: https://arxiv.org/abs/2512.13564
authors: Yuyang Hu, Shichun Liu, Yanwei Yue, et al. (47 authors)
date: 2025-12-15
type: paper
arxiv: "2512.13564"
github: https://github.com/Shichun-Liu/Agent-Memory-Paper-List
---

# Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics

## Abstract

Survey examining memory systems in foundation model-based agents. Distinguishes agent memory from LLM memory, RAG, and context engineering. Proposes unified taxonomy through three lenses: forms, functions, and dynamics.

## Key Distinctions

- **Agent memory ≠ LLM memory**: LLM memory = parametric weights. Agent memory = external persistent storage + retrieval + evolution.
- **Agent memory ≠ RAG**: RAG is a retrieval technique. Agent memory encompasses formation, evolution, and retrieval as a full lifecycle.
- **Agent memory ≠ Context engineering**: Context engineering manages what goes into the prompt. Agent memory manages what persists across prompts.

## Forms: What Carries Memory?

### Token-Level Memory (explicit text in context)

| Subtype | Description | Examples |
|---------|-------------|---------|
| **Flat (1D)** | Linear text buffer, simplest form | Chat history, scratchpads |
| **Planar (2D)** | Structured key-value or tabular storage | MemoryBank, structured profiles |
| **Hierarchical (3D)** | Multi-tier with different granularity levels | MemGPT tiers, RAPTOR trees |

### Parametric Memory (encoded in weights)

| Subtype | Description |
|---------|-------------|
| **Internal** | Knowledge in the LLM's own weights via fine-tuning |
| **External** | Separate small models storing domain knowledge, queried by the main LLM |

### Latent Memory (compressed representations)

| Operation | Description |
|-----------|-------------|
| **Generate** | Create compressed embeddings from experience |
| **Reuse** | Retrieve and inject latent representations into context |
| **Transform** | Convert between latent and explicit representations |

## Functions: Why Agents Need Memory?

### Factual Memory — the "what"
- **User factual**: preferences, profile, history
- **Environment factual**: world knowledge, entity states

### Experiential Memory — the "how"
- **Case-based**: past problem-solution pairs (Retrieve-Reuse-Revise-Retain cycle)
- **Strategy-based**: abstract plans and workflows extracted from experience
- **Skill-based**: reusable tool sequences and subroutines
- **Hybrid**: combinations of the above

### Working Memory — the "currently relevant"
- **Single-turn**: scratchpads, chain-of-thought traces within one inference
- **Multi-turn**: active context maintained across conversation turns

## Dynamics: How Memory Operates

### Formation (creating memories)
- Semantic summarization
- Knowledge distillation
- Structured construction (graphs, tables)
- Latent representation (embeddings)
- Parametric internalization (fine-tuning)

### Evolution (changing memories)
- **Consolidation**: merging, deduplicating, abstracting (maps to KAIROS/Dream cycle)
- **Updating**: modifying existing memories with new information
- **Forgetting**: deliberate removal of stale or low-value memories (Ebbinghaus-inspired decay)

### Retrieval (accessing memories)
- Retrieval timing and intent (proactive vs reactive)
- Query construction (how to formulate retrieval queries)
- Retrieval strategies (vector similarity, graph traversal, hybrid, activation-based)
- Post-retrieval processing (reranking, filtering, integration)

## Benchmarks

| Benchmark | Focus | Key Feature |
|-----------|-------|-------------|
| LoCoMo | Long-conversation memory | Multi-hop, temporal, adversarial QA |
| LOCBENCH | Personal memory | User-specific fact recall |
| LongMemEval | Long-term memory | Cross-session consistency |
| InfiAgent-DABench | Agent + data analysis | Memory under tool use |
| τ-bench | Customer support | Multi-turn task completion |

## Open-Source Frameworks

| Framework | Key Feature |
|-----------|-------------|
| MemGPT/Letta | OS-inspired hierarchical memory |
| Mem0 | Self-improving memory layer |
| Zep | Entity-relationship graph memory |
| LangMem | In-context memory injection |
| A-Mem | Adaptive summarization memory |
| MemoryOS | OS-inspired multi-level memory |

## Research Frontiers (8 directions)

1. **Memory retrieval → memory generation**: from retrieving past memories to generating synthetic useful memories
2. **Automated memory management**: self-organizing without human-designed schemas
3. **RL + memory**: learning what to remember/forget via reward signals
4. **Multimodal memory**: beyond text — images, audio, structured data
5. **Shared multi-agent memory**: common memory across agent teams
6. **Memory for world models**: grounding memory in environment dynamics
7. **Trustworthy memory**: poisoning, hallucination propagation, privacy
8. **Human-cognitive connections**: bridging neuroscience models to agent design
