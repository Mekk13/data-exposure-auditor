import csv
import random
import tempfile
import unittest
from pathlib import Path

from auditor.classify import CATEGORIES
from auditor.detectors.cnp import CANDIDATE_PATTERN, is_valid_cnp
from auditor.synthetic import HEALTH_PHRASES, SURNAMES, generate, person_row, save, wrong_cnp

NONE_INSERTED = {category: False for category in CATEGORIES}


def has_valid_cnp(text: str) -> bool:
    return any(is_valid_cnp(match.group()) for match in CANDIDATE_PATTERN.finditer(text))


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.rows = generate()

    def test_same_seed_same_rows(self):
        self.assertEqual(generate(seed=7), generate(seed=7))

    def test_different_seed_different_rows(self):
        self.assertNotEqual(generate(seed=1), generate(seed=2))

    def test_size_and_ids(self):
        self.assertEqual(len(self.rows), 200)
        ids = [row["doc_id"] for row in self.rows]
        self.assertEqual(len(set(ids)), 200)
        self.assertEqual(self.rows[0]["doc_id"], "SC-01-D01")
        self.assertEqual({row["site_id"][:2] for row in self.rows}, {"SC", "TH", "HO", "RP"})

    def test_dates_and_pre_gdpr_flag(self):
        for row in self.rows:
            self.assertTrue("2010-01-01" <= row["published"] <= "2024-12-31")
            self.assertEqual(row["pre_gdpr"], row["published"] < "2018-05-25")

    def test_truth_matches_text(self):
        for row in self.rows:
            text, truth = row["text"], row["truth"]
            self.assertEqual(truth["cnp"], has_valid_cnp(text), row["doc_id"])
            self.assertEqual(truth["names"], any(name in text for name in SURNAMES), row["doc_id"])
            self.assertEqual(truth["email"], "@example.ro" in text, row["doc_id"])
            self.assertEqual(truth["phone"], "tel. " in text, row["doc_id"])
            self.assertEqual(truth["birthdate"], "data nasterii" in text, row["doc_id"])
            phrases = HEALTH_PHRASES[row["institution_type"]]
            self.assertEqual(truth["health"], any(phrase in text for phrase in phrases), row["doc_id"])


class TestHandBuiltRows(unittest.TestCase):
    def test_only_names(self):
        row = person_row(random.Random(0), 1, "school", dict(NONE_INSERTED, names=True))
        self.assertTrue(row.startswith("1. "))
        self.assertTrue(any(name in row for name in SURNAMES))
        self.assertNotIn("CNP", row)
        self.assertNotIn("@", row)

    def test_cnp_and_health(self):
        row = person_row(random.Random(0), 2, "hospital", dict(NONE_INSERTED, cnp=True, health=True))
        self.assertTrue(has_valid_cnp(row))
        self.assertTrue(any(phrase in row for phrase in HEALTH_PHRASES["hospital"]))
        self.assertFalse(any(name in row for name in SURNAMES))

    def test_wrong_cnp_is_never_valid(self):
        rng = random.Random(0)
        for _ in range(200):
            self.assertFalse(is_valid_cnp(wrong_cnp(rng)))


class TestSave(unittest.TestCase):
    def test_writes_both_files(self):
        rows = generate(n_sites_per_type=1, docs_per_site=3)
        with tempfile.TemporaryDirectory() as folder:
            save(rows, folder)
            with open(Path(folder) / "documents.csv", newline="", encoding="utf-8") as file:
                documents = list(csv.DictReader(file))
            with open(Path(folder) / "truth.csv", newline="", encoding="utf-8") as file:
                truth = list(csv.DictReader(file))
        self.assertEqual(len(documents), 12)
        self.assertEqual(list(documents[0].keys()),
                         ["doc_id", "site_id", "institution_type", "city_size", "published", "pre_gdpr", "text"])
        self.assertEqual(documents[0]["text"], rows[0]["text"])
        self.assertEqual(list(truth[0].keys()), ["doc_id"] + CATEGORIES)
        for saved, row in zip(truth, rows):
            for category in CATEGORIES:
                self.assertEqual(saved[category], str(int(row["truth"][category])))
