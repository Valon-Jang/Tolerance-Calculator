# Roadmap

TolCalc is intentionally split into a deterministic engineering core and optional higher-level workflow/AI layers.

## Public v0.1 — deterministic core

- [x] Asymmetric `+/-` tolerance input
- [x] Signed tolerance-chain composition
- [x] Worst-case minimum / nominal / maximum
- [x] Gap vs. overlap/interference classification
- [x] Dimension sensitivity ranking
- [x] Current vs. alternative design comparison
- [x] JSON CLI and synthetic example
- [x] Unit tests

## Next — engineering review workflow

- [ ] Multiple named scenarios per assembly
- [ ] Required-scenario coverage / missing-review checks
- [ ] Revision history and decision rationale
- [ ] Measured-value comparison
- [ ] CSV / Excel import-export adapters
- [ ] Human-readable review summary

## Later — optional AI layer

The AI layer should never replace the deterministic calculation core. It can operate on top of verified results to help with:

- Similar historical case retrieval
- Difference summarization
- Review-point suggestions
- Candidate tolerance/design alternatives
- Rationale-backed recommendations

Final engineering decisions remain with the engineer.
