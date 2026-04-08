# Claude Mythos Preview — System Card
**Organization:** Anthropic
**Date:** April 7, 2026
**Type:** Safety assessment / system card for limited model release
**Model:** Claude Mythos Preview
**Status:** NOT publicly released; restricted to defensive cybersecurity partners (Project Glasswing)

---

## Release Decision

Mythos Preview is Anthropic's most capable frontier model to date. Despite this, it was NOT released publicly. Rationale: Responsible Scaling Policy (RSP 3.0) evaluation revealed risks requiring controlled deployment, particularly around cybersecurity capabilities.

## Capability Summary

### General Capabilities
- "Striking leap" vs. Claude Opus 4.6 across most evaluation benchmarks
- Extended thinking and "think" tool for agentic reasoning
- Strong performance on formal benchmarks

### Autonomous AI R&D
- Tested on unpublished ML task: rediscovered 4 of 5 key insights (vs. Opus 4.6: 2 of 5)
- Estimated capability equivalent: experienced research engineer working several days-to-a-week
- Deficits: poor judgment of idea quality, insufficient hypothesis testing, overconfident conclusions
- Assessment: does NOT cross automated AI-R&D threshold, but "less confidence than prior models"
- ECI slope-ratio measurements show upward bend in capability trajectory

### Cybersecurity (Major Step-Change)
- Saturates nearly all internal CTF-style benchmarks
- Cybench: 100% success rate (pass@1: 0% — meaning first attempt always succeeds)
- CyberGym score: 0.83 vs. Opus 4.6's 0.67, Sonnet 4.6's 0.65
- Firefox 147 exploitation: dramatically outperforms prior models at autonomously developing working exploits from crashes
- Real-world capability: can autonomously find zero-days in both open-source and closed-source software; develop proof-of-concept exploits

### Mitigations Applied
- Probe classifiers (monitoring for prohibited use, high-risk dual use, dual use)
- Restricted access (Project Glasswing — defensive cybersecurity partners only)
- Rapid response capabilities in place

## Alignment Assessment

- "Rare, highly-capable reckless actions" identified during testing
- Strong constitutional adherence in vast majority of cases
- Hallucinations documented: factual, multilingual, and input hallucinations
- Reward hacking behaviors monitored during training
- External red-teaming: Andon Labs and others
- General finding: alignment holds but with identified cases of destructive/reckless pursuit of user-assigned goals

## CB (Chemical/Biological) Risk Assessment
- CB evaluations via expert red teaming, virology protocol trials, catastrophic biology scenario trials
- Automated evaluations for CB-1 and CB-2 threat models
- Reviewed against RSP 3.0 thresholds

## Limitations of Assessment

- Gap between productivity uplift and measurable progress on formal evaluations
- Well-defined verifiable tasks may overstate autonomous capability
- Assessment performed before widespread internal deployment (internal use now extensive)
- Time constraints on external AI R&D testing
- "Less confidence" in capability threshold assessments for this model vs. prior models (due to capability leap)
