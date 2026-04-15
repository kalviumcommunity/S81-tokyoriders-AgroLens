from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

ProblemKind = Literal["classification", "regression"]
ClassificationSubtype = Literal["binary", "multiclass", "multilabel"]
RegressionSubtype = Literal["continuous", "count"]


@dataclass(frozen=True)
class SupervisedProblemType:
    kind: ProblemKind
    subtype: str
    n_unique: int
    dtype: str
    notes: str = ""


def _is_multilabel_like(y: pd.Series) -> bool:
    """Heuristic: values look like collections of labels.

    We keep this conservative; most datasets will not be multi-label.
    """
    sample = y.dropna().head(10)
    if sample.empty:
        return False
    return all(isinstance(value, (list, tuple, set)) for value in sample)


def infer_supervised_problem_type(y: pd.Series) -> SupervisedProblemType:
    """Infer supervised learning problem type from a target series.

    This is a best-effort heuristic used for guardrails and documentation.
    """
    if not isinstance(y, pd.Series):
        y = pd.Series(y)

    y_non_null = y.dropna()
    n_unique = int(y_non_null.nunique()) if not y_non_null.empty else 0
    dtype = str(y.dtype)

    if _is_multilabel_like(y_non_null):
        return SupervisedProblemType(
            kind="classification",
            subtype="multilabel",
            n_unique=n_unique,
            dtype=dtype,
            notes="Target values look like label collections.",
        )

    # Object/category/bool are almost always classification targets.
    if pd.api.types.is_bool_dtype(y) or pd.api.types.is_object_dtype(y) or pd.api.types.is_categorical_dtype(y):
        subtype: ClassificationSubtype = "binary" if n_unique <= 2 else "multiclass"
        return SupervisedProblemType(
            kind="classification",
            subtype=subtype,
            n_unique=n_unique,
            dtype=dtype,
        )

    if pd.api.types.is_numeric_dtype(y):
        # Numeric could be either classification (0/1, small set) or regression.
        if n_unique <= 2:
            return SupervisedProblemType(
                kind="classification",
                subtype="binary",
                n_unique=n_unique,
                dtype=dtype,
                notes="Numeric target with <=2 unique values.",
            )

        # Small integer label set often indicates multiclass classification.
        if pd.api.types.is_integer_dtype(y) and n_unique <= 20:
            return SupervisedProblemType(
                kind="classification",
                subtype="multiclass",
                n_unique=n_unique,
                dtype=dtype,
                notes="Integer target with small number of unique values.",
            )

        # Count regression heuristic (non-negative integers, larger label space)
        if pd.api.types.is_integer_dtype(y) and (y_non_null.min() >= 0):
            return SupervisedProblemType(
                kind="regression",
                subtype="count",
                n_unique=n_unique,
                dtype=dtype,
                notes="Non-negative integer target; treat as count regression.",
            )

        return SupervisedProblemType(
            kind="regression",
            subtype="continuous",
            n_unique=n_unique,
            dtype=dtype,
        )

    # Fallback to classification when unsure.
    return SupervisedProblemType(
        kind="classification",
        subtype="multiclass" if n_unique > 2 else "binary",
        n_unique=n_unique,
        dtype=dtype,
        notes="Fallback inference.",
    )


def recommended_metrics(problem: SupervisedProblemType) -> list[str]:
    """Return a short list of recommended evaluation metrics for the inferred type."""
    if problem.kind == "classification":
        if problem.subtype == "binary":
            return ["accuracy", "precision", "recall", "f1", "roc_auc"]
        if problem.subtype == "multilabel":
            return ["micro_f1", "macro_f1", "hamming_loss", "subset_accuracy"]
        return ["accuracy", "macro_f1", "weighted_f1", "confusion_matrix"]

    # regression
    if problem.subtype == "count":
        return ["mae", "rmse"]
    return ["mae", "rmse", "r2"]
