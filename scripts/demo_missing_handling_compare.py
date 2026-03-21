"""
Missing Value Handling Comparison Demo
=====================================

This script demonstrates:
1. Loading a DataFrame with missing values
2. Applying drop strategies
3. Applying fill strategies
4. Comparing the impact of each approach
"""

from pathlib import Path

import pandas as pd


def summary(label, df):
    """Print compact summary for comparison."""
    print(f"\n--- {label} ---")
    print(f"shape: {df.shape}")
    print("missing per column:")
    print(df.isna().sum())


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_missing_20260321.csv"

    # 1) Load DataFrame with missing values.
    original_df = pd.read_csv(csv_path)
    summary("Original", original_df)
    print("\nOriginal data preview:")
    print(original_df)

    # 2) Drop strategies.
    # Drop any row that contains at least one missing value.
    drop_any_df = original_df.dropna()
    summary("Drop rows with any missing value (dropna)", drop_any_df)

    # Drop rows only if critical columns are missing.
    drop_subset_df = original_df.dropna(subset=["crop", "price"])
    summary("Drop rows missing critical columns [crop, price]", drop_subset_df)

    # 3) Fill strategies.
    fill_df = original_df.copy()

    # Fill numeric columns with median (robust for small datasets).
    fill_df["price"] = fill_df["price"].fillna(fill_df["price"].median())
    fill_df["yield_kg"] = fill_df["yield_kg"].fillna(fill_df["yield_kg"].median())

    # Fill categorical columns with explicit placeholders.
    fill_df["crop"] = fill_df["crop"].fillna("Unknown Crop")
    fill_df["region"] = fill_df["region"].fillna("Unknown Region")

    summary("Fill missing values (median for numeric, label for categorical)", fill_df)
    print("\nFilled data preview:")
    print(fill_df)

    # 4) Compare impact.
    print("\n=== Impact Comparison ===")
    print(f"Original row count: {len(original_df)}")
    print(f"After drop-any row count: {len(drop_any_df)}")
    print(f"After drop-subset row count: {len(drop_subset_df)}")
    print(f"After fill row count: {len(fill_df)}")

    print("\nInterpretation:")
    print("- Drop-any is strict: highest data loss, but no missing values remain.")
    print("- Drop-subset keeps more rows by dropping only records missing critical fields.")
    print("- Fill strategy keeps all rows and removes missing values by imputation.")
    print("- Best choice depends on whether data retention or purity is more important.")


if __name__ == "__main__":
    main()
