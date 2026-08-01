#!/usr/bin/env python3
"""Compare local HEAD with its live remote ref without mutating the repository."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess


SHA = re.compile(r"^[0-9a-f]{40,64}$")


@dataclass(frozen=True)
class Parity:
    status: str
    detail: str


def run_git(repo: Path, *arguments: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GCM_INTERACTIVE"] = "Never"
    return subprocess.run(
        ["git", "-C", os.fspath(repo), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        timeout=timeout,
        check=False,
    )


def output(repo: Path, *arguments: str) -> str | None:
    try:
        result = run_git(repo, *arguments)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def normalize_ref(value: str) -> str:
    return value if value.startswith("refs/") else f"refs/heads/{value}"


def local_context(repo: Path, explicit_remote: str | None, explicit_ref: str | None) -> tuple[str, str | None, str | None] | None:
    head = output(repo, "rev-parse", "HEAD")
    if head is None or not SHA.fullmatch(head):
        return None
    branch = output(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    remote = explicit_remote
    target = normalize_ref(explicit_ref) if explicit_ref else None

    if target is None and branch:
        configured_remote = output(repo, "config", "--get", f"branch.{branch}.remote")
        configured_ref = output(repo, "config", "--get", f"branch.{branch}.merge")
        if remote is None and configured_remote and configured_remote != ".":
            remote = configured_remote
        target = configured_ref or f"refs/heads/{branch}"
    elif target is None:
        github_ref = os.environ.get("GITHUB_REF", "")
        if github_ref.startswith("refs/"):
            target = github_ref
        elif os.environ.get("GITHUB_REF_TYPE") == "branch" and os.environ.get("GITHUB_REF_NAME"):
            target = f"refs/heads/{os.environ['GITHUB_REF_NAME']}"

    return head, remote or "origin", target


def remote_refs(repo: Path, remote: str, target: str | None, timeout: int) -> tuple[str, list[tuple[str, str]]]:
    arguments = ["ls-remote", "--refs", remote]
    if target:
        arguments.append(target)
    try:
        result = run_git(repo, *arguments, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable", []
    if result.returncode != 0:
        return "unavailable", []
    refs: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        fields = line.split("\t", 1)
        if len(fields) == 2 and SHA.fullmatch(fields[0]) and fields[1].startswith("refs/"):
            refs.append((fields[0], fields[1]))
    return "ok", refs


def inspect_parity(
    repo: Path, remote: str | None = None, ref: str | None = None, timeout: int = 30
) -> Parity:
    context = local_context(repo, remote, ref)
    if context is None:
        return Parity("NOT_CHECKED", "not a readable Git worktree")
    head, selected_remote, target = context
    state, refs = remote_refs(repo, selected_remote or "origin", target, timeout)
    if state != "ok":
        return Parity("NOT_CHECKED", "live remote refs are unavailable")
    if target and not refs:
        return Parity("REMOTE_REF_MISSING", f"remote ref {target} is absent")
    matching = [name for sha, name in refs if sha == head]
    if matching:
        shown = target or matching[0]
        return Parity("PASS", f"HEAD {head[:12]} matches {shown}")
    if target:
        return Parity("MISMATCH", f"HEAD {head[:12]} does not match {target}")
    return Parity("MISMATCH", f"detached HEAD {head[:12]} is absent from live remote refs")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Audit HEAD against live refs using git ls-remote only.")
    result.add_argument("--repo", type=Path, default=Path.cwd(), help="Git worktree (default: cwd)")
    result.add_argument("--remote", help="configured remote name (default: branch upstream or origin)")
    result.add_argument("--ref", help="remote ref or branch name; useful for detached HEAD")
    result.add_argument("--timeout", type=int, default=30, help="git ls-remote timeout in seconds")
    result.add_argument("--strict", action="store_true", help="return nonzero unless HEAD matches")
    return result


def main() -> int:
    args = parser().parse_args()
    result = inspect_parity(args.repo, args.remote, args.ref, max(1, args.timeout))
    print(f"{result.status}: {result.detail}")
    return int(args.strict and result.status != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
