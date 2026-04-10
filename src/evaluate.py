from __future__ import annotations

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.base import ClassifierMixin


def evaluate_model(
    model: ClassifierMixin,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float | str]:
    """Evaluate a trained classifier and return summary metrics."""
    predictions = model.predict(x_test)
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="binary",
        zero_division=0,
    )
    return {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "classification_report": classification_report(y_test, predictions),
    }