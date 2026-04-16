from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression

from .config import DEFAULT_RANDOM_STATE
from .persistence import load_pickle_typed, save_pickle


def train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    max_iter: int = 1000,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> LogisticRegression:
    """Train and return a Logistic Regression classifier."""
    classifier = LogisticRegression(max_iter=max_iter, random_state=random_state)
    classifier.fit(x_train, y_train)
    return classifier


def save_model(model: LogisticRegression, output_path: str | Path) -> None:
    """Persist a trained model to disk."""
    save_pickle(model, output_path)


def load_model(model_path: str | Path) -> LogisticRegression:
    """Load a trained model from disk."""
    return load_pickle_typed(model_path, expected_type=LogisticRegression)