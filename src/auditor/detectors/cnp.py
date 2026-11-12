import re
from datetime import date

CHECK_KEY = "279146358279"

CENTURY_BY_SEX_DIGIT = {
    "1": 1900, "2": 1900,
    "3": 1800, "4": 1800,
    "5": 2000, "6": 2000,
    "7": None, "8": None, "9": None,
}

VALID_COUNTY_CODES = {f"{n:02d}" for n in range(1, 47)} | {"47", "48", "51", "52", "70"}

CANDIDATE_PATTERN = re.compile(r"(?<!\d)[1-9]\d{12}(?!\d)")


def check_digit(first_twelve: str) -> int:
    total = sum(int(d) * int(k) for d, k in zip(first_twelve, CHECK_KEY))
    rest = total % 11
    return 1 if rest == 10 else rest


def _has_valid_date(candidate: str) -> bool:
    century = CENTURY_BY_SEX_DIGIT[candidate[0]]
    yy, mm, dd = int(candidate[1:3]), int(candidate[3:5]), int(candidate[5:7])
    years = [century + yy] if century else [1900 + yy, 2000 + yy]
    for year in years:
        try:
            date(year, mm, dd)
            return True
        except ValueError:
            continue
    return False


def is_valid_cnp(candidate: str) -> bool:
    if len(candidate) != 13 or not candidate.isdigit():
        return False
    if candidate[0] not in CENTURY_BY_SEX_DIGIT:
        return False
    if not _has_valid_date(candidate):
        return False
    if candidate[7:9] not in VALID_COUNTY_CODES:
        return False
    return check_digit(candidate[:12]) == int(candidate[12])


def count_cnps(text: str) -> int:
    return sum(1 for match in CANDIDATE_PATTERN.finditer(text) if is_valid_cnp(match.group()))


def contains_cnp(text: str) -> bool:
    return any(is_valid_cnp(match.group()) for match in CANDIDATE_PATTERN.finditer(text))
