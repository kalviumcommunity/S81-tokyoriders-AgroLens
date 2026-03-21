"""
Function Parameters and Returns Demo
====================================

This script shows:
1. Functions that accept input parameters
2. Correct argument passing
3. Returning values with return
4. Using returned values outside functions
"""


def compute_revenue(quantity_kg, price_per_kg):
    """Return total revenue from quantity and unit price."""
    total = quantity_kg * price_per_kg
    return total


def compute_profit(revenue, cost):
    """Return profit as revenue minus cost."""
    return revenue - cost


def classify_profit(profit):
    """Return a text label based on profit value."""
    if profit > 20000:
        return "high_profit"
    if profit > 8000:
        return "moderate_profit"
    return "low_profit"


def print_summary(crop_name, revenue, profit, label):
    """Print formatted summary using values returned by other functions."""
    print(f"Crop: {crop_name}")
    print(f"Revenue: Rs {revenue:.2f}")
    print(f"Profit: Rs {profit:.2f}")
    print(f"Category: {label}")


def main():
    print("=== Parameter and Return Demo ===")

    # Passing arguments (positional)
    crop_name = "Wheat"
    quantity = 1500
    unit_price = 28.5
    cost = 25000

    revenue = compute_revenue(quantity, unit_price)
    profit = compute_profit(revenue, cost)
    label = classify_profit(profit)

    # Using returned values outside the function
    bonus = 0.05 * profit if profit > 0 else 0
    final_amount = profit + bonus

    print_summary(crop_name, revenue, profit, label)
    print(f"Bonus (5% of profit): Rs {bonus:.2f}")
    print(f"Final amount after bonus: Rs {final_amount:.2f}")

    # Passing arguments (keyword)
    rice_revenue = compute_revenue(price_per_kg=32.0, quantity_kg=1200)
    print(f"\nKeyword-argument example (Rice revenue): Rs {rice_revenue:.2f}")


if __name__ == "__main__":
    main()
