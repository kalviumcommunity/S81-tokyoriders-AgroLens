"""
DataFrame Shape and Type Interpretation Demo
===========================================

This script demonstrates:
1. Loading a dataset into a Pandas DataFrame
2. Inspecting DataFrame shape
3. Inspecting column data types
4. Interpreting what rows, columns, and types represent
"""

from pathlib import Path

import pandas as pd


def interpret_dataset(df):
    """Print human-readable interpretation of rows, columns, and dtypes."""
    row_count, column_count = df.shape

    print("\n=== Interpretation ===")
    print(f"Rows ({row_count}): each row represents one crop record.")
    print(f"Columns ({column_count}): each column represents one feature about a crop.")

    dtype_meaning = {
        "int64": "numeric count/value used for calculations",
        "float64": "numeric value with decimals",
        "object": "text/categorical values",
        "str": "text/categorical values",
        "bool": "True/False flag",
    }

    print("\nColumn-by-column meaning:")
    for column_name, dtype in df.dtypes.items():
        dtype_name = str(dtype)
        meaning = dtype_meaning.get(dtype_name, "general data type")
        print(f"- {column_name}: {dtype_name} -> {meaning}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    # 1) Load dataset into DataFrame.
    data_frame = pd.read_csv(csv_path)

    print(f"Loaded dataset: {csv_path.name}")

    # 2) Inspect shape.
    print("\n=== DataFrame Shape ===")
    print(f"shape: {data_frame.shape}")

    # 3) Inspect column data types.
    print("\n=== Column Data Types ===")
    print(data_frame.dtypes)

    # 4) Interpret rows, columns, and types.
    interpret_dataset(data_frame)


if __name__ == "__main__":
    main()
