from __future__ import annotations

import json
import math
from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class NumericDistributionSummary:
    column: str
    dtype: str
    count: int
    missing: int
    min: float
    p25: float
    median: float
    mean: float
    p75: float
    p95: float
    p99: float
    max: float
    std: float
    skew: float
    outliers_iqr: int


@dataclass(frozen=True)
class CategoricalDistributionSummary:
    column: str
    dtype: str
    count: int
    missing: int
    n_unique: int
    top_values: list[tuple[str, int]]
    rare_values: list[tuple[str, int]]


def _iqr_outlier_count(series: pd.Series) -> int:
    values = series.dropna()
    if values.empty:
        return 0
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return 0
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return int(((values < lower) | (values > upper)).sum())


def summarize_numeric(series: pd.Series, *, name: str) -> NumericDistributionSummary:
    numeric = pd.to_numeric(series, errors="coerce")
    values = numeric.dropna()
    missing = int(numeric.isna().sum())

    if values.empty:
        return NumericDistributionSummary(
            column=name,
            dtype=str(series.dtype),
            count=0,
            missing=missing,
            min=float("nan"),
            p25=float("nan"),
            median=float("nan"),
            mean=float("nan"),
            p75=float("nan"),
            p95=float("nan"),
            p99=float("nan"),
            max=float("nan"),
            std=float("nan"),
            skew=float("nan"),
            outliers_iqr=0,
        )

    return NumericDistributionSummary(
        column=name,
        dtype=str(series.dtype),
        count=int(values.shape[0]),
        missing=missing,
        min=float(values.min()),
        p25=float(values.quantile(0.25)),
        median=float(values.median()),
        mean=float(values.mean()),
        p75=float(values.quantile(0.75)),
        p95=float(values.quantile(0.95)),
        p99=float(values.quantile(0.99)),
        max=float(values.max()),
        std=float(values.std(ddof=1)) if values.shape[0] > 1 else 0.0,
        skew=float(values.skew()) if values.shape[0] > 2 else 0.0,
        outliers_iqr=_iqr_outlier_count(values),
    )


def summarize_categorical(
    series: pd.Series,
    *,
    name: str,
    top_n: int = 10,
    rare_threshold: int = 1,
) -> CategoricalDistributionSummary:
    missing = int(series.isna().sum())
    values = series.dropna().astype(str)
    counts = values.value_counts(dropna=True)

    top_values = [(idx, int(val)) for idx, val in counts.head(top_n).items()]
    rare_values = [(idx, int(val)) for idx, val in counts[counts <= rare_threshold].items()]

    return CategoricalDistributionSummary(
        column=name,
        dtype=str(series.dtype),
        count=int(values.shape[0]),
        missing=missing,
        n_unique=int(values.nunique()),
        top_values=top_values,
        rare_values=rare_values,
    )


def inspect_feature_distributions(
    dataframe: pd.DataFrame,
    *,
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    target: pd.Series | None = None,
) -> tuple[list[NumericDistributionSummary], list[CategoricalDistributionSummary]]:
    """Inspect numeric and categorical feature distributions.

    Returns summaries suitable for printing or reporting.

    If target is provided (binary/multi-class), you can perform per-target comparisons
    externally using groupby; this function stays focused on per-column summaries.
    """
    if numeric_features is None:
        numeric_features = dataframe.select_dtypes(include="number").columns.tolist()
    if categorical_features is None:
        categorical_features = [
            col for col in dataframe.columns if col not in numeric_features
        ]

    numeric_summaries: list[NumericDistributionSummary] = []
    for col in numeric_features:
        if col in dataframe.columns:
            numeric_summaries.append(summarize_numeric(dataframe[col], name=col))

    categorical_summaries: list[CategoricalDistributionSummary] = []
    for col in categorical_features:
        if col in dataframe.columns:
            categorical_summaries.append(summarize_categorical(dataframe[col], name=col))

    return numeric_summaries, categorical_summaries


def compare_numeric_by_target(
    dataframe: pd.DataFrame,
    *,
    numeric_features: list[str],
    target: pd.Series,
) -> pd.DataFrame:
    """Compare numeric feature distributions across target classes (summary table)."""
    temp = dataframe.copy()
    temp["__target__"] = target

    frames: list[pd.DataFrame] = []
    for col in numeric_features:
        if col not in temp.columns:
            continue
        grouped = temp.groupby("__target__")[col].describe(percentiles=[0.25, 0.5, 0.75])
        grouped.insert(0, "feature", col)
        grouped = grouped.reset_index().rename(columns={"__target__": "target"})
        frames.append(grouped)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def compare_categorical_by_target(
    dataframe: pd.DataFrame,
    *,
    categorical_features: list[str],
    target: pd.Series,
    top_n: int = 5,
) -> dict[str, dict[str, list[tuple[str, int]]]]:
    """Compare categorical feature distributions across target classes.

    Returns a nested mapping:
    {
      "feature": {
        "target_value": [("category", count), ...],
        ...
      },
      ...
    }
    """
    temp = dataframe.copy()
    temp["__target__"] = target

    comparisons: dict[str, dict[str, list[tuple[str, int]]]] = {}
    for col in categorical_features:
        if col not in temp.columns:
            continue

        per_target: dict[str, list[tuple[str, int]]] = {}
        grouped = temp[["__target__", col]].dropna().copy()
        if grouped.empty:
            comparisons[col] = per_target
            continue

        grouped[col] = grouped[col].astype(str)
        for target_value, subset in grouped.groupby("__target__"):
            counts = subset[col].value_counts().head(top_n)
            per_target[str(target_value)] = [(idx, int(val)) for idx, val in counts.items()]
        comparisons[col] = per_target

    return comparisons


def build_feature_distribution_report(
    dataframe: pd.DataFrame,
    *,
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    target: pd.Series | None = None,
) -> dict[str, object]:
    """Build a JSON-serializable report capturing feature distribution insights."""
    numeric_summaries, categorical_summaries = inspect_feature_distributions(
        dataframe,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        target=target,
    )

    report: dict[str, object] = {
        "shape": {"rows": int(dataframe.shape[0]), "cols": int(dataframe.shape[1])},
        "numeric": [asdict(summary) for summary in numeric_summaries],
        "categorical": [asdict(summary) for summary in categorical_summaries],
    }

    if target is not None:
        resolved_numeric = (
            numeric_features
            if numeric_features is not None
            else dataframe.select_dtypes(include="number").columns.tolist()
        )
        resolved_categorical = (
            categorical_features
            if categorical_features is not None
            else [col for col in dataframe.columns if col not in resolved_numeric]
        )

        numeric_by_target = compare_numeric_by_target(
            dataframe,
            numeric_features=resolved_numeric,
            target=target,
        )
        report["numeric_by_target"] = (
            numeric_by_target.to_dict(orient="records") if not numeric_by_target.empty else []
        )

        report["categorical_by_target"] = compare_categorical_by_target(
            dataframe,
            categorical_features=resolved_categorical,
            target=target,
        )

    return report


def save_feature_distribution_report(report: dict[str, object], path: str | Path) -> Path:
    def make_json_safe(value: object) -> object:
        if value is None or isinstance(value, (str, bool, int)):
            return value
        if isinstance(value, float):
            return value if math.isfinite(value) else None
        if isinstance(value, (list, tuple)):
            return [make_json_safe(item) for item in value]
        if isinstance(value, dict):
            return {str(key): make_json_safe(val) for key, val in value.items()}

        # Best effort conversion for numpy scalars / pandas types.
        try:
            as_float = float(value)  # type: ignore[arg-type]
        except Exception:
            return str(value)
        return as_float if math.isfinite(as_float) else None

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file_handle:
        json.dump(make_json_safe(report), file_handle, indent=2, ensure_ascii=False, allow_nan=False)
    return destination


def maybe_save_distribution_plots(
    dataframe: pd.DataFrame,
    *,
    numeric_features: list[str],
    output_dir: str | Path,
    bins: int = 30,
) -> list[Path]:
    """Optionally save histogram + boxplot images for numeric features.

    This function is safe to call even when matplotlib is not installed.
    It will return an empty list in that case.
    """
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return []

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    saved: list[Path] = []
    for col in numeric_features:
        if col not in dataframe.columns:
            continue

        series = pd.to_numeric(dataframe[col], errors="coerce")

        fig = plt.figure(figsize=(8, 4))
        ax = fig.add_subplot(1, 2, 1)
        ax.hist(series.dropna(), bins=bins)
        ax.set_title(f"{col} (hist)")

        ax2 = fig.add_subplot(1, 2, 2)
        ax2.boxplot(series.dropna(), vert=True)
        ax2.set_title(f"{col} (box)")

        file_path = destination / f"dist_{col}.png"
        fig.tight_layout()
        fig.savefig(file_path, dpi=150)
        plt.close(fig)
        saved.append(file_path)

    return saved
