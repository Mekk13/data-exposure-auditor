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
