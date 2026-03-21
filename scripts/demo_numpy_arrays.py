"""
NumPy Array Basics Demo
=======================

This script demonstrates:
1. Importing NumPy correctly
2. Converting Python lists into NumPy arrays
3. Creating 1D and simple 2D arrays
4. Inspecting array properties
"""

import numpy as np


def inspect_array(array_name, array_value):
    """Print common properties for a NumPy array."""
    print(f"\n{array_name}:")
    print(array_value)
    print(f"  ndim: {array_value.ndim}")
    print(f"  shape: {array_value.shape}")
    print(f"  size: {array_value.size}")
    print(f"  dtype: {array_value.dtype}")


def main():
    print("=== NumPy Array Demo ===")

    # Convert Python lists into NumPy arrays.
    python_list_1d = [10, 20, 30, 40]
    python_list_2d = [[1, 2, 3], [4, 5, 6]]

    array_1d = np.array(python_list_1d)
    array_2d = np.array(python_list_2d)

    # Explicitly create additional simple arrays.
    ones_1d = np.array([1, 1, 1, 1])
    matrix_2d = np.array([[7, 8], [9, 10]])

    inspect_array("array_1d (from list)", array_1d)
    inspect_array("array_2d (from nested list)", array_2d)
    inspect_array("ones_1d", ones_1d)
    inspect_array("matrix_2d", matrix_2d)

    print("\nQuick element access examples:")
    print(f"array_1d[2] = {array_1d[2]}")
    print(f"array_2d[1, 2] = {array_2d[1, 2]}")


if __name__ == "__main__":
    main()
