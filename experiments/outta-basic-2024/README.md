# OUTTA Basic 2024 reproducible reruns

This directory contains clean-room rerun scripts derived from the task intent in
the user's course notebooks. The supplied notebooks remain unchanged and are not
published because they include course starter material; P2 also contained a
plaintext API key.

The scripts read datasets from paths supplied at runtime, create a stratified
holdout, compare a trivial baseline with an improved model, fit the selected
pipeline on all labelled rows, and write a Kaggle-compatible CSV plus a compact
JSON report. Dataset files, fitted models, caches, and generated submissions are
excluded from Git.

The reports are local validation evidence, not Kaggle leaderboard evidence.
Uploading requires the account owner's authenticated Kaggle session.

```powershell
$python = 'python'

& $python p1_improved.py --data-root 'C:\path\to\2024-outta-basic-p-1' --output-dir '.\work\p1'
& $python p2_improved.py --train-csv 'C:\path\to\train.csv' --test-csv 'C:\path\to\test.csv' --sample-csv 'C:\path\to\sample_submission.csv' --output-dir '.\work\p2'
& $python p3_improved.py --data-root 'C:\path\to\2024-outta-basic-p-3' --output-dir '.\work\p3'
```

Dependencies are pinned by major/minor intent in `requirements.txt`; the exact
versions used by the verified rerun are recorded in each result JSON.
