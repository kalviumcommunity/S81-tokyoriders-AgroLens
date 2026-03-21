"""
NumPy Arithmetic Operations Demo
================================

This script demonstrates:
1. Creating NumPy arrays with numeric values
2. Performing basic arithmetic on arrays
3. Applying scalar operations to arrays
4. Observing element-wise computation behavior
"""

import numpy as np


def main():
    print("=== NumPy Arithmetic Demo ===")

    # Numeric NumPy arrays.
    prices_a = np.array([100, 120, 140, 160], dtype=float)
    prices_b = np.array([10, 20, 30, 40], dtype=float)

    print("\nArray A (prices_a):", prices_a)
    print("Array B (prices_b):", prices_b)

    # Basic array-to-array arithmetic (element-wise).
    add_result = prices_a + prices_b
    sub_result = prices_a - prices_b
    mul_result = prices_a * prices_b
    div_result = prices_a / prices_b

    print("\n=== Element-wise array operations ===")
    print("prices_a + prices_b =", add_result)
    print("prices_a - prices_b =", sub_result)
    print("prices_a * prices_b =", mul_result)
    print("prices_a / prices_b =", div_result)

    # Scalar operations also apply element-wise.
    scalar_add = prices_a + 5
    scalar_mul = prices_a * 1.1
    scalar_div = prices_a / 2

    print("\n=== Scalar operations (also element-wise) ===")
    print("prices_a + 5 =", scalar_add)
    print("prices_a * 1.1 =", scalar_mul)
    print("prices_a / 2 =", scalar_div)

    # Explicit explanation of element-wise behavior.
    print("\n=== Element-wise explanation ===")
    print("Index 0: 100 + 10 =", add_result[0])
    print("Index 1: 120 + 20 =", add_result[1])
    print("Index 2: 140 + 30 =", add_result[2])
    print("Index 3: 160 + 40 =", add_result[3])

    print("\nElement-wise means each position is computed independently")
    print("using matching indices from both arrays, or each element with the scalar.")


if __name__ == "__main__":
    main()
