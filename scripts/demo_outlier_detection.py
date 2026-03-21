"""
Outlier Detection Demo (Visual + IQR Rule)
==========================================

This script demonstrates:
1. Loading a dataset with numeric columns
2. Visual inspection using boxplots
3. Flagging outliers with the IQR rule
4. Interpreting why flagged values stand out
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def iqr_bounds(series):
    """Return IQR-based lower/upper bounds for outlier detection."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return q1, q3, iqr, lower, upper


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_scatter_20260321.csv"
    boxplot_path = project_root / "outputs" / "figures" / "outlier_boxplots_demo.png"

    # 1) Load dataset containing numeric columns.
    data_frame = pd.read_csv(csv_path)
    numeric_columns = ["yield_kg", "price"]
    numeric_df = data_frame[numeric_columns]

    print(f"Loaded dataset: {csv_path.name}")
    print(f"Numeric columns used: {numeric_columns}")

    # 2) Visual inspection: boxplots.
    plt.figure(figsize=(8, 4.5))
    numeric_df.boxplot()
    plt.title("Boxplots for Outlier Inspection")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(boxplot_path, dpi=140, bbox_inches="tight")
    plt.close()

    print(f"Boxplot saved: {boxplot_path}")

    # 3) IQR rule to flag outliers.
    print("\n=== IQR Outlier Check ===")
    outlier_mask = pd.Series(False, index=data_frame.index)

    for column in numeric_columns:
        q1, q3, iqr, lower, upper = iqr_bounds(data_frame[column])
        current_mask = (data_frame[column] < lower) | (data_frame[column] > upper)
        outlier_mask = outlier_mask | current_mask

        print(f"\nColumn: {column}")
        print(f"Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}")
        print(f"Bounds: [{lower:.2f}, {upper:.2f}]")
        print(f"Flagged in this column: {int(current_mask.sum())}")

    flagged_rows = data_frame[outlier_mask]

    # 4) Interpretation.
    print("\n=== Flagged Rows ===")
    if flagged_rows.empty:
        print("No outliers flagged by IQR rule.")
        return

    print(flagged_rows)

    print("\n=== Interpretation ===")
    for _, row in flagged_rows.iterrows():
        print(
            f"- {row['crop']} stands out because yield_kg={row['yield_kg']} and/or "
            f"price={row['price']} falls far from the middle 50% range of the dataset."
        )


if __name__ == "__main__":
    main()
