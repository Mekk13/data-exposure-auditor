import unittest

from auditor.cnp import check_digit, contains_cnp, count_cnps, is_valid_cnp


def make_cnp(prefix: str) -> str:
    return prefix + str(check_digit(prefix))


class TestIsValidCnp(unittest.TestCase):
    def test_accepts_synthetic_valid_cnp(self):
        self.assertTrue(is_valid_cnp(make_cnp("198010112345")))

    def test_accepts_2000s_birth(self):
        self.assertTrue(is_valid_cnp(make_cnp("605123040123")))

    def test_rejects_wrong_check_digit(self):
        cnp = make_cnp("198010112345")
        wrong = cnp[:12] + str((int(cnp[12]) + 1) % 10)
        self.assertFalse(is_valid_cnp(wrong))

    def test_rejects_impossible_date(self):
        self.assertFalse(is_valid_cnp(make_cnp("198023012345")))

    def test_rejects_unknown_county_code(self):
        self.assertFalse(is_valid_cnp(make_cnp("198010160345")))

    def test_rejects_leading_zero(self):
        self.assertFalse(is_valid_cnp(make_cnp("098010112345")))

    def test_rejects_wrong_length_and_non_digits(self):
        self.assertFalse(is_valid_cnp("19801011234"))
        self.assertFalse(is_valid_cnp("19801011234A5"))


class TestCountCnps(unittest.TestCase):
    def test_counts_only_valid_numbers_in_text(self):
        valid_a = make_cnp("198010112345")
        valid_b = make_cnp("287123140001")
        text = f"Elev A, CNP {valid_a}; Elev B CNP: {valid_b}; tel 0712345678; cod 1234567890123"
        self.assertEqual(count_cnps(text), 2)
        self.assertTrue(contains_cnp(text))

    def test_ignores_digits_embedded_in_longer_numbers(self):
        text = "ref 9" + make_cnp("198010112345") + "9"
        self.assertEqual(count_cnps(text), 0)

    def test_empty_text(self):
        self.assertEqual(count_cnps(""), 0)
        self.assertFalse(contains_cnp(""))


if __name__ == "__main__":
    unittest.main()
