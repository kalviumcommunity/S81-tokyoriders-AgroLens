from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyRegressor

from .config import (
    ALL_FEATURES,
    CATEGORICAL_FEATURES,
    DEFAULT_RANDOM_STATE,
    DEFAULT_REGRESSION_EVALUATION_REPORT_PATH,
    DEFAULT_REGRESSION_EXPERIMENT_LOG_PATH,
    DEFAULT_REGRESSION_MODEL_PATH,
    DEFAULT_REGRESSION_PREPROCESSOR_PATH,
    DEFAULT_TEST_SIZE,
    EXCLUDED_COLUMNS,
    NUMERICAL_FEATURES,
    TARGET_SOURCE_COLUMN,
)
from .data_loader import load_training_frame
from .evaluate_regression import evaluate_regression_model
from .feature_engineering import engineer_features
from .preprocessing import (
    fit_preprocessor,
    save_preprocessor,
    separate_features_and_target,
    split_data,
    transform_features,
)
from .problem_type import infer_supervised_problem_type, recommended_metrics
from .regression_model import save_regression_model, train_regression_model


def _prepare_features_and_target(
    dataframe: pd.DataFrame,
    target_column: str | None,
) -> tuple[pd.DataFrame, pd.Series]:
    chosen_target = target_column or TARGET_SOURCE_COLUMN
    if chosen_target not in dataframe.columns:
        raise ValueError(f"Column '{chosen_target}' not found in dataset")

    available_features = [col for col in ALL_FEATURES if col in dataframe.columns]
    if not available_features:
        raise ValueError("No configured feature columns found in the dataset")

    return separate_features_and_target(
        dataframe,
        target_column=chosen_target,
        feature_columns=available_features,
        excluded_columns=EXCLUDED_COLUMNS,
        verbose=False,
    )


def _write_json_report(metrics: dict[str, float | str], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    sanitized: dict[str, float | str | None] = {}
    for key, value in metrics.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            sanitized[key] = None
        else:
            sanitized[key] = value

    with destination.open("w", encoding="utf-8") as file_handle:
        json.dump(sanitized, file_handle, indent=2, ensure_ascii=False, allow_nan=False)


def _append_regression_experiment_log(
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
        "rmse": metrics.get("rmse"),
        "mae": metrics.get("mae"),
        "r2": metrics.get("r2"),
    }

    file_exists = destination.exists()
    with destination.open("a", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def run_regression_training_pipeline(
    data_path: str | None = None,
    target_column: str | None = None,
    *,
    model_output_path: str | Path = DEFAULT_REGRESSION_MODEL_PATH,
    preprocessor_output_path: str | Path = DEFAULT_REGRESSION_PREPROCESSOR_PATH,
    evaluation_report_path: str | Path | None = DEFAULT_REGRESSION_EVALUATION_REPORT_PATH,
    experiment_log_path: str | Path | None = DEFAULT_REGRESSION_EXPERIMENT_LOG_PATH,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
    time_column: str | None = None,
    numeric_scaler: str = "standard",
    baseline_strategy: str = "mean",
) -> dict[str, float | str]:
    """Train and evaluate a Linear Regression model with a constant baseline."""
    raw_frame = load_training_frame(data_path)
    features, target = _prepare_features_and_target(raw_frame, target_column)

    inferred = infer_supervised_problem_type(target)
    if inferred.kind != "regression" and not pd.api.types.is_numeric_dtype(target):
        metrics = ", ".join(recommended_metrics(inferred))
        raise ValueError(
            "This regression pipeline expects a numeric target, but the provided target "
            f"looks like {inferred.kind} ({inferred.subtype}). "
            f"Recommended metrics for that target type: {metrics}."
        )

    engineered_features = engineer_features(features)

    x_train, x_test, y_train, y_test = split_data(
        engineered_features,
        target,
        test_size=test_size,
        random_state=random_state,
        time_column=time_column,
    )

    preprocessor_bundle = fit_preprocessor(
        x_train,
        numeric_features=NUMERICAL_FEATURES,
        categorical_features=CATEGORICAL_FEATURES,
        numeric_scaler=numeric_scaler,
    )
    x_train_prepared = transform_features(x_train, preprocessor_bundle)
    x_test_prepared = transform_features(x_test, preprocessor_bundle)

    baseline = DummyRegressor(strategy=baseline_strategy)
    baseline.fit(x_train_prepared, y_train)
    baseline_metrics = evaluate_regression_model(baseline, x_test_prepared, y_test)

    trained_model = train_regression_model(x_train_prepared, y_train)
    metrics = evaluate_regression_model(trained_model, x_test_prepared, y_test)

    metrics["baseline_strategy"] = baseline_strategy
    metrics["baseline_rmse"] = float(baseline_metrics["rmse"])
    metrics["baseline_mae"] = float(baseline_metrics["mae"])
    metrics["baseline_r2"] = float(baseline_metrics["r2"])
    metrics["improvement_rmse"] = float(baseline_metrics["rmse"]) - float(metrics["rmse"])
    metrics["improvement_mae"] = float(baseline_metrics["mae"]) - float(metrics["mae"])
    metrics["improvement_r2"] = float(metrics["r2"]) - float(baseline_metrics["r2"])

    save_regression_model(trained_model, model_output_path)
    save_preprocessor(preprocessor_bundle, preprocessor_output_path)

    if evaluation_report_path is not None:
        _write_json_report(metrics, evaluation_report_path)

    if experiment_log_path is not None:
        _append_regression_experiment_log(
            log_path=experiment_log_path,
            model_path=model_output_path,
            preprocessor_path=preprocessor_output_path,
            metrics=metrics,
        )

    return metrics
