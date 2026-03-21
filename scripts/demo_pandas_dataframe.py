"""
Pandas DataFrame Basics Demo
============================

This script demonstrates:
1. Importing pandas correctly
2. Creating a DataFrame from a Python dictionary
3. Loading a DataFrame from an external CSV file
4. Inspecting rows, columns, and basic structure
"""

from pathlib import Path

import pandas as pd


def inspect_dataframe(df, name):
    """Print basic structure details for a DataFrame."""
    print(f"\n=== {name} ===")
    print("Head (first rows):")
    print(df.head())

    print("\nRows and columns:")
    print(f"shape: {df.shape}")
    print(f"rows: {df.shape[0]}, columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)


def create_from_dictionary():
    """Create a DataFrame from a Python dictionary."""
    crop_dict = {
        "crop": ["Rice", "Wheat", "Maize"],
        "region": ["Maharashtra", "Punjab", "Gujarat"],
        "price": [2100, 1950, 1800],
        "yield_kg": [1200, 1100, 900],
    }
    return pd.DataFrame(crop_dict)


def load_from_csv(csv_path):
    """Load a DataFrame from an external CSV file."""
    return pd.read_csv(csv_path)


def main():
    print("=== Pandas DataFrame Demo ===")

    # 1) Create DataFrame from a Python dictionary.
    dict_df = create_from_dictionary()
    inspect_dataframe(dict_df, "DataFrame from Python dictionary")

    # 2) Load DataFrame from external CSV file.
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"
    file_df = load_from_csv(csv_path)
    inspect_dataframe(file_df, f"DataFrame from CSV ({csv_path.name})")


if __name__ == "__main__":
    main()
