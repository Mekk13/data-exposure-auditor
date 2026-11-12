import unittest

from auditor.detectors.health import contains_health


class TestContainsHealth(unittest.TestCase):
    def test_single_keywords(self):
        self.assertTrue(contains_health("Diagnostic: necunoscut"))
        self.assertTrue(contains_health("absent din cauza unei boli"))
        self.assertTrue(contains_health("urmeaza tratament"))
        self.assertTrue(contains_health("elev cu dizabilitate"))

    def test_diacritics_variants(self):
        self.assertTrue(contains_health("o boală cronică"))
        self.assertTrue(contains_health("AFECȚIUNE respiratorie"))
        self.assertTrue(contains_health("afecţiune respiratorie"))

    def test_multi_word_keywords(self):
        self.assertTrue(contains_health("a depus certificat medical"))
        self.assertTrue(contains_health("Grad  de\nhandicap: accentuat"))
        self.assertTrue(contains_health("elevi cu cerințe educaționale speciale"))

    def test_ces_abbreviation(self):
        self.assertTrue(contains_health("Elev CES, clasa a V-a"))

    def test_whole_word_only(self):
        self.assertFalse(contains_health("procesul verbal al sedintei"))
        self.assertFalse(contains_health("diagnostice de sistem"))
        self.assertFalse(contains_health("bolta bisericii"))

    def test_ordinary_text(self):
        self.assertFalse(contains_health("Orarul clasei a V-a pentru semestrul I"))

    def test_empty_text(self):
        self.assertFalse(contains_health(""))
