"""
Scatter Plot Relationship Demo
==============================

This script demonstrates:
1. Loading a dataset into a Pandas DataFrame
2. Selecting two numeric variables
3. Creating a scatter plot to visualize their relationship
4. Identifying patterns, trends, clusters, or outliers
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def iqr_bounds(series):
    """Return lower and upper bounds using the 1.5*IQR rule."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_scatter_20260321.csv"
    output_png = project_root / "outputs" / "figures" / "scatter_yield_price_demo.png"

    # 1) Load dataset.
    data_frame = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path.name}")

    # 2) Select two numeric variables.
    x_col = "yield_kg"
    y_col = "price"
    x_values = data_frame[x_col]
    y_values = data_frame[y_col]

    print(f"Selected numeric columns: {x_col}, {y_col}")

    # 3) Create scatter plot.
    plt.figure(figsize=(7, 4.5))
    plt.scatter(x_values, y_values, alpha=0.85)
    plt.title("Scatter Plot: Yield vs Price")
    plt.xlabel("Yield (kg)")
    plt.ylabel("Price")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_png, dpi=140, bbox_inches="tight")
    plt.close()
    print(f"Scatter plot saved: {output_png}")

    # 4) Identify patterns/trends/outliers.
    correlation = x_values.corr(y_values)
    print("\n=== Relationship Summary ===")
    print(f"Pearson correlation ({x_col} vs {y_col}): {correlation:.3f}")

    if correlation > 0.6:
        print("Trend: clear positive relationship (higher yield tends to higher price).")
    elif correlation < -0.6:
        print("Trend: clear negative relationship (higher yield tends to lower price).")
    else:
        print("Trend: weak or moderate linear relationship.")

    # Outlier detection using IQR bounds on both axes.
    x_low, x_high = iqr_bounds(x_values)
    y_low, y_high = iqr_bounds(y_values)
    outlier_mask = (
        (x_values < x_low)
        | (x_values > x_high)
        | (y_values < y_low)
        | (y_values > y_high)
    )

    outliers = data_frame[outlier_mask]

    print("\nPattern notes:")
    print("- Most points form a main cluster with increasing yield and price.")
    if len(outliers) > 0:
        print(f"- Potential outliers detected: {len(outliers)}")
        print(outliers[["crop", x_col, y_col]])
    else:
        print("- No strong outliers detected by IQR rule.")


if __name__ == "__main__":
    main()
