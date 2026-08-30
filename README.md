# TolCalc

**Engineering tolerance stack-up analysis for worst-case gap/overlap, sensitivity, and design comparison.**

[한국어 README](README_KO.md)

TolCalc is an experiment in turning tolerance analysis from a one-off calculation into a repeatable engineering review workflow.

The public `v0.1` release starts with the deterministic core: define dimensions and asymmetric tolerances, compose a signed chain, calculate worst-case bounds, identify the dimensions driving the stack, and compare a current design against an alternative.

> This public version contains only generalized logic and synthetic examples. No company-specific dimensions, products, customer data, internal reference tables, or proprietary workflow data are included.

## Why

A tolerance stack result is useful, but the engineering question is usually larger:

1. Can interference occur?
2. Which dimension contributes most to the risk?
3. What changes if a nominal dimension or tolerance is adjusted?
4. Did the alternative actually remove the problem?
5. Can the reasoning be reproduced later?

TolCalc is designed around that review loop rather than around a single calculator screen.

## Current features

- Asymmetric `+/-` tolerances
- Signed tolerance chains with arbitrary non-zero coefficients
- Worst-case `minimum / nominal / maximum`
- Gap / overlap-interference classification
- Sensitivity ranking by worst-case span contribution
- Current vs. alternative design comparison
- JSON input/output for automation
- Python standard-library calculation core
- Unit tests and CI

## Quick start

Requires Python 3.10+.

```bash
python -m pip install -e .
tolcalc examples/basic_case.json --pretty
```

Or without installation:

```bash
python -m tolcalc.cli examples/basic_case.json --pretty
```

## Example input

```json
{
  "dimensions": [
    {"id": "opening", "nominal": 100.0, "plus": 0.4, "minus": 0.6},
    {"id": "part", "nominal": 99.8, "plus": 0.5, "minus": 0.3}
  ],
  "chain": [
    {"dimension_id": "opening", "coefficient": 1},
    {"dimension_id": "part", "coefficient": -1}
  ],
  "alternative_dimensions": [
    {"id": "opening", "nominal": 101.0, "plus": 0.4, "minus": 0.6}
  ]
}
```

For a signed clearance chain, positive output means **gap** and negative output means **overlap/interference**.

## Core calculation

For each dimension:

```text
low  = nominal - minus_tolerance
high = nominal + plus_tolerance
```

Each chain term applies its coefficient to that interval. TolCalc selects the lower and upper contribution correctly even when the coefficient is negative, then sums all contributions into the worst-case interval.

Sensitivity is based on each dimension's contribution to total worst-case span:

```text
abs(coefficient) × (plus_tolerance + minus_tolerance)
```

This deliberately keeps the core deterministic and auditable.

## Design philosophy

**Calculation first, AI second.**

The tolerance engine should remain deterministic and independently testable. Higher-level features such as historical case retrieval, design suggestions, or AI-generated review notes should sit on top of verified calculation results rather than replace them.

See [ROADMAP.md](docs/ROADMAP.md) for the planned review-workflow and optional AI layers.

## Tests

```bash
python -m unittest discover -s tests -v
```

The initial public release includes tests for asymmetric tolerances, negative chain terms, mixed gap/overlap ranges, sensitivity ranking, alternative-design comparison, and invalid references.

## Status

`v0.1.0` — generalized public core.

The broader concept includes scenario coverage checks, revision/decision history, measured-value comparison, reusable case knowledge, and optional AI-assisted design review. Those are intentionally separated from the first public core so each layer can be tested independently.

## Author

**Valon Jang** — Packaging & Product Development Engineer based in South Korea 🇰🇷

I build and test new ways for AI and software to work on real engineering problems.
