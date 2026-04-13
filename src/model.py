from __future__ import annotations

from pathlib import Path
import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression


def train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    max_iter: int = 500,
    random_state: int = 42,
) -> LogisticRegression:
    """Train and return a Logistic Regression classifier."""
    classifier = LogisticRegression(max_iter=max_iter, random_state=random_state)
    classifier.fit(x_train, y_train)
    return classifier


def save_model(model: LogisticRegression, output_path: str | Path) -> None:
    """Persist a trained model to disk."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output_file:
        pickle.dump(model, output_file)


def load_model(model_path: str | Path) -> LogisticRegression:
    """Load a trained model from disk."""
    source = Path(model_path)
    if not source.exists():
        raise FileNotFoundError(f"Model not found: {source}")

    with source.open("rb") as input_file:
        trained_model = pickle.load(input_file)

    if not isinstance(trained_model, LogisticRegression):
        raise TypeError("Loaded model is not a LogisticRegression instance")

    return trained_model