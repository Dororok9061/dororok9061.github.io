#!/usr/bin/env python3
"""Audit whether a worktree is clean and HEAD exists at its live remote ref."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from check_git_remote_parity import inspect_parity, run_git


def changed_count(repo: Path, *arguments: str) -> int | None:
    try:
        result = run_git(repo, *arguments)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return len([value for value in result.stdout.split("\0") if value])


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Audit uncommitted files and live remote parity.")
    result.add_argument("--repo", type=Path, default=Path.cwd(), help="Git worktree (default: cwd)")
    result.add_argument("--remote", help="configured remote name (default: branch upstream or origin)")
    result.add_argument("--ref", help="remote ref or branch name; useful for detached HEAD")
    result.add_argument("--timeout", type=int, default=30, help="git ls-remote timeout in seconds")
    result.add_argument("--strict", action="store_true", help="return nonzero unless clean and pushed")
    return result


def main() -> int:
    args = parser().parse_args()
    counts = (
        changed_count(args.repo, "diff", "--cached", "--name-only", "-z"),
        changed_count(args.repo, "diff", "--name-only", "-z"),
        changed_count(args.repo, "ls-files", "--others", "--exclude-standard", "-z"),
    )
    if any(value is None for value in counts):
        status, detail = "NOT_CHECKED", "not a readable Git worktree"
    else:
        staged, unstaged, untracked = counts
        parity = inspect_parity(args.repo, args.remote, args.ref, max(1, args.timeout))
        if staged or unstaged or untracked:
            status = "LOCAL_CHANGES"
            detail = f"staged={staged}, unstaged={unstaged}, untracked={untracked}; {parity.status}"
        elif parity.status == "PASS":
            status, detail = "PASS", f"clean worktree; {parity.detail}"
        else:
            status, detail = "UNPUSHED", parity.detail
    print(f"{status}: {detail}")
    return int(args.strict and status != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
