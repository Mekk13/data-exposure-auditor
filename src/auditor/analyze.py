import csv
from math import sqrt
from pathlib import Path

from auditor.classify import CATEGORIES, SENSITIVE

ROOT = Path(__file__).resolve().parents[2]
TRUTH = ROOT / "data" / "synthetic" / "truth.csv"
RESULTS = ROOT / "results" / "results.csv"
SUMMARY = ROOT / "results" / "summary.md"

Z = 1.96


def read_rows(path) -> list:
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def confusion(truth: list, predicted: list) -> tuple:
    tp = fp = fn = tn = 0
    for actual, guess in zip(truth, predicted):
        if actual and guess:
            tp += 1
        elif guess:
            fp += 1
        elif actual:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def precision(tp: int, fp: int) -> float:
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)


def recall(tp: int, fn: int) -> float:
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)


def f1(p: float, r: float) -> float:
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def is_sensitive_truth(row: dict) -> bool:
    return any(row[category] == "1" for category in SENSITIVE)


def metrics_row(name: str, truth: list, predicted: list) -> dict:
    tp, fp, fn, tn = confusion(truth, predicted)
    p = precision(tp, fp)
    r = recall(tp, fn)
    return {"category": name, "tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f1(p, r)}


def per_category_metrics(truth_rows: list, result_rows: list) -> list:
    truth_by_id = {row["doc_id"]: row for row in truth_rows}
    pairs = [(truth_by_id[row["doc_id"]], row) for row in result_rows if row["doc_id"] in truth_by_id]
    table = []
    for category in CATEGORIES:
        truth = [actual[category] == "1" for actual, _ in pairs]
        predicted = [str(found[category]) == "1" for _, found in pairs]
        table.append(metrics_row(category, truth, predicted))
    truth = [is_sensitive_truth(actual) for actual, _ in pairs]
    predicted = [found["label"] == "sensitive" for _, found in pairs]
    table.append(metrics_row("sensitive", truth, predicted))
    return table


def wilson(successes: int, n: int, z: float = Z) -> tuple:
    if n == 0:
        return 0.0, 0.0
    p = successes / n
    middle = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return middle - half, middle + half


def sensitive_share(result_rows: list, pre_gdpr_only: bool = True) -> dict:
    rows = [row for row in result_rows if row["label"] != "none"]
    if pre_gdpr_only:
        rows = [row for row in rows if str(row["pre_gdpr"]) == "1"]
    total = len(rows)
    sensitive = sum(1 for row in rows if row["label"] == "sensitive")
    share = sensitive / total if total else 0.0
    low, high = wilson(sensitive, total)
    return {"sensitive": sensitive, "total": total, "share": share, "low": low, "high": high}


def breakdown(result_rows: list, key: str) -> dict:
    groups = {}
    for row in result_rows:
        groups.setdefault(row[key], []).append(row)
    return {name: sensitive_share(groups[name]) for name in sorted(groups)}


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def metrics_table(table: list) -> list:
    lines = ["| category | tp | fp | fn | precision | recall | f1 |", "|---|---|---|---|---|---|---|"]
    for row in table:
        lines.append(f"| {row['category']} | {row['tp']} | {row['fp']} | {row['fn']} | "
                     f"{row['precision']:.3f} | {row['recall']:.3f} | {row['f1']:.3f} |")
    return lines


def share_table(title: str, groups: dict) -> list:
    lines = [f"| {title} | sensitive | with personal data | share | 95% CI |", "|---|---|---|---|---|"]
    for name, result in groups.items():
        lines.append(f"| {name} | {result['sensitive']} | {result['total']} | {percent(result['share'])} | "
                     f"{percent(result['low'])} - {percent(result['high'])} |")
    return lines


def build_summary(table: list, overall: dict, by_type: dict, by_size: dict) -> str:
    lines = ["# Results summary", "", "Synthetic data only. These numbers show the method, not real findings.", ""]
    lines += ["## Detector metrics", ""] + metrics_table(table) + [""]
    lines += ["## Hypothesis", "",
              "Among exposed pre-GDPR documents that contain personal data, the share labelled sensitive:", ""]
    lines += share_table("group", {"all": overall}) + [""]
    lines += ["## By institution type (pre-GDPR)", ""] + share_table("institution_type", by_type) + [""]
    lines += ["## By city size (pre-GDPR)", ""] + share_table("city_size", by_size) + [""]
    return "\n".join(lines)


def main(truth_path=TRUTH, results_path=RESULTS, summary_path=SUMMARY) -> str:
    truth_rows = read_rows(truth_path)
    result_rows = read_rows(results_path)
    table = per_category_metrics(truth_rows, result_rows)
    overall = sensitive_share(result_rows)
    by_type = breakdown(result_rows, "institution_type")
    by_size = breakdown(result_rows, "city_size")
    summary = build_summary(table, overall, by_type, by_size)
    summary_path = Path(summary_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", newline="", encoding="utf-8") as file:
        file.write(summary)
    print(summary)
    print(f"wrote {summary_path}")
    return summary


if __name__ == "__main__":
    main()
