# CI regression record: absolute-path exclusion

Date investigated: 2026-08-01

Affected run: [GitHub Actions 30638965397](https://github.com/Tontonjeong/Tontonjeong.github.io/actions/runs/30638965397)

Affected commit: `11ff401a26c5f272e93ea4b55d6ff8cb048a3884`

Failed job/step: `validate` / `Validate recruiter and publication metadata`

## Observed failure

The Jekyll build and generated-site validation passed. The metadata step then
reported:

```text
PASS: approved contact, degree, graduation, and availability metadata are wired to KO/EN pages
PASS: KO/EN expected-graduation and availability values share the approved ISO dates
FAIL: no LinkedIn URL found
```

The failure was deterministic on the Ubuntu GitHub-hosted runner and did not
indicate missing profile data. The canonical LinkedIn URL was present in
`src/_data/profile.yml`.

## Root cause

`scripts/check_linkedin_canonical.py` excluded paths by testing every segment
of each **absolute** path for the names `.git`, `_site`, `work`, or `vendor`.
GitHub checks out repositories below `/home/runner/work/...`; therefore the
runner-owned `work` path segment caused every repository file to be skipped.
The scan count remained zero and produced the misleading `no LinkedIn URL
found` error.

## Corrective action

Commit `95f78165fe3267204bb4e9b59fccfd8625bcc955` changed exclusion checks to
operate on `path.relative_to(ROOT).parts`. The rerun
[30639032061](https://github.com/Tontonjeong/Tontonjeong.github.io/actions/runs/30639032061)
passed and PR #5 was merged.

## Regression prevention

`tests/test_check_linkedin_canonical.py` now creates a temporary repository
whose **parent** directory is named `work`. It proves that:

1. a repository below an absolute `work` path is still scanned; and
2. only a repository-relative `work/` directory is excluded.

The deploy workflow runs this test before the contact and publication metadata
checks. A future change that reintroduces absolute-path exclusions will fail in
CI before Pages deployment.
