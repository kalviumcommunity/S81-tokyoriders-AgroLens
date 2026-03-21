"""
Column Name and Data Format Standardization Demo
================================================

This script demonstrates how to:
1. Load a DataFrame with unstandardized column names/formats
2. Clean and standardize column names
3. Apply consistent formatting to one data column
4. Compare dataset before and after standardization
"""

from pathlib import Path

import pandas as pd


def standardize_column_names(df):
    """Normalize column names to snake_case-style lowercase."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    return df


def standardize_region_column(df):
    """Apply consistent text formatting to the region column."""
    df = df.copy()
    df["region"] = df["region"].astype(str).str.strip().str.title()
    return df


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_unstandardized_20260321.csv"

    # 1) Load unstandardized DataFrame.
    raw_df = pd.read_csv(csv_path)

    print("=== BEFORE STANDARDIZATION ===")
    print("Columns:", raw_df.columns.tolist())
    print(raw_df)

    # 2) Standardize column names.
    cleaned_df = standardize_column_names(raw_df)

    # 3) Standardize one data column format.
    cleaned_df = standardize_region_column(cleaned_df)

    print("\n=== AFTER STANDARDIZATION ===")
    print("Columns:", cleaned_df.columns.tolist())
    print(cleaned_df)

    # 4) Compare before vs after.
    print("\n=== COMPARISON SUMMARY ===")
    print("Before columns:", raw_df.columns.tolist())
    print("After columns:", cleaned_df.columns.tolist())
    print("Region values before:", raw_df[" REGION "].tolist())
    print("Region values after:", cleaned_df["region"].tolist())


if __name__ == "__main__":
    main()
