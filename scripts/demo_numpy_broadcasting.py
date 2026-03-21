"""
NumPy Broadcasting Demo
=======================

This script demonstrates:
1. Creating arrays of different shapes
2. Applying broadcasting-based operations
3. Inspecting shapes before operations
4. Explaining why broadcasting works in each case
"""

import numpy as np


def print_case_header(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def case_1_matrix_plus_row_vector():
    print_case_header("Case 1: (3, 4) + (4,)")

    matrix = np.array(
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ],
        dtype=float,
    )
    row_vector = np.array([10, 20, 30, 40], dtype=float)

    print(f"matrix.shape = {matrix.shape}")
    print(f"row_vector.shape = {row_vector.shape}")

    result = matrix + row_vector
    print("result = matrix + row_vector")
    print(result)

    print("Why broadcasting works:")
    print("- Compare from rightmost dimension.")
    print("- matrix has (3, 4), row_vector has (4,).")
    print("- Last dimension 4 matches 4, so valid.")
    print("- row_vector is repeated across 3 rows.")


def case_2_matrix_plus_column_vector():
    print_case_header("Case 2: (3, 4) + (3, 1)")

    matrix = np.array(
        [
            [2, 4, 6, 8],
            [1, 3, 5, 7],
            [10, 20, 30, 40],
        ],
        dtype=float,
    )
    col_vector = np.array([[100], [200], [300]], dtype=float)

    print(f"matrix.shape = {matrix.shape}")
    print(f"col_vector.shape = {col_vector.shape}")

    result = matrix + col_vector
    print("result = matrix + col_vector")
    print(result)

    print("Why broadcasting works:")
    print("- Shapes are (3, 4) and (3, 1).")
    print("- Compare rightmost: 4 vs 1 -> 1 can expand to 4.")
    print("- Next dimension: 3 vs 3 -> matches.")
    print("- Each row gets its corresponding column value added to all columns.")


def case_3_3d_with_1d_scale():
    print_case_header("Case 3: (2, 3, 4) * (4,)")

    tensor = np.arange(24, dtype=float).reshape(2, 3, 4)
    scale = np.array([1, 0.1, 10, -1], dtype=float)

    print(f"tensor.shape = {tensor.shape}")
    print(f"scale.shape = {scale.shape}")

    result = tensor * scale
    print("result = tensor * scale")
    print(result)

    print("Why broadcasting works:")
    print("- Shapes are (2, 3, 4) and (4,).")
    print("- Rightmost dimension 4 matches 4.")
    print("- scale is broadcast across the first two dimensions (2 and 3).")
    print("- Same 4-element scale is applied to each last-dimension slice.")


def main():
    print("NumPy Broadcasting Examples")
    case_1_matrix_plus_row_vector()
    case_2_matrix_plus_column_vector()
    case_3_3d_with_1d_scale()


if __name__ == "__main__":
    main()
