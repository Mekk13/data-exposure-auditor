import re

from auditor.detectors.text import normalize

KEYWORDS = r"(?:data nasterii|data de nastere|nascut|\bn\.)"
DATE = r"\b\d{1,2}[./-]\d{1,2}[./-]\d{4}\b"

BIRTHDATE_PATTERN = re.compile(KEYWORDS + r".{0,40}?" + DATE, re.DOTALL)


def contains_birthdate(text: str) -> bool:
    return BIRTHDATE_PATTERN.search(normalize(text)) is not None
