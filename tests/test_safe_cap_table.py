"""Run: python3 -m unittest discover -s tests"""
import pathlib, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cap-table"))
from safe_cap_table import load, solve  # noqa: E402


def table(rows):
    return dict(rows)


class YCExample1(unittest.TestCase):
    """Y Combinator Post-Money SAFE User Guide, Example 1."""

    def setUp(self):
        self.r = solve(load(ROOT / "cap-table/examples/yc-example-1.json"))

    def test_company_capitalization(self):
        self.assertEqual(self.r["company_capitalization"], 11_764_705)

    def test_safe_prices(self):
        self.assertAlmostEqual(self.r["safe_prices"]["Investor A"], 0.34, places=4)
        self.assertAlmostEqual(self.r["safe_prices"]["Investor B"], 0.68, places=4)

    def test_after_round(self):
        t = table(self.r["after_round"])
        self.assertEqual(t["Investor A (SAFE, cap)"], 588_235)
        self.assertEqual(t["Investor B (SAFE, cap)"], 1_176_470)
        self.assertEqual(t["New investors (priced round)"], 4_486_425)
        total = sum(t.values())
        self.assertEqual(total, 17_945_700)
        self.assertAlmostEqual(t["Founders"] / total, 0.5154, places=4)
        self.assertAlmostEqual(t["New investors (priced round)"] / total, 0.25, places=4)
        self.assertAlmostEqual(t["Unissued option pool (old + increase)"] / total, 0.10, places=4)


class TwoSafesSeriesA(unittest.TestCase):
    def test_numbers(self):
        r = solve(load(ROOT / "cap-table/examples/two-safes-series-a.json"))
        self.assertEqual(r["company_capitalization"], 12_500_000)
        self.assertAlmostEqual(r["round_price"], 1.2174, places=4)
        t = table(r["after_round"])
        self.assertEqual(sum(t.values()), 16_428_571)


class SafesOnly(unittest.TestCase):
    def test_ownership_is_amount_over_cap(self):
        r = solve(load(ROOT / "cap-table/examples/safes-only.json"))
        t = table(r["before_round"])
        total = sum(t.values())
        self.assertAlmostEqual(t["Angel (SAFE, cap)"] / total, 250_000 / 6_000_000, places=4)
        self.assertAlmostEqual(t["Pre-seed fund (SAFE, cap)"] / total, 0.075, places=4)


class EdgeCases(unittest.TestCase):
    def test_cap_above_round_converts_at_round_price(self):
        r = solve(load(ROOT / "cap-table/examples/cap-above-round.json"))
        self.assertEqual(r["conversion"]["High-cap SAFE"], "round price")
        self.assertEqual(r["conversion"]["Discount SAFE"], "discount")
        t = table(r["after_round"])
        self.assertAlmostEqual(t["New investors (priced round)"] / sum(t.values()), 0.20, places=4)

    def test_overselling_raises(self):
        from safe_cap_table import Inputs, Safe
        with self.assertRaises(ValueError):
            solve(Inputs(holders={"F": 1_000_000}, unissued_pool=0,
                         safes=[Safe("X", 5_000_000, 5_000_000)]))


if __name__ == "__main__":
    unittest.main()
