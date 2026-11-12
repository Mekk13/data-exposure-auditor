import re

from auditor.detectors.text import normalize

KEYWORDS = [
    "diagnostic",
    "diagnosticat",
    "diagnosticata",
    "boala",
    "boli",
    "bolnav",
    "bolnava",
    "afectiune",
    "afectiuni",
    "certificat medical",
    "concediu medical",
    "handicap",
    "grad de handicap",
    "dizabilitate",
    "dizabilitati",
    "tratament",
    "internat",
    "internata",
    "internare",
    "spitalizare",
    "ces",
    "cerinte educationale speciale",
]

HEALTH_PATTERN = re.compile(r"\b(?:" + "|".join(KEYWORDS) + r")\b")


def contains_health(text: str) -> bool:
    cleaned = " ".join(normalize(text).split())
    return HEALTH_PATTERN.search(cleaned) is not None
