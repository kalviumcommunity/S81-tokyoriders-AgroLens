from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification


def load_data(
    data_path: str | Path | None = None,
    target_column: str | None = None,
    *,
    n_samples: int = 500,
    n_features: int = 8,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """Load a dataset from CSV or generate a synthetic fallback dataset.

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