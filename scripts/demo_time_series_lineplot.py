"""
Time Series Line Plot Demo
==========================

This script demonstrates how to:
1. Load a dataset containing a time-based column
2. Ensure records are correctly ordered by time
3. Create a line plot using a numeric column
4. Identify and explain visible trends/patterns
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def describe_trend(df, time_col, value_col):
    """Print simple trend interpretation from ordered time-series data."""
    first_value = df[value_col].iloc[0]
    last_value = df[value_col].iloc[-1]
    change = last_value - first_value

    max_row = df.loc[df[value_col].idxmax()]
    min_row = df.loc[df[value_col].idxmin()]

    print("\n=== Trend Interpretation ===")
    print(f"Start value ({df[time_col].iloc[0].date()}): {first_value}")
    print(f"End value   ({df[time_col].iloc[-1].date()}): {last_value}")
    print(f"Net change over period: {change:+.2f}")

    print(f"Minimum point: {min_row[value_col]} on {min_row[time_col].date()}")
    print(f"Maximum point: {max_row[value_col]} on {max_row[time_col].date()}")

    if change > 0:
        direction = "overall upward"
    elif change < 0:
        direction = "overall downward"
    else:
        direction = "overall flat"

    print(f"Visible pattern: {direction} trend with minor month-to-month variation.")


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_time_series_20260321.csv"
    output_png = project_root / "outputs" / "figures" / "time_series_price_lineplot.png"

    # 1) Load dataset with time-based column.
    data_frame = pd.read_csv(csv_path)

    # Convert and validate time column.
    data_frame["date"] = pd.to_datetime(data_frame["date"], errors="raise")

    # 2) Ensure data is ordered by time.
    data_frame = data_frame.sort_values("date").reset_index(drop=True)

    print(f"Loaded dataset: {csv_path.name}")
    print("\n=== Ordered Data Preview ===")
    print(data_frame)

    # 3) Create line plot for numeric column.
    plt.figure(figsize=(8, 4))
    plt.plot(data_frame["date"], data_frame["price"], marker="o", linewidth=2)
    plt.title("Price Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_png, dpi=140, bbox_inches="tight")
    plt.close()

    print(f"\nLine plot saved: {output_png}")

    # 4) Interpret visible trend/patterns.
    describe_trend(data_frame, "date", "price")


if __name__ == "__main__":
    main()
