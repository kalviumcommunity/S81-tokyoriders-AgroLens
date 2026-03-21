"""
Numeric Distribution Comparison Demo
===================================

This script demonstrates how to:
1. Load a dataset with multiple numeric columns
2. Compute summary statistics for each numeric column
3. Compare distributions across columns
4. Interpret similarities and differences
"""

from pathlib import Path

import pandas as pd


def interpret_column(column_name, stats):
    """Return concise interpretation text for one numeric column."""
    mean_value = stats["mean"]
    median_value = stats["50%"]
    std_value = stats["std"]
    value_range = stats["max"] - stats["min"]

    skew_hint = "roughly symmetric" if abs(mean_value - median_value) < 0.1 * (abs(mean_value) + 1) else "likely skewed"

    return {
        "column": column_name,
        "mean": mean_value,
        "median": median_value,
        "std": std_value,
        "range": value_range,
        "shape_hint": skew_hint,
    }


def print_comparison(interpretations):
    """Compare columns by spread and central tendency."""
    print("\n=== Distribution Comparison ===")

    most_variable = max(interpretations, key=lambda x: x["std"])
    least_variable = min(interpretations, key=lambda x: x["std"])

    print(
        f"Most variable column: {most_variable['column']} "
        f"(std={most_variable['std']:.2f}, range={most_variable['range']:.2f})"
    )
    print(
        f"Least variable column: {least_variable['column']} "
        f"(std={least_variable['std']:.2f}, range={least_variable['range']:.2f})"
    )

    print("\nColumn-wise interpretation:")
    for item in interpretations:
        print(
            f"- {item['column']}: mean={item['mean']:.2f}, median={item['median']:.2f}, "
            f"std={item['std']:.2f}, range={item['range']:.2f}, {item['shape_hint']}"
        )

    print("\nSimilarity/Difference summary:")
    print("- Columns with close mean and median tend to have more balanced distributions.")
    print("- Higher standard deviation indicates wider spread and less consistency.")
    print("- Range helps identify how extreme minimum and maximum values are.")


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    # 1) Load dataset.
    data_frame = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path.name}")

    # 2) Select all numeric columns and compute summary statistics.
    numeric_df = data_frame.select_dtypes(include=["number"])
    print("\nNumeric columns:", numeric_df.columns.tolist())

    summary_stats = numeric_df.describe().T
    print("\n=== Summary Statistics (numeric columns) ===")
    print(summary_stats[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]])

    # 3) Build interpretation per column.
    interpretations = [
        interpret_column(column_name, row_stats)
        for column_name, row_stats in summary_stats.iterrows()
    ]

    # 4) Compare and interpret distributions.
    print_comparison(interpretations)


if __name__ == "__main__":
    main()
