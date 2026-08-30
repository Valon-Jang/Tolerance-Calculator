from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import ChainTerm, Dimension, analyze_chain, compare_results


def _load_dimensions(items: list[dict]) -> dict[str, Dimension]:
    dimensions = {}
    for item in items:
        dim = Dimension(
            id=str(item["id"]),
            nominal=float(item["nominal"]),
            plus=float(item.get("plus", 0.0)),
            minus=float(item.get("minus", 0.0)),
        )
        if dim.id in dimensions:
            raise ValueError(f"duplicate dimension id: {dim.id}")
        dimensions[dim.id] = dim
    return dimensions


def _load_terms(items: list[dict]) -> list[ChainTerm]:
    return [
        ChainTerm(
            dimension_id=str(item["dimension_id"]),
            coefficient=float(item.get("coefficient", 1.0)),
        )
        for item in items
    ]


def _analyze_case(case: dict) -> dict:
    dimensions = _load_dimensions(case["dimensions"])
    terms = _load_terms(case["chain"])
    current = analyze_chain(dimensions, terms)

    output = {"result": current.to_dict()}

    if "alternative_dimensions" in case:
        alt_dimensions = dict(dimensions)
        for item in case["alternative_dimensions"]:
            dim = Dimension(
                id=str(item["id"]),
                nominal=float(item["nominal"]),
                plus=float(item.get("plus", 0.0)),
                minus=float(item.get("minus", 0.0)),
            )
            alt_dimensions[dim.id] = dim
        alternative = analyze_chain(alt_dimensions, terms)
        output["comparison"] = compare_results(current, alternative)

    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="tolerance-calculator",
        description="Deterministic worst-case tolerance stack-up analysis.",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to a Tolerance Calculator JSON case",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    case = json.loads(args.input.read_text(encoding="utf-8"))
    result = _analyze_case(case)
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
