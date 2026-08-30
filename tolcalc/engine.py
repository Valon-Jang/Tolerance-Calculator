from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Dimension:
    """A nominal dimension with asymmetric plus/minus tolerances."""

    id: str
    nominal: float
    plus: float = 0.0
    minus: float = 0.0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("dimension id must not be empty")
        if self.plus < 0 or self.minus < 0:
            raise ValueError("plus/minus tolerances must be non-negative")

    @property
    def low(self) -> float:
        return self.nominal - self.minus

    @property
    def high(self) -> float:
        return self.nominal + self.plus

    @property
    def span(self) -> float:
        return self.plus + self.minus


@dataclass(frozen=True)
class ChainTerm:
    dimension_id: str
    coefficient: float = 1.0

    def __post_init__(self) -> None:
        if not self.dimension_id:
            raise ValueError("dimension_id must not be empty")
        if self.coefficient == 0:
            raise ValueError("coefficient must be non-zero")


@dataclass(frozen=True)
class ChainResult:
    nominal: float
    minimum: float
    maximum: float
    classification: str
    sensitivity: tuple[tuple[str, float, float], ...]

    @property
    def span(self) -> float:
        return self.maximum - self.minimum

    def to_dict(self) -> dict:
        clean = lambda value: round(value, 12)
        return {
            "nominal": clean(self.nominal),
            "minimum": clean(self.minimum),
            "maximum": clean(self.maximum),
            "span": clean(self.span),
            "classification": self.classification,
            "sensitivity": [
                {
                    "dimension_id": dim_id,
                    "worst_case_span_contribution": clean(contribution),
                    "share_percent": clean(share_percent),
                }
                for dim_id, contribution, share_percent in self.sensitivity
            ],
        }


def classify_gap_overlap(minimum: float, maximum: float) -> str:
    """Classify a signed clearance interval.

    Positive values represent gap, negative values represent overlap/interference.
    """

    if minimum >= 0:
        return "GAP_ONLY"
    if maximum <= 0:
        return "OVERLAP_ONLY"
    return "GAP_OR_OVERLAP"


def analyze_chain(
    dimensions: Mapping[str, Dimension],
    terms: Iterable[ChainTerm],
) -> ChainResult:
    nominal = 0.0
    minimum = 0.0
    maximum = 0.0
    contributions: list[tuple[str, float]] = []

    materialized_terms = tuple(terms)
    if not materialized_terms:
        raise ValueError("chain must contain at least one term")

    for term in materialized_terms:
        try:
            dim = dimensions[term.dimension_id]
        except KeyError as exc:
            raise KeyError(f"unknown dimension: {term.dimension_id}") from exc

        c = term.coefficient
        nominal += c * dim.nominal

        low_contribution = c * dim.low
        high_contribution = c * dim.high
        minimum += min(low_contribution, high_contribution)
        maximum += max(low_contribution, high_contribution)

        contributions.append((dim.id, abs(c) * dim.span))

    total_span = sum(value for _, value in contributions)
    ranked = [
        (
            dim_id,
            contribution,
            0.0 if total_span == 0 else contribution / total_span * 100.0,
        )
        for dim_id, contribution in contributions
    ]
    sensitivity = tuple(sorted(ranked, key=lambda item: item[1], reverse=True))

    return ChainResult(
        nominal=nominal,
        minimum=minimum,
        maximum=maximum,
        classification=classify_gap_overlap(minimum, maximum),
        sensitivity=sensitivity,
    )


def compare_results(current: ChainResult, alternative: ChainResult) -> dict:
    """Return a compact Current-vs-Alt comparison."""

    return {
        "current": current.to_dict(),
        "alternative": alternative.to_dict(),
        "delta": {
            "nominal": alternative.nominal - current.nominal,
            "minimum": alternative.minimum - current.minimum,
            "maximum": alternative.maximum - current.maximum,
            "span": alternative.span - current.span,
        },
        "overlap_risk_removed": current.minimum < 0 <= alternative.minimum,
        "gap_risk_removed": current.maximum > 0 >= alternative.maximum,
        "classification_changed": current.classification != alternative.classification,
    }
