from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import RAW_DATA_DIR


def load_csv(data_path: str | Path) -> pd.DataFrame:
    """Load a CSV from disk and return the raw dataframe.

    Responsibility: read + validate only.
    No splitting, no target derivation, no fitting, no feature engineering.
    """
    csv_path = Path(data_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    if dataframe.empty:
        raise ValueError(f"Loaded dataset is empty: {csv_path}")

    return dataframe


def load_training_frame(data_path: str | Path | None = None) -> pd.DataFrame:
    """Load raw training data as a dataframe.

    If data_path is None, uses the repository demo CSV when present.
    """
    if data_path is None:
        default_csv = RAW_DATA_DIR / "source_demo_crops_20260321.csv"
        return load_csv(default_csv)

    return load_csv(data_path)


def load_inference_frame(
    data_path: str | Path,
    target_column: str | None = None,
) -> pd.DataFrame:
    """Load feature data for inference.

    If target_column is supplied and exists, it is removed to avoid leakage.
    """
    dataframe = load_csv(data_path)
    if target_column and target_column in dataframe.columns:
        return dataframe.drop(columns=[target_column])
    return dataframe


def load_prediction_data(data_path: str | Path, target_column: str | None = None) -> pd.DataFrame:
    """Backward-compatible alias for load_inference_frame."""
    return load_inference_frame(data_path, target_column=target_column)


def load_training_data(
    data_path: str | Path | None = None,
    target_column: str | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """Legacy helper returning (features, target).

    Prefer using:
    - load_training_frame() in the data loading layer, and
    - target/label handling inside the training layer.
    """
    dataframe = load_training_frame(data_path)
    if target_column is None:
        raise ValueError("target_column must be provided when using load_training_data")
    if target_column not in dataframe.columns:
        raise ValueError(f"Column '{target_column}' not found in dataset")
    return dataframe.drop(columns=[target_column]), dataframe[target_column]


def load_data(
    data_path: str | Path | None = None,
    target_column: str | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """Backward-compatible alias for load_training_data."""
    return load_training_data(
        data_path=data_path,
        target_column=target_column,
    )