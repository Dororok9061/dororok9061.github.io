# OUTTA P-1/P-2/P-3 local rerun validation

Run date: 2026-08-01 KST. Source notebooks and datasets were read-only. All
generated caches, models, and submission CSV files stayed in the ignored
workspace. The repository contains only clean scripts, compact JSON reports,
and sanitized executed review notebooks.

| Project | Validation protocol | Baseline | Improved | Submission artifact |
|---|---|---|---|---|
| P-1 | seed 42, 80/20 stratified random-row holdout | accuracy 0.0472, macro-F1 0.0038 | HOG + RBF-SVM; accuracy 1.0000, macro-F1 1.0000 | 7,172 rows; schema, IDs, labels, missing values, SHA-256 verified |
| P-2 | seed 42, normalized-description grouped train/calibration/holdout; threshold selected on calibration only | accuracy 0.9525, F1 0.0000, recall 0.0000 | word+character TF-IDF + class-weighted LinearSVC; accuracy 0.9896, F1 0.8879, recall 0.8655, AP 0.9187 | 5,364 rows; schema, IDs, labels, missing values, SHA-256 verified |
| P-3 | seed 42, 80/20 stratified holdout; SVM C selected by training-only five-fold CV | accuracy 0.1038, macro-F1 0.0188 | acoustic summaries + RBF-SVM; accuracy 0.8142, macro-F1 0.8108 | 300 rows; schema, IDs, genres, missing values, SHA-256 verified |

## Data-quality limits

- P-1 has no signer or source-group ID. The perfect random-row holdout score
  may be optimistic because augmented or near-duplicate source images cannot be
  grouped reliably.
- P-2 contains 2,635 rows in repeated-description groups. The final published
  score uses group-aware splitting; an earlier random-row result was discarded.
- P-3 has no artist or track-family group metadata, so artist-conditioned
  evaluation was not possible.
- P-2 is highly imbalanced (4.75% positive). Accuracy alone is misleading;
  balanced accuracy, F1, precision, recall, and average precision are reported.

## Verification boundary

The generated CSV files are structurally ready for upload. Kaggle credentials
and an authenticated competition session were unavailable, so upload history,
official metric, leaderboard score, and rank remain
`NOT_VERIFIED_NO_AUTHENTICATED_KAGGLE_SUBMISSION`.

The raw P-2 notebook remains excluded because it contains a plaintext Google
API key. The clean rerun uses no API key. The owner must revoke and replace the
exposed credential independently.
