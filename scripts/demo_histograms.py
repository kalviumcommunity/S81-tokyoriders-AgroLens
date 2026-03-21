"""
Histogram Distribution Demo
===========================

This script demonstrates:
1. Loading a dataset into a Pandas DataFrame
2. Selecting numeric columns
3. Creating histograms to visualize distributions
4. Interpreting shape and spread of selected columns
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def interpret_distribution(series, column_name):
    """Print concise interpretation of shape and spread."""
    mean_value = series.mean()
    median_value = series.median()
    std_value = series.std()
    value_range = series.max() - series.min()
    skew_value = series.skew()

    if skew_value > 0.5:
        shape = "right-skewed"
    elif skew_value < -0.5:
        shape = "left-skewed"
    else:
        shape = "roughly symmetric"

    print(f"\n{column_name}:")
    print(f"- mean={mean_value:.2f}, median={median_value:.2f}")
    print(f"- std={std_value:.2f}, range={value_range:.2f}")
    print(f"- skew={skew_value:.2f} -> {shape}")


def save_histograms(numeric_df, output_file):
    """Create and save histograms for numeric columns."""
    axes = numeric_df.hist(figsize=(10, 4), bins=6, edgecolor="black")

    # Flatten axes for reliable title assignment.
    for ax in axes.flatten():
        ax.set_ylabel("Frequency")

    plt.suptitle("Numeric Column Distributions", y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=140, bbox_inches="tight")
    plt.close()


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_csv = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"
    output_png = project_root / "outputs" / "figures" / "histograms_demo.png"

    # 1) Load DataFrame.
    data_frame = pd.read_csv(input_csv)
    print(f"Loaded dataset: {input_csv.name}")

    # 2) Select numeric columns.
    numeric_df = data_frame.select_dtypes(include=["number"])
    print(f"Numeric columns selected: {numeric_df.columns.tolist()}")

    # 3) Create histogram visualizations.
    save_histograms(numeric_df, output_png)
    print(f"Histogram image saved: {output_png}")

    # 4) Interpret shape and spread.
    print("\n=== Distribution Interpretation ===")
    for column_name in numeric_df.columns:
        interpret_distribution(numeric_df[column_name], column_name)


if __name__ == "__main__":
    main()
