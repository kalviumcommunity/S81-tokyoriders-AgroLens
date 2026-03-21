"""
Pandas Missing Values Inspection Demo
=====================================

This script demonstrates how to:
1. Load a dataset into a Pandas DataFrame
2. Detect missing values
3. Summarize missing values by column and row
4. Inspect rows containing missing data
"""

from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_missing_20260321.csv"

    # 1) Load dataset into DataFrame.
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path.name}")

    # 2) Detect missing values.
    print("\n=== Missing Value Matrix (True means missing) ===")
    print(df.isna())

    # 3) Summarize missing values.
    print("\n=== Missing Values by Column ===")
    print(df.isna().sum())

    print("\n=== Missing Values by Row ===")
    missing_per_row = df.isna().sum(axis=1)
    print(missing_per_row)

    # 4) Inspect rows containing missing data.
    print("\n=== Rows Containing Missing Data ===")
    rows_with_missing = df[df.isna().any(axis=1)]
    print(rows_with_missing)


if __name__ == "__main__":
    main()
