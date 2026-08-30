import unittest

from tolcalc import ChainTerm, Dimension, analyze_chain, compare_results


class TolCalcEngineTests(unittest.TestCase):
    def test_asymmetric_worst_case(self):
        dims = {
            "A": Dimension("A", 10.0, plus=0.3, minus=0.1),
            "B": Dimension("B", 4.0, plus=0.2, minus=0.4),
        }
        result = analyze_chain(
            dims,
            [ChainTerm("A", 1), ChainTerm("B", -1)],
        )

        self.assertAlmostEqual(result.nominal, 6.0)
        self.assertAlmostEqual(result.minimum, 5.7)
        self.assertAlmostEqual(result.maximum, 6.7)
        self.assertEqual(result.classification, "GAP_ONLY")

    def test_overlap_possible(self):
        dims = {
            "opening": Dimension("opening", 10.0, plus=0.1, minus=0.3),
            "part": Dimension("part", 10.0, plus=0.2, minus=0.1),
        }
        result = analyze_chain(
            dims,
            [ChainTerm("opening", 1), ChainTerm("part", -1)],
        )
        self.assertLess(result.minimum, 0)
        self.assertGreater(result.maximum, 0)
        self.assertEqual(result.classification, "GAP_OR_OVERLAP")

    def test_sensitivity_ranks_largest_span_first(self):
        dims = {
            "A": Dimension("A", 10, plus=0.5, minus=0.5),
            "B": Dimension("B", 5, plus=0.1, minus=0.1),
        }
        result = analyze_chain(dims, [ChainTerm("A"), ChainTerm("B", -1)])
        self.assertEqual(result.sensitivity[0][0], "A")
        self.assertGreater(result.sensitivity[0][2], result.sensitivity[1][2])

    def test_current_alt_comparison_detects_removed_overlap(self):
        dims = {
            "opening": Dimension("opening", 10.0, plus=0.0, minus=0.2),
            "part": Dimension("part", 10.0, plus=0.1, minus=0.0),
        }
        current = analyze_chain(dims, [ChainTerm("opening"), ChainTerm("part", -1)])

        alt_dims = dict(dims)
        alt_dims["opening"] = Dimension("opening", 10.5, plus=0.0, minus=0.2)
        alternative = analyze_chain(
            alt_dims, [ChainTerm("opening"), ChainTerm("part", -1)]
        )
        comparison = compare_results(current, alternative)
        self.assertTrue(comparison["overlap_risk_removed"])

    def test_rejects_unknown_dimension(self):
        with self.assertRaises(KeyError):
            analyze_chain({}, [ChainTerm("missing")])


if __name__ == "__main__":
    unittest.main()
