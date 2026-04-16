from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

from .persistence import load_pickle_typed, save_pickle


def train_regression_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
) -> LinearRegression:
    """Train and return a Linear Regression model."""
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)
    return regressor


def save_regression_model(model: LinearRegression, output_path: str | Path) -> None:
    """Persist a trained regression model to disk."""
    save_pickle(model, output_path)


def load_regression_model(model_path: str | Path) -> LinearRegression:
    """Load a trained regression model from disk."""
    return load_pickle_typed(model_path, expected_type=LinearRegression)
