"""
Boxplot Distribution Demo
========================

This script demonstrates:
1. Loading a dataset into a Pandas DataFrame
2. Selecting one or more numeric columns
3. Creating boxplots to visualize distributions
4. Interpreting median, spread, and outliers
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def summarize_boxplot_stats(series, column_name):
    """Print median, spread (IQR), and outlier count using IQR rule."""
    q1 = series.quantile(0.25)
    median = series.quantile(0.50)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_mask = (series < lower_bound) | (series > upper_bound)
    outlier_count = int(outlier_mask.sum())

    print(f"\n{column_name}:")
    print(f"- median (Q2): {median:.2f}")
    print(f"- spread (IQR = Q3 - Q1): {iqr:.2f}")
    print(f"- whisker bounds (IQR rule): [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"- outlier count: {outlier_count}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_csv = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"
    output_png = project_root / "outputs" / "figures" / "boxplots_demo.png"

    # 1) Load DataFrame.
    data_frame = pd.read_csv(input_csv)
    print(f"Loaded dataset: {input_csv.name}")

    # 2) Select numeric columns.
    numeric_df = data_frame.select_dtypes(include=["number"])
    print(f"Numeric columns selected: {numeric_df.columns.tolist()}")

    # 3) Create boxplots.
    plt.figure(figsize=(8, 4))
    numeric_df.boxplot()
    plt.title("Numeric Column Boxplots")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(output_png, dpi=140, bbox_inches="tight")
    plt.close()

    print(f"Boxplot image saved: {output_png}")

    # 4) Interpret median, spread, and outliers.
    print("\n=== Boxplot Interpretation ===")
    for column_name in numeric_df.columns:
        summarize_boxplot_stats(numeric_df[column_name], column_name)


if __name__ == "__main__":
    main()
