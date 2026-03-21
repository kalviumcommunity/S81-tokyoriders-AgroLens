"""
Pandas DataFrame Selection Demo
===============================

This script demonstrates:
1. Loading a DataFrame in pandas
2. Selecting columns by name
3. Selecting rows by indexing/slicing
4. Combining row and column selection
"""

from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_20260321.csv"

    # 1) Load DataFrame into pandas.
    df = pd.read_csv(csv_path)
    print(f"Loaded file: {csv_path.name}")

    # 2) Select columns by name.
    print("\n=== Column Selection ===")
    print("Single column: df['crop']")
    print(df["crop"])

    print("\nMultiple columns: df[['crop', 'price']]")
    print(df[["crop", "price"]])

    # 3) Select rows using indexing and slicing.
    print("\n=== Row Selection ===")
    print("Row by index (iloc[1]):")
    print(df.iloc[1])

    print("\nRows by slice (iloc[1:3]):")
    print(df.iloc[1:3])

    # 4) Combine row and column selection.
    print("\n=== Combined Row + Column Selection ===")
    print("Single value (iloc[2, 2]) -> row 2, column 2:")
    print(df.iloc[2, 2])

    print("\nSubset with rows 0:3 and columns ['crop', 'yield_kg']:")
    print(df.loc[0:2, ["crop", "yield_kg"]])


if __name__ == "__main__":
    main()
