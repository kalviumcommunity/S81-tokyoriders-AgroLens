from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .config import DEFAULT_RANDOM_STATE, DEFAULT_TEST_SIZE
from .persistence import load_pickle_typed, save_pickle


@dataclass
class PreprocessorBundle:
    scaler: StandardScaler
    feature_columns: list[str]


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split features and target into train/test subsets.

    Returns:
        X_train, X_test, y_train, y_test
    """
    try:
        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=test_size,
            random_state=random_state,
            stratify=target,
        )
    except ValueError:
        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=test_size,
            random_state=random_state,
            stratify=None,
        )
    return x_train, x_test, y_train, y_test


def fit_preprocessor(x_train: pd.DataFrame) -> PreprocessorBundle:
    """Fit a preprocessor bundle on training features only."""
    numeric_frame = x_train.select_dtypes(include="number")
    if numeric_frame.empty:
        raise ValueError("No numeric feature columns found to fit the preprocessor")

    scaler = StandardScaler()
    scaler.fit(numeric_frame)
    return PreprocessorBundle(scaler=scaler, feature_columns=numeric_frame.columns.tolist())


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
    save_pickle(bundle, output_path)


def load_preprocessor(preprocessor_path: str | Path) -> PreprocessorBundle:
    """Load a fitted preprocessor bundle from disk."""
    return load_pickle_typed(preprocessor_path, expected_type=PreprocessorBundle)


def preprocess_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
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