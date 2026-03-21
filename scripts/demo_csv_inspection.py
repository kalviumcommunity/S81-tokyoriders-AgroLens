"""
CSV Loading and Structure Inspection Demo
=========================================

This script demonstrates how to:
1. Load a CSV file into a Pandas DataFrame
2. Verify rows and columns are interpreted correctly
3. Inspect the DataFrame after loading
4. Identify basic structural issues
"""

from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = ["crop", "region", "price", "yield_kg"]


def load_csv(csv_path):
    """Load CSV into a DataFrame."""
    return pd.read_csv(csv_path)


def inspect_dataframe(df):
    """Print DataFrame structure and quick preview."""
    print("=== DataFrame Preview ===")
    print(df.head())

    print("\n=== Shape Check ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n=== Column Check ===")
    print(df.columns.tolist())

    print("\n=== Data Types ===")
    print(df.dtypes)


def find_structural_issues(df):
    """Identify common structural issues in loaded data."""
    issues = []

    actual_columns = df.columns.tolist()
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in actual_columns]
    extra_columns = [column for column in actual_columns if column not in EXPECTED_COLUMNS]

    if missing_columns:
        issues.append(f"Missing expected columns: {missing_columns}")

    if extra_columns:
        issues.append(f"Unexpected extra columns: {extra_columns}")

    duplicate_row_count = int(df.duplicated().sum())
    if duplicate_row_count > 0:
        issues.append(f"Duplicate rows found: {duplicate_row_count}")

    null_counts = df.isnull().sum()
    null_columns = null_counts[null_counts > 0]
    if not null_columns.empty:
        issues.append(f"Missing values detected: {null_columns.to_dict()}")

    blank_column_names = [column for column in actual_columns if str(column).strip() == ""]
    if blank_column_names:
        issues.append("Blank column names detected")

    return issues


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    print(f"Loading CSV: {csv_path}")
    dataframe = load_csv(csv_path)

    inspect_dataframe(dataframe)

    print("\n=== Structural Issue Check ===")
    issues = find_structural_issues(dataframe)

    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No basic structural issues found.")


if __name__ == "__main__":
    main()
