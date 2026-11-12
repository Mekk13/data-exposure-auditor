from auditor.detectors.birthdate import contains_birthdate
from auditor.detectors.cnp import contains_cnp
from auditor.detectors.contact import contains_email, contains_phone
from auditor.detectors.health import contains_health
from auditor.detectors.names import contains_names

CATEGORIES = ["cnp", "health", "names", "email", "phone", "birthdate"]
SENSITIVE = {"cnp", "health"}

DETECTORS = {
    "cnp": contains_cnp,
    "health": contains_health,
    "names": contains_names,
    "email": contains_email,
    "phone": contains_phone,
    "birthdate": contains_birthdate,
}


def detect_all(text: str) -> dict:
    return {category: DETECTORS[category](text) for category in CATEGORIES}


def label(found: dict) -> str:
    if any(found.get(category, False) for category in SENSITIVE):
        return "sensitive"
    if any(found.values()):
        return "ordinary"
    return "none"
