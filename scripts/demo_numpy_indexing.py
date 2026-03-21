"""
NumPy 1D/2D Arrays, Shape, Dimensions, and Indexing Demo
"""

import numpy as np


def main():
    # Create 1D and 2D arrays.
    array_1d = np.array([12, 24, 36, 48, 60])
    array_2d = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])

    print("=== 1D Array ===")
    print(array_1d)
    print(f"shape: {array_1d.shape}")
    print(f"ndim: {array_1d.ndim}")

    print("\n=== 2D Array ===")
    print(array_2d)
    print(f"shape: {array_2d.shape}")
    print(f"ndim: {array_2d.ndim}")

    # Access elements using correct index positions.
    print("\n=== Element Access ===")
    print(f"array_1d[0] = {array_1d[0]}")
    print(f"array_1d[3] = {array_1d[3]}")
    print(f"array_2d[0, 2] = {array_2d[0, 2]}")
    print(f"array_2d[2, 1] = {array_2d[2, 1]}")


if __name__ == "__main__":
    main()
