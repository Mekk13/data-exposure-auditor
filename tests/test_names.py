import unittest

from auditor.detectors.names import contains_names, looks_like_name


class TestLooksLikeName(unittest.TestCase):
    def test_uppercase_surname(self):
        self.assertTrue(looks_like_name("POPESCU Ion"))

    def test_capitalised_surname_two_given_names(self):
        self.assertTrue(looks_like_name("Ionescu Maria Elena"))

    def test_diacritics_and_hyphen(self):
        self.assertTrue(looks_like_name("ȘTEFĂNESCU-POP Ana-Maria"))

    def test_single_word_is_not_name(self):
        self.assertFalse(looks_like_name("Popescu"))

    def test_lowercase_is_not_name(self):
        self.assertFalse(looks_like_name("popescu ion"))

    def test_all_caps_heading_is_not_name(self):
        self.assertFalse(looks_like_name("LISTA CANDIDATILOR ADMISI"))

    def test_institution_is_ignored(self):
        self.assertFalse(looks_like_name("Liceul Teoretic Avram"))
        self.assertFalse(looks_like_name("Școala Gimnazială Nr. 5"))
        self.assertFalse(looks_like_name("Primăria Comunei"))


class TestContainsNames(unittest.TestCase):
    def test_list_of_three_names_on_lines(self):
        text = "POPESCU Ion\nIONESCU Maria Elena\nGeorgescu Andrei"
        self.assertTrue(contains_names(text))

    def test_names_separated_by_commas_and_semicolons(self):
        text = "Admisi: Popescu Ion, Ionescu Maria; Georgescu Andrei"
        self.assertTrue(contains_names(text))

    def test_two_names_are_not_enough(self):
        self.assertFalse(contains_names("POPESCU Ion\nIONESCU Maria"))

    def test_institution_list_is_not_names(self):
        text = "Liceul Teoretic Avram\nȘcoala Gimnazială Nr. 5\nSpitalul Județean Cluj\nPrimăria Comunei Vale"
        self.assertFalse(contains_names(text))

    def test_empty_text(self):
        self.assertFalse(contains_names(""))
