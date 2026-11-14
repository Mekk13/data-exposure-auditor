import csv
from collections import Counter
from pathlib import Path

from auditor.classify import CATEGORIES, detect_all, label

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = ROOT / "data" / "synthetic" / "documents.csv"
RESULTS = ROOT / "results" / "results.csv"

KEEP = ["doc_id", "site_id", "institution_type", "city_size", "published", "pre_gdpr"]
COLUMNS = KEEP + CATEGORIES + ["label"]


def read_documents(path) -> list:
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def audit(documents: list) -> list:
    results = []
    for document in documents:
        found = detect_all(document["text"])
        row = {key: document[key] for key in KEEP}
        for category in CATEGORIES:
            row[category] = int(found[category])
        row["label"] = label(found)
        results.append(row)
    return results


def write_results(results: list, path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)


def main(documents_path=DOCUMENTS, results_path=RESULTS) -> list:
    results = audit(read_documents(documents_path))
    write_results(results, results_path)
    counts = Counter(row["label"] for row in results)
    print(f"audited {len(results)} documents -> {results_path}")
    for name in ["sensitive", "ordinary", "none"]:
        print(f"  {name}: {counts[name]}")
    return results


if __name__ == "__main__":
    main()
