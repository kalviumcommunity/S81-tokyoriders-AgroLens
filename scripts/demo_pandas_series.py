"""
Pandas Series Basics Demo
=========================

This script demonstrates:
1. Importing pandas correctly
2. Creating Series from Python lists
3. Creating Series from NumPy arrays
4. Inspecting Series values and index
"""

import numpy as np
import pandas as pd


def main():
    print("=== Pandas Series Demo ===")

    # Create Series from a Python list.
    crop_list = ["Rice", "Wheat", "Maize", "Cotton"]
    series_from_list = pd.Series(crop_list)

    print("\nSeries from Python list:")
    print(series_from_list)
    print("values:", series_from_list.values)
    print("index:", series_from_list.index)

    # Create Series from a NumPy array.
    price_array = np.array([2100, 1950, 1800, 5000], dtype=float)
    series_from_array = pd.Series(price_array, index=["rice", "wheat", "maize", "cotton"])

    print("\nSeries from NumPy array:")
    print(series_from_array)
    print("values:", series_from_array.values)
    print("index:", series_from_array.index)


if __name__ == "__main__":
    main()
