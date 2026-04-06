# AI as Coordination-Compressing Capital: Task Reallocation, Organizational Redesign, and the Regime Fork

**Author:** Alex Farach
**arXiv:** 2602.16078
**Submitted:** 2026-02-17 | **Revised:** 2026-03-06
**Category:** Economics (econ.GN)
**URL:** https://arxiv.org/abs/2602.16078

---

## Abstract (paraphrased)

Introduces "agent capital" (K_A) — AI that reduces coordination costs within organizations, changing organizational structure itself rather than just task composition. Coordination compression expands spans of control and enables endogenous task creation. Five propositions characterize distributional outcomes. Central finding: identical technology produces either broad-based gains or superstar concentration depending on who benefits from coordination compression ("regime fork"). Economy-wide inequality falls in all regimes via employment expansion; manager-worker wage gap widens universally.

---

## Key Definitions

**Agent capital (K_A):** A distinct production input that reduces coordination friction c(K_A) within organizations. Distinguished from task-level AI (which affects what workers do) — agent capital changes organizational structure itself.

**Coordination friction:** c_i(K_A) = c_0 / [1 + γ · K_A · s_i^β]
- c_0: baseline friction
- γ: coordination compression effectiveness  
- s_i: manager skill
- β: elite complementarity exponent (KEY PARAMETER — determines regime)

**Span of control:** S_i(K_A) = 1/c_i(K_A) — strictly increases in K_A

---

## Five Formal Propositions

**P1 — Output Effect:** ∂Y/∂K_A > 0 for any γ > 0. Output strictly increases with agent capital.

**P2 — Span Expansion:** Each manager's coordination capacity S_i(K_A) strictly increases in K_A. High-skill managers experience accelerating gains when β > 0.

**P3 — Manager Demand:** When c_0 < 1, managers required to supervise N workers strictly decreases as K_A rises.

**P4 — Wage Dispersion:** Under proportional worker allocation with β > 0, the Gini coefficient of managerial wages strictly increases in K_A, with rates accelerating in β.

**P5 — Task Frontier Expansion:** When δ > 0, the task frontier T(K_A) strictly increases → total employment E(K_A) weakly increasing.

---

## The Regime Fork

Critical parameter: **β** (elite complementarity exponent). Each manager's effective agent capital = K_A · s_i^β.

- **Low β (≈0.2):** Coordination compression acts as "general infrastructure" — benefits distributed broadly (concave mapping compresses skill differences)
- **High β (≈3.0):** "Elite complementarity" — only top-skill managers extract substantial capacity gains (convex mapping amplifies skill differences)

**2×2 Taxonomy (β × δ):**

| | Low δ (low task creation) | High δ (high task creation) |
|---|---|---|
| **Low β** | Gentle Compression — flat inequality, modest gains | Rising Tide — broad gains, inequality contained |
| **High β** | Winner Takes All — superstar concentration | Creative Destruction — volatile, expansion + concentration |

---

## Empirical Validation

Simulation only: 20-manager newsroom, 400 heterogeneous workers. No causal econometric testing.

**External reference:** Ewens and Giroud (2025) documented hierarchy flattening post-AI adoption — cited in support of Propositions 2-3, but not the authors' own data.

---

## Theoretical Lineage

- Extends **Garicano (2000)** knowledge hierarchy framework (parameterizes coordination costs with team size)
- Standard result: "large teams face diminishing returns from coordination losses" (Bolton-Dewatripont 1994)
- Innovation: makes coordination friction itself a function of AI capability

---

## Limitations (author-acknowledged)

1. Production function stylization: fixed factor shares (α, 1-α) via Cobb-Douglas
2. No general equilibrium: single-firm partial equilibrium
3. Exogenous skills: worker/manager skills fixed
4. β parameter collapse: conflates pre-existing inequality with AI complementarity
5. Simulations only: "calibration to specific industries requires richer data than currently available"

---

## Falsifiable Claims

1. Span expansion: ∂S_i/∂K_A > 0 — measurable via org charts post-AI adoption
2. Manager reduction: firms adopting coordination AI reduce management headcount (Ewens & Giroud 2025 supports)
3. Differential gains by skill: high-skill managers' spans expand faster than average (testable via HR data)
4. Task frontier effects: new job creation via occupational data
