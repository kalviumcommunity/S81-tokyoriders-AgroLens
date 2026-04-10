from __future__ import annotations

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