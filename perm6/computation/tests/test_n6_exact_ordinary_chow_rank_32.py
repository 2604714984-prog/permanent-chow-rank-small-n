from __future__ import annotations

import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "n6_exact_ordinary_chow_rank_32.py"
FROZEN = ROOT / "data" / "n6_exact_ordinary_chow_rank_32.json"


def load_module():
    spec = importlib.util.spec_from_file_location("n6_exact_rank32", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load_module()


class N6ExactOrdinaryChowRank32Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = AUDIT.build_payload()
        cls.frozen = json.loads(FROZEN.read_text(encoding="utf-8"))

    def test_frozen_payload(self) -> None:
        self.assertEqual(self.payload, self.frozen)

    def test_every_half_defect_row_dominates_ten_thirds(self) -> None:
        for encoded in self.payload["half_defect_rows"].values():
            row = tuple(Fraction(value) for value in encoded)
            self.assertTrue(AUDIT.dominates_half_defect(row))

    def test_squarefree_symbol_table_is_derived_exactly(self) -> None:
        self.assertEqual(
            self.payload["squarefree_symbol_table"],
            [
                [0, 10, 16, 19, 20, 20, 20],
                [0, 9, 14, 16, 16, 20, 20],
                [0, 8, 12, 13, 16, 19, 20],
                [0, 7, 10, 10, 15, 17, 19],
            ],
        )
        self.assertEqual(
            self.payload["squarefree_symbol_audit"]["candidate_count"], 45696
        )

    def test_small_permanent_intersection_coordinate_maxima(self) -> None:
        self.assertEqual(
            self.payload["coordinate_intersection_audit"][
                "four_cycle_maxima_by_edge_count_0_to_6"
            ],
            [0, 0, 0, 0, 1, 1, 3],
        )

    def test_actual_span_five_derivative_profiles(self) -> None:
        profiles = {
            row["support"]: row for row in self.payload["span_five_normal_forms"]
        }
        self.assertEqual(
            [
                (
                    profiles[support]["quadratic_derivative_rank"],
                    profiles[support]["middle_derivative_rank"],
                )
                for support in range(1, 6)
            ],
            [(11, 14), (11, 14), (13, 18), (14, 20), (15, 20)],
        )
        self.assertEqual(
            profiles[3]["contained_squarefree_directional_rank_floor"], 5
        )
        self.assertEqual(
            profiles[4]["contained_squarefree_directional_rank_floor"], 6
        )
        self.assertEqual(
            profiles[5]["contained_squarefree_directional_rank_floor"], 6
        )

    def test_rejected_formal_actual_shortcut_stays_rejected(self) -> None:
        profiles = {
            row["support"]: row for row in self.payload["span_five_normal_forms"]
        }
        self.assertFalse(profiles[2]["formal_pair_equals_actual_derivative_space"])
        self.assertFalse(profiles[2]["formal_triple_equals_actual_derivative_space"])
        self.assertFalse(profiles[3]["formal_triple_equals_actual_derivative_space"])

    def test_repaired_rows_are_derived_from_actual_profiles(self) -> None:
        rows = self.payload["span_five_derived_half_defect_rows"]
        self.assertEqual(rows["1"], ["3", "9", "9", "10", "16", "17"])
        self.assertEqual(rows["2"], rows["1"])
        self.assertEqual(rows["3"], ["1", "5", "7", "12", "14", "19"])
        self.assertEqual(rows["4"], ["0", "5", "8", "13", "15", "20"])
        self.assertEqual(rows["5"], rows["4"])

    def test_defect_cancels_and_first_feasible_term_count_is_32(self) -> None:
        self.assertEqual(self.payload["minimum_n"], 32)
        self.assertEqual(self.payload["n31_gap"], 10)
        self.assertEqual(self.payload["n32_gap"], 0)

    def test_claim_boundary_is_ordinary_only(self) -> None:
        self.assertIn("not border rank", self.payload["scope"])
        self.assertEqual(
            self.payload["status"], "EXACT_THEOREM_FINITE_REPLAY"
        )
        self.assertEqual(self.payload["conclusion"], "ChowRank(perm_6) = 32")


if __name__ == "__main__":
    unittest.main()
