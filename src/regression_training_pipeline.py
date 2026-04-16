from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

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


def _build_unfitted_preprocessor(
    features: pd.DataFrame,
    *,
    numeric_scaler: str,
) -> ColumnTransformer:
    numeric_columns = [col for col in NUMERICAL_FEATURES if col in features.columns]
    categorical_columns = [col for col in CATEGORICAL_FEATURES if col in features.columns]

    overlap = set(numeric_columns) & set(categorical_columns)
    if overlap:
        overlapped = ", ".join(sorted(overlap))
        raise ValueError(f"Features cannot be both numeric and categorical: {overlapped}")

    if not numeric_columns and not categorical_columns:
        raise ValueError("No usable feature columns found to fit the preprocessor")

    if numeric_scaler == "standard":
        numeric_transformer = StandardScaler()
    elif numeric_scaler == "minmax":
        numeric_transformer = MinMaxScaler()
    else:
        raise ValueError("numeric_scaler must be either 'standard' or 'minmax'")

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_columns),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_columns,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def _write_json_report(metrics: dict[str, float | str | int | None], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    sanitized: dict[str, float | str | int | None] = {}
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
    metrics: dict[str, float | str | int | None],
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
    cv_folds: int = 5,
) -> dict[str, float | str | int | None]:
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

    metrics: dict[str, float | str | int | None] = {}

    # Cross-validation (computed on training data only; preprocessing is fitted inside each fold).
    if cv_folds >= 2 and len(x_train) >= 2:
        n_splits = min(int(cv_folds), int(len(x_train)))
        if n_splits >= 2:
            cv_preprocessor = _build_unfitted_preprocessor(x_train, numeric_scaler=numeric_scaler)
            cv_model = LinearRegression()
            cv_pipeline = Pipeline(
                [
                    ("preprocessor", cv_preprocessor),
                    ("model", cv_model),
                ]
            )

            cv = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

            # MAE (negated by sklearn; flip sign for reporting).
            cv_mae_scores = -cross_val_score(
                cv_pipeline,
                x_train,
                y_train,
                cv=cv,
                scoring="neg_mean_absolute_error",
            )
            cv_mae_scores = cv_mae_scores.astype(float)
            metrics["cv_mae_mean"] = float(cv_mae_scores.mean())
            metrics["cv_mae_std"] = float(cv_mae_scores.std())

            # MSE/RMSE (MSE negated by sklearn; flip sign; RMSE is sqrt(MSE)).
            cv_mse_scores = -cross_val_score(
                cv_pipeline,
                x_train,
                y_train,
                cv=cv,
                scoring="neg_mean_squared_error",
            )
            cv_mse_scores = cv_mse_scores.astype(float)
            cv_rmse_scores = np.sqrt(cv_mse_scores)
            metrics["cv_mse_mean"] = float(cv_mse_scores.mean())
            metrics["cv_mse_std"] = float(cv_mse_scores.std())
            metrics["cv_rmse_mean"] = float(cv_rmse_scores.mean())
            metrics["cv_rmse_std"] = float(cv_rmse_scores.std())

            # R² requires at least 2 samples in each test fold.
            min_test_fold_size = int(len(x_train)) // int(n_splits)
            if min_test_fold_size >= 2:
                cv_r2_scores = cross_val_score(
                    cv_pipeline,
                    x_train,
                    y_train,
                    cv=cv,
                    scoring="r2",
                )
                cv_r2_scores = cv_r2_scores.astype(float)
                metrics["cv_r2_mean"] = float(cv_r2_scores.mean())
                metrics["cv_r2_std"] = float(cv_r2_scores.std())

            metrics["cv_folds"] = int(n_splits)

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
    model_metrics = evaluate_regression_model(trained_model, x_test_prepared, y_test)
    metrics.update(model_metrics)

    baseline_mse = float(baseline_metrics["mse"])
    model_mse = float(metrics["mse"])
    improvement_mse = baseline_mse - model_mse

    baseline_mae = float(baseline_metrics["mae"])
    model_mae = float(metrics["mae"])
    improvement_mae = baseline_mae - model_mae

    metrics["baseline_strategy"] = baseline_strategy
    metrics["baseline_mse"] = baseline_mse
    metrics["baseline_rmse"] = float(baseline_metrics["rmse"])
    metrics["baseline_mae"] = baseline_mae
    metrics["baseline_r2"] = float(baseline_metrics["r2"])

    metrics["improvement_mse"] = improvement_mse
    metrics["improvement_rmse"] = float(baseline_metrics["rmse"]) - float(metrics["rmse"])
    metrics["improvement_mae"] = improvement_mae
    metrics["improvement_r2"] = float(metrics["r2"]) - float(baseline_metrics["r2"])

    if baseline_mse != 0:
        metrics["improvement_mse_pct"] = float((improvement_mse / baseline_mse) * 100)
    else:
        metrics["improvement_mse_pct"] = None

    if baseline_mae != 0:
        metrics["improvement_mae_pct"] = float((improvement_mae / baseline_mae) * 100)
    else:
        metrics["improvement_mae_pct"] = None

    mean_target = float(y_test.mean())
    metrics["mean_target"] = mean_target
    if mean_target != 0:
        denom = abs(mean_target)
        metrics["mae_pct_of_mean_target"] = float((model_mae / denom) * 100)
        metrics["baseline_mae_pct_of_mean_target"] = float((baseline_mae / denom) * 100)
    else:
        metrics["mae_pct_of_mean_target"] = None
        metrics["baseline_mae_pct_of_mean_target"] = None

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
