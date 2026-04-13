from __future__ import annotations

from pathlib import Path

import pandas as pd

from .data_loader import load_prediction_data
from .feature_engineering import engineer_features
from .model import load_model
from .predict import predict
from .preprocessing import load_preprocessor, transform_features


def run_prediction_pipeline(
    data_path: str | Path,
    *,
    model_path: str | Path = "outputs/models/model.pkl",
    preprocessor_path: str | Path = "outputs/models/preprocessor.pkl",
    target_column: str | None = None,
    output_path: str | Path | None = "outputs/reports/predictions.csv",
) -> pd.DataFrame:
    """Run inference using persisted model and preprocessing artifacts."""
    raw_features = load_prediction_data(data_path, target_column=target_column)
    engineered_features = engineer_features(raw_features)

    preprocessor_bundle = load_preprocessor(preprocessor_path)
    prepared_features = transform_features(engineered_features, preprocessor_bundle)

    trained_model = load_model(model_path)
    predictions = predict(trained_model, prepared_features)

    prediction_frame = raw_features.copy()
    prediction_frame["prediction"] = predictions

    if output_path is not None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        prediction_frame.to_csv(destination, index=False)

    return prediction_frame