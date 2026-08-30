# Tolerance Calculator

A small, general-purpose engineering tolerance stack-up calculator for worst-case gap/overlap analysis, sensitivity ranking, and Current-vs-Alternative comparison.

[한국어 README](README_KO.md)

## Why

Tolerance reviews often start in spreadsheets and quickly become difficult to audit when dimensions, signs, and alternatives change. Tolerance Calculator keeps the core calculation model explicit and reproducible:

- nominal dimensions with asymmetric `+ / -` tolerance
- signed chain coefficients
- worst-case minimum / maximum
- gap / overlap classification
- sensitivity contribution by dimension
- Current vs Alternative comparison
- JSON input/output for scripting or AI workflows

This public version is intentionally generic and contains no company, customer, product, or production data.

## Quick start

Requires Python 3.10+ and uses only the standard library at runtime.

```bash
python -m tolcalc examples/basic.json
```

Example input:

```json
{
  "dimensions": [
    {"id": "housing", "nominal": 20.0, "plus": 0.2, "minus": 0.1},
    {"id": "insert", "nominal": 19.6, "plus": 0.1, "minus": 0.1}
  ],
  "chain": [
    {"dimension_id": "housing", "coefficient": 1},
    {"dimension_id": "insert", "coefficient": -1}
  ]
}
```

The signed result is interpreted as clearance:

- positive interval: `GAP_ONLY`
- negative interval: `OVERLAP_ONLY`
- crosses zero: `GAP_OR_OVERLAP`

## Current vs Alternative

```bash
python -m tolcalc examples/current.json --alternative examples/alternative.json
```

The comparison reports changes in nominal, minimum, maximum, span, classification, and whether an overlap/gap risk was removed.

## Python API

```python
from tolcalc import Dimension, ChainTerm, analyze_chain

dimensions = {
    "A": Dimension("A", nominal=10.0, plus=0.2, minus=0.1),
    "B": Dimension("B", nominal=9.7, plus=0.1, minus=0.1),
}

result = analyze_chain(
    dimensions,
    [ChainTerm("A", 1), ChainTerm("B", -1)],
)

print(result.to_dict())
```

## Sensitivity

For a pure worst-case stack, each dimension's contribution is calculated from:

`abs(coefficient) × total tolerance span`

and normalized as a percentage of the total stack span. This is not a statistical process capability model; it is a simple way to show which tolerances dominate the worst-case window.

## Repository structure

```text
tolcalc/          calculation engine and CLI
tests/            regression tests
examples/         synthetic input examples
docs/             design notes
.github/workflows automated tests
```

## Test

```bash
python -m unittest discover -s tests -v
```

CI runs the same tests across supported Python versions.

## Scope

### Included in v0.1

- asymmetric tolerances
- positive and negative chain coefficients
- worst-case stack analysis
- gap/overlap classification
- dimension sensitivity ranking
- Current/Alternative comparison
- JSON CLI

### Not yet included

- RSS / statistical tolerance analysis
- Monte Carlo simulation
- GD&T feature relationships
- unit conversion
- Excel import/export
- revision database
- graphical stack editor
- AI recommendation layer

These are possible extensions, not claims about the current implementation.

## Design principles

- **Transparent math** — every result comes from explicit dimensions and coefficients.
- **Deterministic first** — calculation does not depend on an LLM.
- **AI-friendly interface** — JSON makes the engine easy to call from AI or automation systems.
- **Generic public data** — examples are synthetic and reusable outside any specific company or product.

## Background

This public implementation grew out of experiments in using software and AI to make engineering tolerance reviews easier to repeat, compare, and audit. The public repository focuses on the reusable calculation core rather than any company-specific workflow or data.
