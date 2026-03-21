"""
Duplicate Records Handling Demo
===============================

This script demonstrates how to:
1. Load a dataset containing duplicate records
2. Detect duplicate rows
3. Inspect duplicate entries
4. Remove duplicates intentionally
5. Verify duplicates are handled correctly
"""

from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "raw" / "source_demo_crops_duplicates_20260321.csv"

    # 1) Load dataset.
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path.name}")
    print(f"Initial shape: {df.shape}")

    # 2) Detect duplicate rows.
    duplicate_mask = df.duplicated(keep=False)
    duplicate_count = int(df.duplicated().sum())

    print("\n=== Duplicate Detection ===")
    print(f"Duplicate row count (excluding first occurrence): {duplicate_count}")

    # 3) Inspect duplicate entries.
    duplicate_rows = df[duplicate_mask].sort_values(by=df.columns.tolist()).reset_index(drop=True)
    print("\n=== Duplicate Entries ===")
    print(duplicate_rows)

    # 4) Remove duplicates intentionally.
    deduplicated_df = df.drop_duplicates(keep="first").reset_index(drop=True)

    print("\n=== After Removing Duplicates ===")
    print(deduplicated_df)
    print(f"New shape: {deduplicated_df.shape}")

    # 5) Verify duplicates are handled.
    remaining_duplicates = int(deduplicated_df.duplicated().sum())
    rows_removed = len(df) - len(deduplicated_df)

    print("\n=== Verification ===")
    print(f"Rows removed: {rows_removed}")
    print(f"Remaining duplicate rows: {remaining_duplicates}")

    if remaining_duplicates == 0:
        print("Verification successful: duplicates have been handled correctly.")
    else:
        print("Verification failed: duplicates still exist.")


if __name__ == "__main__":
    main()
