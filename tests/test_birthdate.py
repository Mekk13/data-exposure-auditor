import unittest

from auditor.detectors.birthdate import contains_birthdate


class TestContainsBirthdate(unittest.TestCase):
    def test_data_nasterii_with_dots(self):
        self.assertTrue(contains_birthdate("Data nasterii: 01.02.1980"))

    def test_diacritics_and_uppercase(self):
        self.assertTrue(contains_birthdate("DATA NAȘTERII 15/06/1975"))
        self.assertTrue(contains_birthdate("Data naşterii 15-06-1975"))

    def test_nascut_and_nascuta(self):
        self.assertTrue(contains_birthdate("Ion, născut la 3.4.1990 in Cluj"))
        self.assertTrue(contains_birthdate("Maria, nascuta in data de 12.12.1988"))

    def test_short_n_dot(self):
        self.assertTrue(contains_birthdate("Popescu Ion (n. 07.08.1965)"))

    def test_date_on_next_line(self):
        self.assertTrue(contains_birthdate("Data nasterii:\n01.02.1980"))

    def test_date_without_keyword(self):
        self.assertFalse(contains_birthdate("Sedinta are loc pe 01.02.2024"))

    def test_keyword_without_date(self):
        self.assertFalse(contains_birthdate("Completati data nasterii in formular"))

    def test_date_too_far_from_keyword(self):
        text = "Data nasterii se completeaza in formularul anexat la cerere. Termen: 01.02.2024"
        self.assertFalse(contains_birthdate(text))

    def test_n_inside_word_is_not_keyword(self):
        self.assertFalse(contains_birthdate("Termen. 01.02.2024"))

    def test_incomplete_date(self):
        self.assertFalse(contains_birthdate("Data nasterii: 01.02.80"))

    def test_empty_text(self):
        self.assertFalse(contains_birthdate(""))
