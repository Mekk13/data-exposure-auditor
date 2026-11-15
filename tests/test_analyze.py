import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from auditor.analyze import (breakdown, confusion, f1, main, per_category_metrics, precision, recall,
                             sensitive_share, wilson)


def result(doc_id, label, pre_gdpr="1", institution_type="school", city_size="small", **flags):
    row = {"doc_id": doc_id, "institution_type": institution_type, "city_size": city_size,
           "pre_gdpr": pre_gdpr, "label": label}
    for category in ["cnp", "health", "names", "email", "phone", "birthdate"]:
        row[category] = flags.get(category, "0")
    return row


def truth(doc_id, **flags):
    row = {"doc_id": doc_id}
    for category in ["cnp", "health", "names", "email", "phone", "birthdate"]:
        row[category] = flags.get(category, "0")
    return row


class TestConfusion(unittest.TestCase):
    def test_counts(self):
        actual = [True, True, False, False, True]
        guess = [True, False, True, False, True]
        self.assertEqual(confusion(actual, guess), (2, 1, 1, 1))

    def test_empty(self):
        self.assertEqual(confusion([], []), (0, 0, 0, 0))


class TestScores(unittest.TestCase):
    def test_precision_recall_f1(self):
        self.assertAlmostEqual(precision(3, 1), 0.75)
        self.assertAlmostEqual(recall(3, 3), 0.5)
        self.assertAlmostEqual(f1(0.75, 0.5), 0.6)

    def test_zero_division(self):
        self.assertEqual(precision(0, 0), 0.0)
        self.assertEqual(recall(0, 0), 0.0)
        self.assertEqual(f1(0.0, 0.0), 0.0)


class TestWilson(unittest.TestCase):
    def test_half(self):
        low, high = wilson(50, 100)
        self.assertAlmostEqual(low, 0.404, places=3)
        self.assertAlmostEqual(high, 0.596, places=3)

    def test_empty(self):
        self.assertEqual(wilson(0, 0), (0.0, 0.0))

    def test_all_successes_stays_below_one(self):
        low, high = wilson(10, 10)
        self.assertLess(low, 1.0)
        self.assertAlmostEqual(high, 1.0)


class TestMetrics(unittest.TestCase):
    def test_per_category(self):
        truth_rows = [truth("A", cnp="1", names="1"), truth("B", names="1"), truth("C", health="1")]
        result_rows = [result("C", "ordinary", names="1"), result("A", "sensitive", cnp="1", names="1"),
                       result("B", "sensitive", cnp="1")]
        table = {row["category"]: row for row in per_category_metrics(truth_rows, result_rows)}
        self.assertEqual((table["cnp"]["tp"], table["cnp"]["fp"], table["cnp"]["fn"]), (1, 1, 0))
        self.assertAlmostEqual(table["cnp"]["precision"], 0.5)
        self.assertEqual((table["names"]["tp"], table["names"]["fp"], table["names"]["fn"]), (1, 1, 1))
        self.assertEqual((table["health"]["tp"], table["health"]["fn"]), (0, 1))
        self.assertEqual(table["health"]["precision"], 0.0)
        self.assertEqual((table["sensitive"]["tp"], table["sensitive"]["fp"], table["sensitive"]["fn"]), (1, 1, 1))


class TestShare(unittest.TestCase):
    def setUp(self):
        self.rows = [
            result("1", "sensitive", institution_type="school", city_size="small"),
            result("2", "ordinary", institution_type="school", city_size="large"),
            result("3", "sensitive", institution_type="hospital", city_size="large"),
            result("4", "none", institution_type="hospital", city_size="large"),
            result("5", "sensitive", pre_gdpr="0", institution_type="hospital", city_size="small"),
        ]

    def test_pre_gdpr_only(self):
        share = sensitive_share(self.rows)
        self.assertEqual((share["sensitive"], share["total"]), (2, 3))
        self.assertAlmostEqual(share["share"], 2 / 3)

    def test_all_years(self):
        share = sensitive_share(self.rows, pre_gdpr_only=False)
        self.assertEqual((share["sensitive"], share["total"]), (3, 4))

    def test_no_documents(self):
        share = sensitive_share([])
        self.assertEqual((share["total"], share["share"]), (0, 0.0))

    def test_breakdown_by_type(self):
        groups = breakdown(self.rows, "institution_type")
        self.assertEqual(list(groups), ["hospital", "school"])
        self.assertEqual((groups["hospital"]["sensitive"], groups["hospital"]["total"]), (1, 1))
        self.assertEqual((groups["school"]["sensitive"], groups["school"]["total"]), (1, 2))

    def test_breakdown_by_size(self):
        groups = breakdown(self.rows, "city_size")
        self.assertEqual((groups["large"]["sensitive"], groups["large"]["total"]), (1, 2))
        self.assertEqual((groups["small"]["sensitive"], groups["small"]["total"]), (1, 1))


class TestMain(unittest.TestCase):
    def test_writes_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / "truth.csv").write_text("doc_id,cnp,health,names,email,phone,birthdate\nA,1,0,1,0,0,0\n",
                                              encoding="utf-8")
            (folder / "results.csv").write_text(
                "doc_id,site_id,institution_type,city_size,published,pre_gdpr,cnp,health,names,email,phone,birthdate,label\n"
                "A,S,school,small,2015-01-01,1,1,0,1,0,0,0,sensitive\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                main(folder / "truth.csv", folder / "results.csv", folder / "summary.md")
            content = (folder / "summary.md").read_text(encoding="utf-8")
        self.assertIn("## Detector metrics", content)
        self.assertIn("## By institution type", content)
        self.assertIn("## By city size", content)
        self.assertIn("| all | 1 | 1 | 100.0% |", content)
