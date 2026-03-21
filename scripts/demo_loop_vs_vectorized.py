"""
Loop vs Vectorized NumPy Computation Demo
=========================================

Task:
1. Create NumPy arrays
2. Compute result with a loop
3. Compute the same result with vectorized NumPy operations
4. Verify both results are equal
"""

import numpy as np


def compute_with_loop(yield_kg, price_per_kg, transport_cost):
    """Compute net revenue per crop using a Python loop."""
    net_revenue = np.zeros(len(yield_kg), dtype=float)

    for index in range(len(yield_kg)):
        gross = yield_kg[index] * price_per_kg[index]
        net_revenue[index] = gross - transport_cost[index]

    return net_revenue


def compute_with_vectorization(yield_kg, price_per_kg, transport_cost):
    """Compute net revenue per crop using vectorized NumPy operations."""
    return (yield_kg * price_per_kg) - transport_cost


def main():
    print("=== Loop vs Vectorized Operations ===")

    # 1. Create NumPy arrays.
    yield_kg = np.array([1200, 950, 1500, 800], dtype=float)
    price_per_kg = np.array([32.5, 28.0, 24.75, 40.0], dtype=float)
    transport_cost = np.array([1500, 1200, 2100, 1000], dtype=float)

    print("yield_kg:", yield_kg)
    print("price_per_kg:", price_per_kg)
    print("transport_cost:", transport_cost)

    # 2. Loop-based operation.
    loop_result = compute_with_loop(yield_kg, price_per_kg, transport_cost)
    print("\nLoop result:", loop_result)

    # 3. Vectorized operation.
    vectorized_result = compute_with_vectorization(yield_kg, price_per_kg, transport_cost)
    print("Vectorized result:", vectorized_result)

    # 4. Verify equality.
    are_equal = np.allclose(loop_result, vectorized_result)
    print("\nResults match:", are_equal)

    if are_equal:
        print("Verification successful: both approaches produce the same values.")
    else:
        print("Verification failed: results differ.")


if __name__ == "__main__":
    main()
