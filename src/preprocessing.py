from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

from .config import DEFAULT_RANDOM_STATE, DEFAULT_TEST_SIZE
from .persistence import load_pickle_typed, save_pickle


def validate_feature_target_definition(
    dataframe: pd.DataFrame,
    *,
    target_column: str,
    feature_columns: list[str],
    excluded_columns: list[str] | None = None,
) -> None:
    """Validate that feature/target definitions are consistent and leak-free."""
    if target_column not in dataframe.columns:
        raise ValueError(f"Target '{target_column}' not found in dataframe")

    if target_column in feature_columns:
        raise ValueError("Target leaked into features!")

    if excluded_columns:
        overlap = set(excluded_columns) & set(feature_columns)
        if overlap:
            overlapped = ", ".join(sorted(overlap))
            raise ValueError(f"Excluded columns found in feature list: {overlapped}")

    missing_features = set(feature_columns) - set(dataframe.columns)
    if missing_features:
        missing = ", ".join(sorted(missing_features))
        raise ValueError(f"Features not found in dataframe: {missing}")


def separate_features_and_target(
    dataframe: pd.DataFrame,
    *,
    target_column: str,
    feature_columns: list[str],
    excluded_columns: list[str] | None = None,
    verbose: bool = False,
) -> tuple[pd.DataFrame, pd.Series]:
    """Separate X (features) and y (target) explicitly.

    This is intended to run early in the pipeline before any fitting.
    """
    validate_feature_target_definition(
        dataframe,
        target_column=target_column,
        feature_columns=feature_columns,
        excluded_columns=excluded_columns,
    )

    x = dataframe[feature_columns]
    y = dataframe[target_column]

    if verbose:
        print(f"Features: {x.shape}")
        print(f"Target: {y.shape}")
        try:
            print(f"Target distribution:\n{y.value_counts(normalize=True)}")
        except Exception:
            pass

    return x, y


@dataclass
class PreprocessorBundle:
    transformer: ColumnTransformer
    input_columns: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
    time_column: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split features and target into train/test subsets.

    - Default (classification-friendly): random split with stratification when possible.
    - Time-series option: set time_column to split chronologically (no shuffle).

    Returns:
        X_train, X_test, y_train, y_test
    """
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")

    if len(features) != len(target):
        raise ValueError("Features and target must have the same number of rows")

    if time_column is not None:
        if time_column not in features.columns:
            raise ValueError(f"time_column '{time_column}' not found in features")
        if not features.index.isin(target.index).all():
            raise ValueError("Target index does not align with feature index for time-based split")

        aligned_target = target.reindex(features.index)
        time_values = features[time_column]
        if time_values.isna().any():
            raise ValueError(f"time_column '{time_column}' contains missing values")

        if pd.api.types.is_object_dtype(time_values) or pd.api.types.is_string_dtype(time_values):
            time_values = pd.to_datetime(time_values, errors="raise")

        ordered_index = time_values.sort_values(kind="mergesort").index
        ordered_features = features.loc[ordered_index]
        ordered_target = aligned_target.loc[ordered_index]

        split_at = int(len(ordered_features) * (1 - test_size))
        if split_at <= 0 or split_at >= len(ordered_features):
            raise ValueError("test_size results in an empty train or test split")

        x_train = ordered_features.iloc[:split_at]
        x_test = ordered_features.iloc[split_at:]
        y_train = ordered_target.iloc[:split_at]
        y_test = ordered_target.iloc[split_at:]
        return x_train, x_test, y_train, y_test

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


def fit_preprocessor(
    x_train: pd.DataFrame,
    *,
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    numeric_scaler: str = "standard",
) -> PreprocessorBundle:
    """Fit a preprocessor bundle on training features only.

    - Numeric columns are scaled.
    - Categorical columns are one-hot encoded.

    numeric_scaler:
        - "standard" (default): StandardScaler (mean=0, std=1)
        - "minmax": MinMaxScaler (range [0, 1])
    """
    if numeric_features is None:
        numeric_columns = x_train.select_dtypes(include="number").columns.tolist()
    else:
        numeric_columns = [col for col in numeric_features if col in x_train.columns]

    if categorical_features is None:
        categorical_columns = x_train.select_dtypes(exclude="number").columns.tolist()
    else:
        categorical_columns = [col for col in categorical_features if col in x_train.columns]

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

    transformer = ColumnTransformer(
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
    transformer.fit(x_train)

    input_columns = numeric_columns + categorical_columns
    return PreprocessorBundle(
        transformer=transformer,
        input_columns=input_columns,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
    )


def transform_features(features: pd.DataFrame, bundle: PreprocessorBundle) -> pd.DataFrame:
    """Transform features with a fitted preprocessor bundle."""
    missing_columns = set(bundle.input_columns) - set(features.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input data is missing required feature columns: {missing}")

    ordered = features[bundle.input_columns]
    transformed = bundle.transformer.transform(ordered)
    output_columns = list(bundle.transformer.get_feature_names_out())
    return pd.DataFrame(transformed, columns=output_columns, index=ordered.index)


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
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, StandardScaler | MinMaxScaler | None]:
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

    # Backward-compatible return: last value used to be a scaler.
    # We now return a StandardScaler when the numeric transformer exists.
    scaler = None
    if bundle.numeric_columns:
        scaler = bundle.transformer.named_transformers_.get("num")
    return x_train_scaled, x_test_scaled, y_train, y_test, scaler