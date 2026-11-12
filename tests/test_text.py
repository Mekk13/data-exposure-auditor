import unittest

from auditor.detectors.text import normalize


class TestNormalize(unittest.TestCase):
    def test_lowercases(self):
        self.assertEqual(normalize("ABC Def"), "abc def")

    def test_strips_comma_and_cedilla_diacritics(self):
        self.assertEqual(normalize("ăâîșşțţ"), "aaisstt")

    def test_strips_uppercase_diacritics(self):
        self.assertEqual(normalize("ȘCOALA ÎNVĂȚĂMÂNT"), "scoala invatamant")
