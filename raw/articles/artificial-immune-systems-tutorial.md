---
source: https://arxiv.org/abs/1006.4949
authors: Julie Greensmith, Amanda Whitbrook, Uwe Aickelin
date: 2010-06-25
type: article
quality: primary
stance: challenging
---

# Artificial Immune Systems Tutorial

## Overview

AIS are algorithms inspired by the human immune system. The immune system is robust, decentralised, error tolerant, and adaptive. Unlike neural networks or genetic algorithms, AIS encompasses a SPECTRUM of algorithms because different algorithms implement different properties of different cells (B-cells, T-cells, dendritic cells).

Two generations: 1st gen (simplified models: negative selection, clonal selection, immune networks), 2nd gen (deeper immunology: Danger Theory, dendritic cell algorithms).

## The 3 First-Generation Algorithms

### 1. Negative Selection

**Biological basis:** T-cells that react to self-proteins are destroyed during maturation in the thymus. Only T-cells that DON'T react to self survive. The system learns what is SELF and rejects everything else.

**Algorithm:**
1. Generate random detector set
2. Remove detectors that match any "self" pattern (censoring)
3. Remaining detectors monitor for "non-self" (anomalies)

**Applications:** Intrusion detection, anomaly detection, fault detection.

**Key property:** Learns by EXCLUSION, not inclusion. Doesn't model what attacks look like — models what NORMAL looks like and flags everything else.

**Limitation:** "Considerable limitations when applied to realistic applications" — scalability issues, high false positive rates in high-dimensional spaces.

### 2. Clonal Selection (CLONALG)

**Biological basis:** When a B-cell's antibody binds to an antigen (pathogen), that B-cell is CLONED. Clones undergo somatic hypermutation (random mutations). Clones with HIGHER binding affinity are selected and amplified. Lower affinity clones die. This is Darwinian selection at the cellular level.

**Algorithm (CLONALG — de Castro & Von Zuben, 2002):**
1. Initialize population of antibodies (candidate solutions)
2. For each antigen (problem instance): select antibodies with highest affinity
3. Clone selected antibodies (more clones for higher affinity)
4. Mutate clones (mutation rate INVERSELY proportional to affinity — good solutions mutate less)
5. Select best mutated clones to replace worst in population
6. Repeat

**Key property: Credit assignment via amplification.** The system doesn't ATTRIBUTE credit ("this antibody caused the pathogen's elimination"). It AMPLIFIES what worked and lets what didn't work die. Credit assignment emerges from selection pressure, not explicit attribution.

**Affinity maturation:** Over generations, average antibody affinity INCREASES for the specific antigen. The population converges toward good solutions without any central coordinator knowing which solution is "best."

**Applications:** Optimization, pattern recognition, multi-modal function optimization (can find multiple optima simultaneously because different clones explore different regions).

### 3. Immune Network Theory (Jerne, 1974)

**Biological basis:** Antibodies don't just interact with antigens — they interact with EACH OTHER. An antibody's binding site can be recognized by another antibody's binding site (idiotypic interactions). This creates a regulatory network where antibodies stimulate and suppress each other.

**Algorithm (aiNet — de Castro & Von Zuben, 2002):**
1. Based on CLONALG + network interactions
2. After clonal selection: compute affinity between ALL antibodies
3. Suppress antibodies that are too similar (network suppression)
4. This maintains DIVERSITY — prevents convergence to single solution

**Key property: Distributed memory without central repository.** Each node is simultaneously detector AND regulator. Memory is stored in the STRUCTURE of the network, not in a central database. The network is its own memory.

**Applications:** Data clustering, data compression, multi-modal optimization.

**Connection to knowledge graphs:** The immune network is a SELF-REGULATING GRAPH where nodes (antibodies) and edges (affinity interactions) evolve together. Adding a new node changes the activation of existing nodes. Removing a node changes the network's behavior. This is structurally similar to a knowledge graph with typed, weighted edges — but the weights are emergent from interaction, not assigned.

## Credit Assignment: How the Immune System Solves It

The immune system solves credit assignment WITHOUT solving it:

1. **No explicit attribution:** The system never asks "which antibody killed the pathogen?" It asks "which antibodies are binding well?" and amplifies those.

2. **Selection replaces attribution:** Instead of crediting the right antibody, the system creates MORE of what seems to work. If it works, the population shifts toward it. If it doesn't, the clones die.

3. **Feedback is sparse and delayed:** Binding affinity is a noisy signal. The pathogen may be eliminated by the collective action of many antibodies. No single antibody gets "credit."

4. **The population IS the memory:** After infection, high-affinity B-cells persist as memory cells. The "credit" is literally survival — the good antibodies are the ones that are still alive.

**The key insight for knowledge graphs:** RWKG asks "which edge caused the retrieval failure?" and tries to modify that edge's weight. The immune system would ask "which retrievals worked?" and amplify those paths. It WOULDN'T try to identify the failing edge — it would strengthen successful alternatives until the failing path becomes irrelevant by competition.

## Relevance: AIS Applied to Knowledge Graphs

**What HAS been done:** AIS applied to optimization, clustering, anomaly detection, intrusion detection, robotics. The algorithms are well-established.

**What has NOT been done (as far as this survey covers):** AIS applied to knowledge graph retrieval, agent memory, or experience-weighted graph adaptation. The web search for "artificial immune system" + "knowledge graph" OR "credit assignment" returned zero direct results.

**The gap is real:** The immune system's approach to credit assignment (amplification, not attribution) has been formalized as algorithms (CLONALG, aiNet) but never applied to the specific problem RWKG identifies (which graph edge caused retrieval failure). This is a genuine unexplored intersection — not a recombination of existing work.

**Pearl classification:**
- AIS algorithms are Level 2 (intervention): CLONALG does do(mutate, select) and measures affinity change
- The claim "AIS would solve RWKG's credit assignment" is Level 1 (association): structural similarity between immune networks and knowledge graphs. No one has tested do(apply-AIS-to-KG)
- Testing it would be Level 2: implement CLONALG-style selection on KG edges, measure retrieval improvement
