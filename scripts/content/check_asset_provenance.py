#!/usr/bin/env python3
"""Check that every static public /assets reference resolves inside src."""

from __future__ import annotations

import csv
import hashlib

from provenance_common import ROOT, SRC, asset_exists, asset_references, digest, fail, public_asset


def main() -> int:
    references = asset_references()
    errors: list[str] = []
    for reference in references:
        if not asset_exists(reference.asset):
            source = reference.source.relative_to(SRC)
            errors.append(f"{source}:{reference.line} missing {reference.asset}")

    audit = ROOT / "docs" / "qa" / "ASSET_PROVENANCE_AUDIT.csv"
    if not audit.is_file():
        errors.append("docs/qa/ASSET_PROVENANCE_AUDIT.csv is missing")
    else:
        with audit.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != 14:
            errors.append(f"expected 14 primary asset audit rows, found {len(rows)}")
        for row in rows:
            path = public_asset(row["primary_asset"])
            if not path.is_file():
                errors.append(f"audit row {row['id']} references missing {row['primary_asset']}")
            else:
                expected = row["sha256_12"]
                candidates = {digest(path)[:12]}
                # Git may materialize text SVGs with CRLF on Windows while Pages
                # builds the LF blob on Linux. Treat newline encoding as transport,
                # while still rejecting every content-changing hash mismatch.
                normalized = path.read_bytes().replace(b"\r\n", b"\n")
                candidates.add(hashlib.sha256(normalized).hexdigest()[:12])
                if expected not in candidates:
                    errors.append(f"audit row {row['id']} has stale SHA-256")
    unique = len({reference.asset for reference in references})
    return fail(f"{len(references)} public asset references resolve to {unique} targets; 14 audit rows are current", errors)


if __name__ == "__main__":
    raise SystemExit(main())
