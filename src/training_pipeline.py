from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from .data_loader import load_training_data
from .evaluate import evaluate_model
from .feature_engineering import engineer_features
from .config import (
    DEFAULT_EVALUATION_REPORT_PATH,
    DEFAULT_EXPERIMENT_LOG_PATH,
    DEFAULT_MODEL_PATH,
    DEFAULT_PREPROCESSOR_PATH,
)
from .model import save_model, train_model
from .preprocessing import fit_preprocessor, save_preprocessor, split_data, transform_features


def _write_json_report(metrics: dict[str, float | str], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file_handle:
        json.dump(metrics, file_handle, indent=2, ensure_ascii=False)


def _append_experiment_log(
    *,
    log_path: str | Path,
    model_path: str | Path,
    preprocessor_path: str | Path,
    metrics: dict[str, float | str],
) -> None:
    destination = Path(log_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_path": str(Path(model_path)),
        "preprocessor_path": str(Path(preprocessor_path)),
        "accuracy": metrics.get("accuracy"),
        "precision": metrics.get("precision"),
        "recall": metrics.get("recall"),
        "f1_score": metrics.get("f1_score"),
    }

    file_exists = destination.exists()
    with destination.open("a", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def run_training_pipeline(
    data_path: str | None = None,
    target_column: str | None = None,
    *,
    model_output_path: str | Path = DEFAULT_MODEL_PATH,
    preprocessor_output_path: str | Path = DEFAULT_PREPROCESSOR_PATH,
    evaluation_report_path: str | Path | None = DEFAULT_EVALUATION_REPORT_PATH,
    experiment_log_path: str | Path | None = DEFAULT_EXPERIMENT_LOG_PATH,
) -> dict[str, float | str]:
    """Train and evaluate a model, then persist model and preprocessing artifacts."""
    features, target = load_training_data(data_path=data_path, target_column=target_column)
    engineered_features = engineer_features(features)

    x_train, x_test, y_train, y_test = split_data(engineered_features, target)
    preprocessor_bundle = fit_preprocessor(x_train)
    x_train_prepared = transform_features(x_train, preprocessor_bundle)
    x_test_prepared = transform_features(x_test, preprocessor_bundle)

    trained_model = train_model(x_train_prepared, y_train)
    metrics = evaluate_model(trained_model, x_test_prepared, y_test)

    save_model(trained_model, model_output_path)
    save_preprocessor(preprocessor_bundle, preprocessor_output_path)

    if evaluation_report_path is not None:
        _write_json_report(metrics, evaluation_report_path)

    if experiment_log_path is not None:
        _append_experiment_log(
            log_path=experiment_log_path,
            model_path=model_output_path,
            preprocessor_path=preprocessor_output_path,
            metrics=metrics,
        )
    return metrics