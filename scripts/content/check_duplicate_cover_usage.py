#!/usr/bin/env python3
"""Reject exact primary-cover reuse across unrelated coursework subjects."""

from __future__ import annotations

from collections import defaultdict

from provenance_common import courses, digest, fail, public_asset


def main() -> int:
    records = courses()
    by_digest: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []
    for course in records:
        path = public_asset(course.thumbnail)
        if path.is_file():
            by_digest[digest(path)].append(course.id)
    for course_ids in by_digest.values():
        if len(course_ids) > 1:
            errors.append(f"unrelated coursework covers are exact duplicates: {', '.join(course_ids)}")
    if len(by_digest) != len(records):
        errors.append(f"expected {len(records)} unique readable covers, found {len(by_digest)}")
    return fail(f"{len(records)} coursework primary covers are unique", errors)


if __name__ == "__main__":
    raise SystemExit(main())
