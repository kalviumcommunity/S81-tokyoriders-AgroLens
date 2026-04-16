from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier

from .data_loader import load_training_frame
from .evaluate import evaluate_model
from .feature_engineering import engineer_features
from .feature_inspection import (
    build_feature_distribution_report,
    maybe_save_distribution_plots,
    save_feature_distribution_report,
)
from .config import (
    DEFAULT_EVALUATION_REPORT_PATH,
    DEFAULT_EXPERIMENT_LOG_PATH,
    DEFAULT_DISTRIBUTION_FIGURES_DIR,
    DEFAULT_DISTRIBUTION_REPORT_PATH,
    DEFAULT_MODEL_PATH,
    DEFAULT_PREPROCESSOR_PATH,
    DEFAULT_RANDOM_STATE,
    DEFAULT_TEST_SIZE,
    ALL_FEATURES,
    CATEGORICAL_FEATURES,
    EXCLUDED_COLUMNS,
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
    TARGET_SOURCE_COLUMN,
)
from .model import save_model, train_model
from .problem_type import infer_supervised_problem_type, recommended_metrics
from .preprocessing import (
    fit_preprocessor,
    save_preprocessor,
    separate_features_and_target,
    split_data,
    transform_features,
)


def _derive_binary_target(values: pd.Series) -> pd.Series:
    threshold = float(values.median())
    return (values >= threshold).astype(int).rename("target")


def _prepare_features_and_target(
    dataframe: pd.DataFrame,
    target_column: str | None,
) -> tuple[pd.DataFrame, pd.Series]:
    if target_column is not None:
        if target_column not in dataframe.columns:
            raise ValueError(f"Column '{target_column}' not found in dataset")
        # When an explicit target is supplied, treat all remaining columns as candidate features.
        features = dataframe.drop(columns=[target_column])
        return features, dataframe[target_column]

    # Demo-friendly default: derive a binary target from yield_kg when available.
    if TARGET_SOURCE_COLUMN in dataframe.columns:
        derived_target = _derive_binary_target(dataframe[TARGET_SOURCE_COLUMN]).rename(TARGET_COLUMN)

        # Explicit, reviewable feature selection (5.14)
        available_features = [col for col in ALL_FEATURES if col in dataframe.columns]
        if not available_features:
            raise ValueError("No configured feature columns found in the dataset")

        working = dataframe.copy()
        working[TARGET_COLUMN] = derived_target

        # Enforce that leakage columns are not used as features
        features, target = separate_features_and_target(
            working,
            target_column=TARGET_COLUMN,
            feature_columns=available_features,
            excluded_columns=EXCLUDED_COLUMNS,
            verbose=False,
        )
        return features, target

    raise ValueError(
        "target_column must be provided for training when the dataset has no 'yield_kg' column"
    )


def _synthetic_training_data(
    *,
    n_samples: int = 500,
    n_features: int = 8,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    features_array, target_array = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=max(2, n_features // 2),
        n_redundant=max(0, n_features // 4),
        n_classes=2,
        random_state=random_state,
    )
    feature_names = [f"feature_{index}" for index in range(n_features)]
    features = pd.DataFrame(features_array, columns=feature_names)
    target = pd.Series(target_array, name="target")
    return features, target


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
    distribution_report_path: str | Path | None = DEFAULT_DISTRIBUTION_REPORT_PATH,
    distribution_figures_dir: str | Path | None = DEFAULT_DISTRIBUTION_FIGURES_DIR,
    evaluation_report_path: str | Path | None = DEFAULT_EVALUATION_REPORT_PATH,
    experiment_log_path: str | Path | None = DEFAULT_EXPERIMENT_LOG_PATH,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
    time_column: str | None = None,
    numeric_scaler: str = "standard",
) -> dict[str, float | str]:
    """Train and evaluate a model, then persist model and preprocessing artifacts."""
    try:
        raw_frame = load_training_frame(data_path)
        features, target = _prepare_features_and_target(raw_frame, target_column)
    except FileNotFoundError:
        features, target = _synthetic_training_data()

    inferred = infer_supervised_problem_type(target)
    if inferred.kind != "classification":
        metrics = ", ".join(recommended_metrics(inferred))
        raise ValueError(
            "This training pipeline is configured for classification targets, but the provided target "
            f"looks like {inferred.kind} ({inferred.subtype}). "
            f"Recommended metrics for that target type: {metrics}. "
            "Fix: choose a categorical target for classification, or implement a regression model/evaluator."
        )

    engineered_features = engineer_features(features)

    x_train, x_test, y_train, y_test = split_data(
        engineered_features,
        target,
        test_size=test_size,
        random_state=random_state,
        time_column=time_column,
    )

    numeric_columns_for_inspection = x_train.select_dtypes(include="number").columns.tolist()

    if distribution_report_path is not None:
        report = build_feature_distribution_report(
            x_train,
            target=y_train,
        )
        save_feature_distribution_report(report, distribution_report_path)

    if distribution_figures_dir is not None:
        maybe_save_distribution_plots(
            x_train,
            numeric_features=numeric_columns_for_inspection,
            output_dir=distribution_figures_dir,
        )

    preprocessor_bundle = fit_preprocessor(
        x_train,
        numeric_features=NUMERICAL_FEATURES,
        categorical_features=CATEGORICAL_FEATURES,
        numeric_scaler=numeric_scaler,
    )
    x_train_prepared = transform_features(x_train, preprocessor_bundle)
    x_test_prepared = transform_features(x_test, preprocessor_bundle)

    baseline = DummyClassifier(strategy="most_frequent", random_state=random_state)
    baseline.fit(x_train_prepared, y_train)
    baseline_metrics = evaluate_model(baseline, x_test_prepared, y_test)

    trained_model = train_model(x_train_prepared, y_train)
    metrics = evaluate_model(trained_model, x_test_prepared, y_test)

    metrics["baseline_strategy"] = "most_frequent"
    metrics["baseline_classification_report"] = baseline_metrics["classification_report"]
    for key in ("accuracy", "precision", "recall", "f1_score"):
        metrics[f"baseline_{key}"] = float(baseline_metrics[key])
        metrics[f"improvement_{key}"] = float(metrics[key]) - float(baseline_metrics[key])

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