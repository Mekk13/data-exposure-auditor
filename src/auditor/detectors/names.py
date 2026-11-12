import re

from auditor.detectors.text import normalize

UPPER = "A-ZĂÂÎȘŞȚŢ"
LOWER = "a-zăâîșşțţ"

WORD = rf"(?:[{UPPER}]{{2,}}|[{UPPER}][{LOWER}]+)"
SURNAME = rf"{WORD}(?:-{WORD})?"
GIVEN = rf"[{UPPER}][{LOWER}]+(?:-[{UPPER}][{LOWER}]+)?"

NAME_PATTERN = re.compile(rf"\b{SURNAME}\s+{GIVEN}(?:\s+{GIVEN})?\b")

STOPWORDS = {
    "scoala", "liceul", "colegiul", "gradinita", "universitatea", "facultatea",
    "spitalul", "primaria", "judetul", "consiliul", "ministerul", "inspectoratul",
    "directia", "centrul", "serviciul", "biroul", "comuna", "orasul", "municipiul",
    "strada", "str", "nr", "romania", "clasa", "lista", "anunt", "rezultate",
    "gimnaziala", "teoretic", "tehnologic", "national", "local", "judetean",
}

MIN_NAMES = 3


def looks_like_name(entry: str) -> bool:
    for match in NAME_PATTERN.finditer(entry):
        words = normalize(match.group()).replace("-", " ").split()
        if not any(word in STOPWORDS for word in words):
            return True
    return False


def contains_names(text: str) -> bool:
    entries = re.split(r"[\n;,]", text)
    return sum(1 for entry in entries if looks_like_name(entry)) >= MIN_NAMES
