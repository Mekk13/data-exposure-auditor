import unittest

from auditor.classify import CATEGORIES, SENSITIVE, detect_all, label
from auditor.detectors.cnp import check_digit


def make_cnp(prefix: str) -> str:
    return prefix + str(check_digit(prefix))


class TestDetectAll(unittest.TestCase):
    def test_returns_every_category(self):
        found = detect_all("")
        self.assertEqual(list(found.keys()), CATEGORIES)
        self.assertFalse(any(found.values()))

    def test_detects_each_category(self):
        cnp = make_cnp("198010112345")
        text = (
            f"POPESCU Ion, CNP {cnp}\n"
            "IONESCU Maria, data nasterii 01.02.1980\n"
            "GEORGESCU Andrei, certificat medical\n"
            "contact: secretariat@example.com, tel 0712 345 678"
        )
        found = detect_all(text)
        self.assertTrue(all(found.values()))

    def test_returns_only_booleans(self):
        found = detect_all("tel 0712345678")
        self.assertTrue(all(isinstance(value, bool) for value in found.values()))


class TestLabel(unittest.TestCase):
    def test_sensitive_categories(self):
        self.assertEqual(SENSITIVE, {"cnp", "health"})

    def test_cnp_is_sensitive(self):
        cnp = make_cnp("287123140001")
        self.assertEqual(label(detect_all(f"CNP {cnp}")), "sensitive")

    def test_health_is_sensitive(self):
        self.assertEqual(label(detect_all("elev cu grad de handicap")), "sensitive")

    def test_sensitive_wins_over_ordinary(self):
        self.assertEqual(label({"cnp": False, "health": True, "email": True}), "sensitive")

    def test_contact_is_ordinary(self):
        self.assertEqual(label(detect_all("secretariat@example.com")), "ordinary")
        self.assertEqual(label(detect_all("tel 0264 123 456")), "ordinary")

    def test_nothing_found_is_none(self):
        self.assertEqual(label(detect_all("Orarul clasei a V-a")), "none")
        self.assertEqual(label({}), "none")
