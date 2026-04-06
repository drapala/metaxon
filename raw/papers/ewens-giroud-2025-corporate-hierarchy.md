# Corporate Hierarchy

**Authors:** Michael Ewens & Xavier Giroud (Columbia Business School, NBER, CEPR)
**Published:** NBER Working Paper 34162, October 2025
**URL:** http://www.columbia.edu/~xg2285/Hierarchy.pdf | SSRN 5391667

---

## Abstract (paraphrased)

Introduces a novel measure of corporate hierarchies for 3,128 U.S. public firms derived from LinkedIn resume data (7 million employees, 8.7 million job transitions 2017–2023) and network estimation technique. Documents facts about corporate hierarchies: firms average 9.5 layers (median 8), pyramidal structure. More hierarchical firms have better operating performance, higher admin costs, more patents, lower volatility. Firms flatten hierarchies following AI adoption; pharmaceutical firms added layers following Covid-19. Results consistent with knowledge hierarchy and information hierarchy models.

---

## Dataset & Methodology

- **Sample:** 3,128 U.S. public firms (Compustat 2015+, filtered by SIC coverage on LinkedIn)
- **Source:** CoreSignal LinkedIn resume data — 7M+ unique workers, 8.7M job transitions 2017–2023
- **Coverage:** LinkedIn covers 49% of Compustat headcount for median firm (biased toward managerial class and workers with public profiles)
- **Algorithm:** Huitfeldt, Kostøl, Nimczik & Weber (2023) Minimum Violation Ranking (MVR) — k-means clustering of job ranks inferred from promotion/lateral-move patterns
- **Key limitation:** Cross-sectional by design — only 18% of firms changed layers during 2016–2023; this occurred in only 3.9% of firm-years. When layers change, 75% of the time they increase (median: +1 layer).

---

## Key Descriptive Facts

- Average firm: **9.5 hierarchical layers** (median 8); exceeds prior literature (capped at 4 via occupation codes)
- Structure: **pyramidal** — more workers at bottom layers across all industries
- **Trend:** Layers have declined over sample period (Figure 1: average ~10.4 in 2015 → ~10.1 in 2023; median dropped from 9 to 8 around 2017)
- Industry variation: IT highest (~12+ layers), Chemicals/Drugs lowest (~5); within-industry variation larger than across-time variation
- Size → layers: strong positive relationship (R² > 70% in regressions); size does not fully explain hierarchy variation

---

## Firm Outcomes (Section 7 — correlational)

**Authors explicitly caution: results are correlational and do not warrant causal interpretation.**

More layers associated with:
- Higher ROA, gross profit margin, net profit margin (Section 7.2)
- Higher SG&A expenses (administrative costs) — cost of maintaining hierarchy
- More R&D investment and patents; no difference in patent quality (citations)
- More acquisitions (non-diversifying)
- Lower stock return volatility (lower business risk, not financial risk)
- Higher CEO compensation, higher CEO pay ratio (wage inequality)
- More educated workforce, higher internal promotion rates, longer tenure

---

## Determinants of Hierarchy (Section 8)

### 8.2 Covid Pandemic
- Pharmaceutical firms (SIC 2834) increased layers by ~4% post-Covid (demand + complexity shock)
- Difference-in-differences with firm and year fixed effects
- Pre-trend coefficients insignificant → supports parallel trends assumption

### 8.3 Artificial Intelligence (key finding)
- AI adoption measured via Babina, Fedyk, He & Hodson (2024) metrics: 4 variants based on AI job postings (broad/narrow) and AI skills
- **Result: Firms with higher AI adoption have fewer hierarchical layers**
- Significant at **10% level** across all 4 AI adoption metrics
- Tests are "**under-powered**" due to limited within-firm variation in layers
- Consistent with knowledge hierarchy theory: AI lowers cost of knowledge acquisition → reduces demand for "problem-solver" middle management layers
- Also consistent with information hierarchy: better information processing → less need for delegation layers

---

## Limitations (author-acknowledged)

1. **Correlational only** — causal identification requires exogenous variation in hierarchy; endogeneity of org structure makes this difficult
2. **Coverage bias** — LinkedIn tilts toward managerial class; <50% coverage for most firms
3. **Within-firm variation** — limited changes in layers during sample period; firm fixed effects reduce statistical power
4. **Single-country, large public firms** — U.S. publicly traded companies only; not generalizable to SMEs or other countries
5. **Self-reported data** — job titles on LinkedIn are user-submitted; consistency issues addressed by cleaning algorithm but not eliminated

---

## Relationship to Prior Work

- First comprehensive measure of corporate hierarchy for U.S. public firms (prior work: ~300 firms via Hewitt Associates surveys)
- Extends Garicano (2000) knowledge hierarchy model — empirical analog for all major theoretical predictions
- Confirms "flattening firm" documented by Rajan & Wulf (2006) and Guadalupe & Wulf (2010) at top of hierarchy, now across full hierarchy
- AI finding consistent with Bolton & Dewatripont (1994): lower communication costs → fewer layers
