# data-exposure-auditor

A research tool that checks how much old personal data is still sitting
in public view on institutional websites, and flags how sensitive it is,
without ever collecting the data itself.

## What it does

Plenty of personal data that was put online years ago is still a quick
search away: name lists, old result sheets, scanned documents. A lot of
it predates GDPR and was never cleaned up. This tool audits a set of
institutional websites, finds publicly reachable documents, and records
only *what kind* of data is exposed (names, ID numbers, and so on) and
whether it counts as sensitive, never the actual values.

The point isn't to collect anyone's data. It's to measure the scale of
the problem: how much is out there, and how much of it is the kind that
really shouldn't be.

## Tech

Python (details to be firmed up as the project takes shape).

## How to run

Everything uses the Python standard library (3.12), no installs needed.
Run these from the repo root.

1. Generate the fake dataset (200 made-up documents, seed 42):

   ```
   python generate.py
   ```

   This writes `data/synthetic/documents.csv` and `data/synthetic/truth.csv`.
   All values in it are invented.

2. Run the audit:

   ```
   python run.py
   ```

   This writes `results/results.csv`: one row per document with a 0/1 flag
   per category and a label (`sensitive`, `ordinary` or `none`). The text
   itself is never written to the results.

3. Run the tests:

   ```
   python -m unittest discover -s tests -t . -v
   ```
