"""
DataFrame Overview Demo
=======================

This script demonstrates:
1. Loading a dataset into a Pandas DataFrame
2. Using head() to preview the data
3. Using info() to inspect structure and data types
4. Using describe() to summarize numeric columns
"""

from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    # Load dataset into DataFrame.
    data_frame = pd.read_csv(csv_path)

    print(f"Loaded dataset: {csv_path.name}")

    print("\n=== head() preview ===")
    print(data_frame.head())

    print("\n=== info() structure and dtypes ===")
    data_frame.info()

    print("\n=== describe() numeric summary ===")
    print(data_frame.describe())


if __name__ == "__main__":
    main()
