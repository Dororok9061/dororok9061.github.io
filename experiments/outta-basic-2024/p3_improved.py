"""P3: cached acoustic features + tuned RBF-SVM genre classifier."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


SEED = 42
SAMPLE_RATE = 22050
DURATION_SECONDS = 30.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize(array: np.ndarray) -> np.ndarray:
    return np.concatenate([np.mean(array, axis=1), np.std(array, axis=1)])


def extract_feature(path: Path) -> np.ndarray:
    signal, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True, duration=DURATION_SECONDS)
    if signal.size == 0:
        raise ValueError(f"Empty audio: {path}")
    signal, _ = librosa.effects.trim(signal, top_db=40)
    stft = np.abs(librosa.stft(signal, n_fft=2048, hop_length=512))
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=20)
    delta = librosa.feature.delta(mfcc)
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    spectral = np.vstack(
        [
            librosa.feature.spectral_centroid(S=stft, sr=sr),
            librosa.feature.spectral_bandwidth(S=stft, sr=sr),
            librosa.feature.spectral_rolloff(S=stft, sr=sr),
            librosa.feature.zero_crossing_rate(signal),
            librosa.feature.rms(S=stft),
        ]
    )
    return np.concatenate([summarize(mfcc), summarize(delta), summarize(chroma), summarize(contrast), summarize(spectral)]).astype(np.float32)


def feature_matrix(paths: list[Path], cache: Path) -> np.ndarray:
    names = np.asarray([str(path.resolve()) for path in paths])
    if cache.exists():
        stored = np.load(cache, allow_pickle=False)
        if np.array_equal(stored["names"], names):
            return stored["features"]
    features = np.asarray([extract_feature(path) for path in paths], dtype=np.float32)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, names=names, features=features)
    return features


def multiclass_metrics(y_true: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "macro_f1": float(f1_score(y_true, pred, average="macro")),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    train_root = args.data_root / "train" / "train"
    test_root = args.data_root / "test" / "test"
    sample_path = args.data_root / "sample_submission.csv"
    train_paths = sorted(train_root.glob("*/*.wav"))
    test_paths = sorted(test_root.glob("*.wav"))
    sample = pd.read_csv(sample_path)
    if len(test_paths) != len(sample):
        raise ValueError("Test audio and sample-submission row counts differ")

    y = np.asarray([path.parent.name for path in train_paths])
    train_features = feature_matrix(train_paths, args.output_dir / "p3_train_features.npz")
    test_features = feature_matrix(test_paths, args.output_dir / "p3_test_features.npz")
    x_train, x_valid, y_train, y_valid = train_test_split(
        train_features, y, test_size=0.2, random_state=SEED, stratify=y
    )

    baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
    baseline_metrics = multiclass_metrics(y_valid, baseline.predict(x_valid))

    pipeline = make_pipeline(StandardScaler(), SVC(kernel="rbf", gamma="scale"))
    search = GridSearchCV(
        pipeline,
        {"svc__C": [1.0, 3.0, 10.0, 30.0]},
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED),
        scoring="accuracy",
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    improved_metrics = multiclass_metrics(y_valid, search.predict(x_valid))

    best_model = search.best_estimator_.fit(train_features, y)
    predictions = best_model.predict(test_features)
    submission = sample.copy()
    submission["genre"] = predictions
    submission_path = args.output_dir / "submission_p3_improved.csv"
    submission.to_csv(submission_path, index=False)

    report = {
        "project": "OUTTA Basic P3",
        "evidence_status": "LOCAL_STRATIFIED_HOLDOUT_REPRODUCED",
        "leaderboard_status": "NOT_VERIFIED_NO_AUTHENTICATED_KAGGLE_SUBMISSION",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "data": {
            "train_files": len(train_paths),
            "test_files": len(test_paths),
            "classes": int(np.unique(y).size),
            "sample_submission_sha256": sha256(sample_path),
        },
        "audio": {"sample_rate": SAMPLE_RATE, "duration_seconds": DURATION_SECONDS},
        "split": {"type": "stratified_holdout", "validation_fraction": 0.2},
        "baseline": {"model": "most_frequent", **baseline_metrics},
        "improved": {
            "model": "MFCC+delta+chroma+spectral summaries + StandardScaler + RBF-SVM",
            "selected_parameters": search.best_params_,
            "training_cv_accuracy": float(search.best_score_),
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
            "librosa": librosa.__version__,
        },
    }
    report_path = args.output_dir / "p3_results.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
