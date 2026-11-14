import csv
import random
from datetime import date, timedelta
from pathlib import Path

from auditor.classify import CATEGORIES
from auditor.detectors.cnp import check_digit

GDPR_DATE = date(2018, 5, 25)
FIRST_DAY = date(2010, 1, 1)
LAST_DAY = date(2024, 12, 31)

TYPES = {
    "school": "SC",
    "town_hall": "TH",
    "hospital": "HO",
    "results_portal": "RP",
}

CITY_SIZES = ["small", "medium", "large"]

PROBABILITIES = {
    "school": {"cnp": 0.2, "health": 0.25, "names": 0.9, "email": 0.3, "phone": 0.3, "birthdate": 0.5},
    "town_hall": {"cnp": 0.3, "health": 0.2, "names": 0.8, "email": 0.2, "phone": 0.4, "birthdate": 0.2},
    "hospital": {"cnp": 0.35, "health": 0.8, "names": 0.7, "email": 0.1, "phone": 0.3, "birthdate": 0.5},
    "results_portal": {"cnp": 0.25, "health": 0.05, "names": 0.95, "email": 0.1, "phone": 0.05, "birthdate": 0.3},
}

DECOY_PROBABILITY = 0.4

SURNAMES = ["POPESCU", "IONESCU", "POPA", "RADU", "DUMITRU", "STAN", "STOICA", "GHEORGHE",
            "MATEI", "CIOBANU", "SERBAN", "MOLDOVAN", "LUCA", "NISTOR", "BARBU", "TUDOR"]
GIVEN_NAMES = ["Ion", "Maria", "Andrei", "Elena", "Mihai", "Ana", "Alexandru", "Ioana",
               "Gabriel", "Cristina", "Vasile", "Daniela", "Florin", "Raluca", "Bogdan", "Simona"]

HEADERS = {
    "school": "Scoala Gimnaziala Nr. {n}\nLista elevilor clasei a {grade}-a, anul scolar {year}-{next_year}",
    "town_hall": "Primaria {place}\nHotarare privind lista beneficiarilor de ajutor social, {year}",
    "hospital": "Spitalul Judetean {place}\nLista pacientilor, sectia {ward}, {year}",
    "results_portal": "Olimpiada de matematica, etapa judeteana {year}\nTabel cu rezultatele finale",
}

PLACES = ["Arad", "Deva", "Turda", "Bistrita", "Focsani", "Slobozia", "Vaslui", "Zalau"]
WARDS = ["Cardiologie", "Pediatrie", "Neurologie", "Chirurgie"]
GRADES = ["V", "VI", "VII", "VIII"]

HEALTH_PHRASES = {
    "school": ["cerinte educationale speciale", "absent, certificat medical"],
    "town_hall": ["grad de handicap accentuat", "persoana cu dizabilitati"],
    "hospital": ["diagnostic: pneumonie", "internare 5 zile", "concediu medical 10 zile"],
    "results_portal": ["absent, certificat medical"],
}

EXTRA = {
    "school": "media {score}",
    "town_hall": "suma {amount} lei",
    "hospital": "salon {room}",
    "results_portal": "punctaj {score}",
}

NO_PEOPLE_TEXT = "Anunt: programul de lucru cu publicul ramane neschimbat."


def random_day(rng: random.Random, first: date, last: date) -> date:
    return first + timedelta(days=rng.randint(0, (last - first).days))


def first_twelve(rng: random.Random) -> str:
    born = random_day(rng, date(1950, 1, 1), date(2012, 12, 31))
    if born.year < 2000:
        sex = rng.choice("12")
    else:
        sex = rng.choice("56")
    county = f"{rng.randint(1, 46):02d}"
    serial = f"{rng.randint(1, 999):03d}"
    return sex + born.strftime("%y%m%d") + county + serial


def fake_cnp(rng: random.Random) -> str:
    start = first_twelve(rng)
    return start + str(check_digit(start))


def wrong_cnp(rng: random.Random) -> str:
    start = first_twelve(rng)
    return start + str((check_digit(start) + 1) % 10)


def fake_phone(rng: random.Random) -> str:
    return f"07{rng.randint(10, 99)} {rng.randint(100, 999)} {rng.randint(100, 999)}"


def fake_birthdate(rng: random.Random) -> str:
    born = random_day(rng, date(1950, 1, 1), date(2012, 12, 31))
    return "data nasterii " + born.strftime("%d.%m.%Y")


def header(rng: random.Random, institution_type: str, year: int) -> str:
    return HEADERS[institution_type].format(
        n=rng.randint(1, 30),
        grade=rng.choice(GRADES),
        year=year,
        next_year=year + 1,
        place=rng.choice(PLACES),
        ward=rng.choice(WARDS),
    )


def extra(rng: random.Random, institution_type: str) -> str:
    return EXTRA[institution_type].format(
        score=rng.randint(50, 100),
        amount=rng.randint(100, 900),
        room=rng.randint(1, 40),
    )


def person_row(rng: random.Random, number: int, institution_type: str, truth: dict) -> str:
    surname = rng.choice(SURNAMES)
    given = rng.choice(GIVEN_NAMES)
    parts = []
    if truth["names"]:
        parts.append(f"{surname} {given}")
    if truth["cnp"]:
        parts.append("CNP " + fake_cnp(rng))
    if truth["birthdate"]:
        parts.append(fake_birthdate(rng))
    if truth["health"]:
        parts.append(rng.choice(HEALTH_PHRASES[institution_type]))
    if truth["email"]:
        parts.append(f"{given.lower()}.{surname.lower()}{number}@example.ro")
    if truth["phone"]:
        parts.append("tel. " + fake_phone(rng))
    parts.append(extra(rng, institution_type))
    return f"{number}. " + ", ".join(parts)


def decoys(rng: random.Random) -> list:
    lines = []
    if rng.random() < DECOY_PROBABILITY:
        lines.append("Cod document: " + wrong_cnp(rng))
    if rng.random() < DECOY_PROBABILITY:
        lines.append(f"Factura nr. {rng.randint(2010, 2024)}/{rng.randint(1, 99999):05d}")
    if rng.random() < DECOY_PROBABILITY:
        lines.append(f"Nr. inregistrare 0{rng.choice('23')}{rng.randint(10, 99)} {rng.randint(100, 999)} {rng.randint(100, 999)}")
    return lines


def make_document(rng: random.Random, institution_type: str, published: date) -> tuple:
    chances = PROBABILITIES[institution_type]
    truth = {category: rng.random() < chances[category] for category in CATEGORIES}
    lines = [header(rng, institution_type, published.year)]
    if any(truth.values()):
        for number in range(1, rng.randint(3, 8) + 1):
            lines.append(person_row(rng, number, institution_type, truth))
    else:
        lines.append(NO_PEOPLE_TEXT)
    lines.extend(decoys(rng))
    return "\n".join(lines), truth


def generate(n_sites_per_type: int = 5, docs_per_site: int = 10, seed: int = 42) -> list:
    rng = random.Random(seed)
    rows = []
    for institution_type, prefix in TYPES.items():
        for site_number in range(1, n_sites_per_type + 1):
            site_id = f"{prefix}-{site_number:02d}"
            city_size = rng.choice(CITY_SIZES)
            for doc_number in range(1, docs_per_site + 1):
                published = random_day(rng, FIRST_DAY, LAST_DAY)
                text, truth = make_document(rng, institution_type, published)
                rows.append({
                    "doc_id": f"{site_id}-D{doc_number:02d}",
                    "site_id": site_id,
                    "institution_type": institution_type,
                    "city_size": city_size,
                    "published": published.isoformat(),
                    "pre_gdpr": published < GDPR_DATE,
                    "text": text,
                    "truth": truth,
                })
    return rows


def save(rows: list, folder) -> None:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "documents.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["doc_id", "site_id", "institution_type", "city_size", "published", "pre_gdpr", "text"])
        for row in rows:
            writer.writerow([row["doc_id"], row["site_id"], row["institution_type"], row["city_size"],
                             row["published"], int(row["pre_gdpr"]), row["text"]])
    with open(folder / "truth.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["doc_id"] + CATEGORIES)
        for row in rows:
            writer.writerow([row["doc_id"]] + [int(row["truth"][category]) for category in CATEGORIES])


def main() -> None:
    folder = Path(__file__).resolve().parents[2] / "data" / "synthetic"
    rows = generate()
    save(rows, folder)
    print(f"wrote {len(rows)} documents to {folder}")


if __name__ == "__main__":
    main()
