# Codex handoff

Reactivation prompt: Read this file, ensure Ruby/Bundler is on PATH, fresh-clone remote `main`, and rerun Jekyll/security checks.

- Base branch/commit: `fix/publication-evidence-ci-regression` / `305aaac231c01e7baf83aa83596ae0faa085e33c`.
- Migration branch: `migration/portable-contract-20260801`.
- Remote `main` at migration: `69d652d5780dc42f479ed19e16cfb7d9378dcc79`.
- Local recruiter and divergent-main states preserved under named remote branches.
- Fresh clone/fsck: PASS. Jekyll build: BLOCKED because Ruby/Bundler was not on PATH.
- Next: install/activate Ruby 3.3.12 and Bundler, then rerun `VERIFY.md`; no force-push.
