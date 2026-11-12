import unittest

from auditor.detectors.contact import contains_email, contains_phone


class TestContainsEmail(unittest.TestCase):
    def test_finds_simple_email(self):
        self.assertTrue(contains_email("Contact: secretariat@example.com"))

    def test_finds_email_with_dots_and_subdomain(self):
        self.assertTrue(contains_email("scrieti la ion.popescu+test@mail.example.ro."))

    def test_ignores_text_without_at(self):
        self.assertFalse(contains_email("www.example.com si nimic altceva"))

    def test_ignores_at_without_domain(self):
        self.assertFalse(contains_email("pret 5 @ bucata"))
        self.assertFalse(contains_email("user@localhost"))

    def test_empty_text(self):
        self.assertFalse(contains_email(""))


class TestContainsPhone(unittest.TestCase):
    def test_mobile_plain(self):
        self.assertTrue(contains_phone("tel 0712345678"))

    def test_mobile_with_spaces_dots_dashes(self):
        self.assertTrue(contains_phone("tel 0712 345 678"))
        self.assertTrue(contains_phone("tel 0712.345.678"))
        self.assertTrue(contains_phone("tel 0712-345-678"))

    def test_mobile_international_forms(self):
        self.assertTrue(contains_phone("+40712345678"))
        self.assertTrue(contains_phone("+40 712 345 678"))
        self.assertTrue(contains_phone("0040712345678"))

    def test_bucharest_landline(self):
        self.assertTrue(contains_phone("Fax: 021 312 34 56"))
        self.assertTrue(contains_phone("021-312-34-56"))

    def test_county_landline(self):
        self.assertTrue(contains_phone("Telefon 0264 123 456"))
        self.assertTrue(contains_phone("0364.123.456"))

    def test_ignores_dates(self):
        self.assertFalse(contains_phone("sedinta din 02.03.2021 10:00"))
        self.assertFalse(contains_phone("07.12.2023"))

    def test_ignores_too_short_and_too_long(self):
        self.assertFalse(contains_phone("071234567"))
        self.assertFalse(contains_phone("07123456789"))

    def test_ignores_digits_inside_longer_number(self):
        self.assertFalse(contains_phone("cod 1234071234567"))

    def test_ignores_wrong_leading_digit(self):
        self.assertFalse(contains_phone("0512345678"))
        self.assertFalse(contains_phone("0812345678"))

    def test_empty_text(self):
        self.assertFalse(contains_phone(""))
