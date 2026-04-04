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
