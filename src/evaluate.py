from __future__ import annotations

import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_recall_fscore_support,
    roc_auc_score,
)


def _maybe_compute_roc_auc(
    model: ClassifierMixin,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> float | None:
    """Compute ROC-AUC for binary classification when possible."""
    if len(y_test) < 2 or y_test.nunique() != 2:
        return None

    classes = getattr(model, "classes_", None)

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(x_test)
        if getattr(proba, "ndim", 0) == 2 and proba.shape[1] == 2:
            if classes is not None and len(classes) == 2:
                pos_class = classes[1]
                pos_index = list(classes).index(pos_class)
                scores = proba[:, pos_index]
                y_true = (y_test == pos_class).astype(int)
                return float(roc_auc_score(y_true, scores))

            return float(roc_auc_score(y_test, proba[:, 1]))

    if hasattr(model, "decision_function"):
        scores = model.decision_function(x_test)
        if classes is not None and len(classes) == 2:
            pos_class = classes[1]
            y_true = (y_test == pos_class).astype(int)
            return float(roc_auc_score(y_true, scores))

        return float(roc_auc_score(y_test, scores))

    return None


def evaluate_model(
    model: ClassifierMixin,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float | str | None]:
    """Evaluate a trained classifier and return summary metrics."""
    predictions = model.predict(x_test)
    average = "binary" if y_test.nunique() == 2 else "weighted"
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average=average,
        zero_division=0,
    )

    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1_score),
        "roc_auc": _maybe_compute_roc_auc(model, x_test, y_test),
        "classification_report": classification_report(y_test, predictions, zero_division=0),
    }