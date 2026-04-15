from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification

from .config import RAW_DATA_DIR


def load_training_data(
    data_path: str | Path | None = None,
    target_column: str | None = None,
    *,
    n_samples: int = 500,
    n_features: int = 8,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """Load training data from CSV or generate a synthetic fallback dataset.

    Args:
        data_path: Optional path to a CSV file.
        target_column: Required when loading a CSV; ignored for synthetic data.
        n_samples: Number of synthetic rows when data_path is not provided.
        n_features: Number of synthetic features when data_path is not provided.
        random_state: Random seed for reproducibility.

    Returns:
        Tuple of (features, target).
    """
    if data_path is None:
        default_csv = RAW_DATA_DIR / "source_demo_crops_20260321.csv"
        if default_csv.exists():
            dataframe = pd.read_csv(default_csv)
            target_source = "yield_kg" if "yield_kg" in dataframe.columns else None
            if target_source is None:
                numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()
                if numeric_columns:
                    target_source = numeric_columns[-1]

            if target_source is not None:
                target_values = dataframe[target_source]
                threshold = float(target_values.median())
                target = (target_values >= threshold).astype(int).rename("target")
                features = dataframe.drop(columns=[target_source])
                return features, target

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

    csv_path = Path(data_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    if target_column is None:
        raise ValueError("target_column must be provided when loading from CSV")
    if target_column not in dataframe.columns:
        raise ValueError(f"Column '{target_column}' not found in dataset")

    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column]
    return features, target


def load_prediction_data(
    data_path: str | Path,
    target_column: str | None = None,
) -> pd.DataFrame:
    """Load feature data for inference.

    If target_column is supplied and exists, it is removed to avoid leakage.
    """
    csv_path = Path(data_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    if target_column and target_column in dataframe.columns:
        return dataframe.drop(columns=[target_column])
    return dataframe


def load_data(
    data_path: str | Path | None = None,
    target_column: str | None = None,
    *,
    n_samples: int = 500,
    n_features: int = 8,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """Backward-compatible alias for load_training_data."""
    return load_training_data(
        data_path=data_path,
        target_column=target_column,
        n_samples=n_samples,
        n_features=n_features,
        random_state=random_state,
    )