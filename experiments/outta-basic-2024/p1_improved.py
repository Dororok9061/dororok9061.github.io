"""P1: HOG + RBF-SVM sign-language image classifier."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from skimage.feature import hog
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


SEED = 42


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hog_features(values: np.ndarray) -> np.ndarray:
    images = values.reshape(-1, 28, 28).astype(np.float32) / 255.0
    return np.asarray(
        [
            hog(
                image,
                orientations=9,
                pixels_per_cell=(4, 4),
                cells_per_block=(2, 2),
                block_norm="L2-Hys",
                feature_vector=True,
            )
            for image in images
        ],
        dtype=np.float32,
    )


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    train_path = args.data_root / "train.csv"
    test_path = args.data_root / "test.csv"
    sample_path = args.data_root / "sample_submission.csv"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    sample = pd.read_csv(sample_path)
    if train.shape[1] != 785 or test.shape[1] != 784:
        raise ValueError("Expected one label plus 784 pixels for 28x28 images")
    if len(test) != len(sample):
        raise ValueError("Test and sample-submission row counts differ")

    y = train.pop("label").to_numpy()
    features = hog_features(train.to_numpy())
    test_features = hog_features(test.to_numpy())
    x_train, x_valid, y_train, y_valid = train_test_split(
        features, y, test_size=0.2, random_state=SEED, stratify=y
    )

    baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
    baseline_metrics = metrics(y_valid, baseline.predict(x_valid))

    model = SVC(C=10.0, kernel="rbf", gamma="scale", cache_size=2048)
    model.fit(x_train, y_train)
    improved_metrics = metrics(y_valid, model.predict(x_valid))

    model.fit(features, y)
    predictions = model.predict(test_features)
    submission = sample.copy()
    submission["label"] = predictions.astype(int)
    submission_path = args.output_dir / "submission_p1_improved.csv"
    submission.to_csv(submission_path, index=False)

    report = {
        "project": "OUTTA Basic P1",
        "evidence_status": "LOCAL_STRATIFIED_HOLDOUT_REPRODUCED",
        "leaderboard_status": "NOT_VERIFIED_NO_AUTHENTICATED_KAGGLE_SUBMISSION",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "data": {
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "features": 784,
            "classes": int(np.unique(y).size),
            "train_sha256": sha256(train_path),
            "test_sha256": sha256(test_path),
        },
        "split": {"type": "stratified_holdout", "validation_fraction": 0.2},
        "baseline": {"model": "most_frequent", **baseline_metrics},
        "improved": {
            "model": "HOG(9,4x4,2x2)+RBF-SVM(C=10)",
            **improved_metrics,
        },
        "submission": {
            "path": submission_path.name,
            "rows": int(len(submission)),
            "sha256": sha256(submission_path),
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
    }
    report_path = args.output_dir / "p1_results.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
