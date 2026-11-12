import re

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")

PREFIX = r"(?<!\d)(?:\+40|0040|0)[\s.-]?"
SEP = r"[\s.-]?"

PHONE_PATTERNS = [
    re.compile(PREFIX + r"7\d{2}" + SEP + r"\d{3}" + SEP + r"\d{3}(?!\d)"),
    re.compile(PREFIX + r"[23]\d" + SEP + r"\d{3}" + SEP + r"\d{2}" + SEP + r"\d{2}(?!\d)"),
    re.compile(PREFIX + r"[23]\d{2}" + SEP + r"\d{3}" + SEP + r"\d{3}(?!\d)"),
]


def contains_email(text: str) -> bool:
    return EMAIL_PATTERN.search(text) is not None


def contains_phone(text: str) -> bool:
    return any(pattern.search(text) for pattern in PHONE_PATTERNS)
