from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class PreprocessorBundle:
    scaler: StandardScaler
    feature_columns: list[str]


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split features and target into train/test subsets.

    Returns:
        X_train, X_test, y_train, y_test
    """
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )
    return x_train, x_test, y_train, y_test


def fit_preprocessor(x_train: pd.DataFrame) -> PreprocessorBundle:
    """Fit a preprocessor bundle on training features only."""
    scaler = StandardScaler()
    scaler.fit(x_train)
    return PreprocessorBundle(scaler=scaler, feature_columns=x_train.columns.tolist())


def transform_features(features: pd.DataFrame, bundle: PreprocessorBundle) -> pd.DataFrame:
    """Transform features with a fitted preprocessor bundle."""
    missing_columns = set(bundle.feature_columns) - set(features.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input data is missing required feature columns: {missing}")

    ordered = features[bundle.feature_columns]
    transformed = bundle.scaler.transform(ordered)
    return pd.DataFrame(transformed, columns=bundle.feature_columns, index=ordered.index)


def save_preprocessor(bundle: PreprocessorBundle, output_path: str | Path) -> None:
    """Persist a fitted preprocessor bundle to disk."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output_file:
        pickle.dump(bundle, output_file)


def load_preprocessor(preprocessor_path: str | Path) -> PreprocessorBundle:
    """Load a fitted preprocessor bundle from disk."""
    source = Path(preprocessor_path)
    if not source.exists():
        raise FileNotFoundError(f"Preprocessor not found: {source}")

    with source.open("rb") as input_file:
        bundle = pickle.load(input_file)

    if not isinstance(bundle, PreprocessorBundle):
        raise TypeError("Loaded preprocessor is not a PreprocessorBundle")

    return bundle


def preprocess_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, StandardScaler]:
    """Backward-compatible helper for split+fit+transform.

    Returns:
        X_train, X_test, y_train, y_test, fitted_scaler
    """
    x_train, x_test, y_train, y_test = split_data(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
    )
    bundle = fit_preprocessor(x_train)
    x_train_scaled = transform_features(x_train, bundle)
    x_test_scaled = transform_features(x_test, bundle)

    return x_train_scaled, x_test_scaled, y_train, y_test, bundle.scaler