"""P2: secret-free TF-IDF + linear SVM fake-job classifier."""

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
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC


SEED = 42
TEXT_COLUMNS = [
    "title",
    "location",
    "department",
    "salary_range",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function",
]
FLAG_COLUMNS = ["telecommuting", "has_company_logo", "has_questions"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assemble_text(frame: pd.DataFrame) -> pd.Series:
    text = frame.reindex(columns=TEXT_COLUMNS).fillna("").astype(str).agg(" ".join, axis=1)
    flags = frame.reindex(columns=FLAG_COLUMNS).fillna(0).astype(int)
    flag_text = flags.apply(
        lambda row: " ".join(f"__{name}_{value}__" for name, value in row.items()), axis=1
    )
    return text + " " + flag_text


def duplicate_groups(frame: pd.DataFrame) -> np.ndarray:
    """Keep exact duplicate descriptions in one split to reduce leakage."""
    descriptions = (
        frame["description"].fillna("").astype(str).str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    )
    return np.asarray(
        [
            hashlib.sha256(value.encode("utf-8")).hexdigest() if value else f"missing-{job_id}"
            for value, job_id in zip(descriptions, frame["job_id"], strict=True)
        ]
    )


def binary_metrics(y_true: np.ndarray, pred: np.ndarray, scores: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "average_precision": float(average_precision_score(y_true, scores)),
        "roc_auc": float(roc_auc_score(y_true, scores)),
    }


def best_threshold(y_true: np.ndarray, scores: np.ndarray) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    f1 = 2 * precision[:-1] * recall[:-1] / np.maximum(precision[:-1] + recall[:-1], 1e-12)
    return float(thresholds[int(np.nanargmax(f1))])


def vectorizer() -> FeatureUnion:
    return FeatureUnion(
        [
            (
                "word",
                TfidfVectorizer(
                    strip_accents="unicode",
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.995,
                    max_features=80000,
                    sublinear_tf=True,
                ),
            ),
            (
                "char",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    min_df=3,
                    max_features=60000,
                    sublinear_tf=True,
                ),
            ),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-csv", type=Path, required=True)
    parser.add_argument("--test-csv", type=Path, required=True)
    parser.add_argument("--sample-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(args.train_csv)
    test = pd.read_csv(args.test_csv)
    sample = pd.read_csv(args.sample_csv)
    if "fraudulent" not in train or len(test) != len(sample):
        raise ValueError("Unexpected train/test/submission schema")

    y = train["fraudulent"].to_numpy(dtype=int)
    text = assemble_text(train)
    test_text = assemble_text(test)
    groups = duplicate_groups(train)
    outer = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    develop_idx, holdout_idx = next(outer.split(text, y, groups))
    x_develop, x_holdout = text.iloc[develop_idx], text.iloc[holdout_idx]
    y_develop, y_holdout = y[develop_idx], y[holdout_idx]
    groups_develop = groups[develop_idx]
    inner = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    train_rel, calibration_rel = next(inner.split(x_develop, y_develop, groups_develop))
    x_train, x_calibration = x_develop.iloc[train_rel], x_develop.iloc[calibration_rel]
    y_train, y_calibration = y_develop[train_rel], y_develop[calibration_rel]

    dummy = DummyClassifier(strategy="most_frequent").fit(np.zeros((len(y_train), 1)), y_train)
    dummy_pred = dummy.predict(np.zeros((len(y_holdout), 1)))
    baseline_metrics = binary_metrics(y_holdout, dummy_pred, dummy_pred.astype(float))

    features = vectorizer()
    train_matrix = features.fit_transform(x_train)
    calibration_matrix = features.transform(x_calibration)
    holdout_matrix = features.transform(x_holdout)
    model = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED)
    model.fit(train_matrix, y_train)
    threshold = best_threshold(y_calibration, model.decision_function(calibration_matrix))
    holdout_scores = model.decision_function(holdout_matrix)
    holdout_pred = (holdout_scores >= threshold).astype(int)
    improved_metrics = binary_metrics(y_holdout, holdout_pred, holdout_scores)

    final_features = vectorizer()
    full_matrix = final_features.fit_transform(text)
    final_model = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED)
    final_model.fit(full_matrix, y)
    test_scores = final_model.decision_function(final_features.transform(test_text))
    predictions = (test_scores >= threshold).astype(int)
    submission = sample.copy()
    submission["fraudulent"] = predictions
    submission_path = args.output_dir / "submission_p2_improved.csv"
    submission.to_csv(submission_path, index=False)

    report = {
        "project": "OUTTA Basic P2",
        "evidence_status": "LOCAL_STRATIFIED_HOLDOUT_REPRODUCED",
        "leaderboard_status": "NOT_VERIFIED_NO_AUTHENTICATED_KAGGLE_SUBMISSION",
        "secret_status": "CLEAN_RERUN_NO_API_KEY_REQUIRED",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "data": {
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "positive_rows": int(y.sum()),
            "positive_rate": float(y.mean()),
            "train_sha256": sha256(args.train_csv),
            "test_sha256": sha256(args.test_csv),
        },
        "split": {
            "type": "stratified_group_train_calibration_holdout",
            "group_key": "normalized exact description hash; missing descriptions remain unique by job_id",
            "train_rows": int(len(y_train)),
            "calibration_rows": int(len(y_calibration)),
            "holdout_rows": int(len(y_holdout)),
            "threshold_selected_on": "calibration_f1",
        },
        "baseline": {"model": "most_frequent", **baseline_metrics},
        "improved": {
            "model": "word+character TF-IDF + class-weighted LinearSVC",
            "decision_threshold": threshold,
            **improved_metrics,
        },
        "submission": {
            "path": submission_path.name,
            "rows": int(len(submission)),
            "positive_predictions": int(predictions.sum()),
            "sha256": sha256(submission_path),
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
    }
    report_path = args.output_dir / "p2_results.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
