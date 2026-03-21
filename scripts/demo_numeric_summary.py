"""
Numeric Column Summary Statistics Demo
======================================

This script demonstrates how to:
1. Load a dataset into a Pandas DataFrame
2. Select individual numeric columns
3. Compute basic summary statistics
4. Interpret results clearly
"""

from pathlib import Path

import pandas as pd


def summarize_column(series, column_name):
    """Print summary stats and a short interpretation for one numeric column."""
    mean_value = series.mean()
    median_value = series.median()
    min_value = series.min()
    max_value = series.max()
    std_value = series.std()

    print(f"\n=== {column_name} Summary ===")
    print(f"mean:   {mean_value:.2f}")
    print(f"median: {median_value:.2f}")
    print(f"min:    {min_value:.2f}")
    print(f"max:    {max_value:.2f}")
    print(f"std:    {std_value:.2f}")

    print("Interpretation:")
    print(f"- Typical value is around {mean_value:.2f} (mean) and {median_value:.2f} (median).")
    print(f"- Values range from {min_value:.2f} to {max_value:.2f}.")
    print(f"- Variability (std) is {std_value:.2f}; higher values indicate more spread.")


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    # 1) Load dataset into DataFrame.
    data_frame = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path.name}")

    # 2) Select individual numeric columns.
    price_column = data_frame["price"]
    yield_column = data_frame["yield_kg"]

    # 3) Compute summary statistics for selected numeric columns.
    summarize_column(price_column, "price")
    summarize_column(yield_column, "yield_kg")


if __name__ == "__main__":
    main()
