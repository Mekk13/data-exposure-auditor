import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from auditor.classify import CATEGORIES
from auditor.run import COLUMNS, audit, main
from auditor.synthetic import generate, save

EXPECTED = ["doc_id", "site_id", "institution_type", "city_size", "published", "pre_gdpr"] + CATEGORIES + ["label"]


class TestRun(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.data = Path(self.folder.name) / "data"
        self.results = Path(self.folder.name) / "results" / "results.csv"
        self.rows = generate(n_sites_per_type=2, docs_per_site=4)
        save(self.rows, self.data)
        with redirect_stdout(io.StringIO()):
            main(self.data / "documents.csv", self.results)
        with open(self.results, newline="", encoding="utf-8") as file:
            self.output = list(csv.DictReader(file))

    def tearDown(self):
        self.folder.cleanup()

    def test_columns(self):
        self.assertEqual(COLUMNS, EXPECTED)
        self.assertEqual(list(self.output[0].keys()), EXPECTED)

    def test_no_text_column(self):
        self.assertNotIn("text", self.output[0])
        with open(self.results, encoding="utf-8") as file:
            content = file.read()
        self.assertNotIn("@example.ro", content)
        self.assertNotIn("CNP", content)

    def test_one_row_per_document(self):
        self.assertEqual(len(self.output), len(self.rows))
        self.assertEqual([row["doc_id"] for row in self.output], [row["doc_id"] for row in self.rows])

    def test_values_are_flags_and_labels(self):
        for row in self.output:
            for category in CATEGORIES:
                self.assertIn(row[category], {"0", "1"})
            self.assertIn(row["label"], {"sensitive", "ordinary", "none"})

    def test_audit_on_hand_made_document(self):
        document = {"doc_id": "X", "site_id": "S", "institution_type": "school", "city_size": "small",
                    "published": "2015-01-01", "pre_gdpr": "1", "text": "contact secretariat@example.ro"}
        result = audit([document])[0]
        self.assertEqual(result["email"], 1)
        self.assertEqual(result["label"], "ordinary")
        self.assertNotIn("text", result)
