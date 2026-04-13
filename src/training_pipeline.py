from __future__ import annotations

from pathlib import Path

from .data_loader import load_training_data
from .evaluate import evaluate_model
from .feature_engineering import engineer_features
from .model import save_model, train_model
from .preprocessing import fit_preprocessor, save_preprocessor, split_data, transform_features


def run_training_pipeline(
    data_path: str | None = None,
    target_column: str | None = None,
    *,
    model_output_path: str | Path = "outputs/models/model.pkl",
    preprocessor_output_path: str | Path = "outputs/models/preprocessor.pkl",
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
    return metrics