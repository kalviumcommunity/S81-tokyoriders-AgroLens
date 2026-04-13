from __future__ import annotations

import numpy as np
import pandas as pd


def engineer_features(features: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic engineered features from input features."""
    engineered = features.copy()
    numeric_columns = engineered.select_dtypes(include="number").columns.tolist()

    if len(numeric_columns) >= 2:
        first_column = numeric_columns[0]
        second_column = numeric_columns[1]

        engineered[f"{first_column}_plus_{second_column}"] = (
            engineered[first_column] + engineered[second_column]
        )
        denominator = engineered[second_column].replace(0, np.nan)
        engineered[f"{first_column}_over_{second_column}"] = (
            engineered[first_column] / denominator
        ).fillna(0.0)

    return engineered