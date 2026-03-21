"""
Conditionals and Logical Operators Demo
======================================

This script demonstrates:
1. if / elif / else branches
2. Numeric and string comparisons
3. Logical operators: and, or, not
4. Different execution paths with clear explanations
"""


def evaluate_price_risk(price_per_kg):
    """Classify market risk based on numeric price."""
    print(f"\nInput price_per_kg = {price_per_kg}")

    if price_per_kg < 1500:
        print("Path: if -> Low price zone, high income risk")
        return "high_risk"
    elif price_per_kg < 2200:
        print("Path: elif -> Medium price zone, moderate risk")
        return "moderate_risk"
    else:
        print("Path: else -> Strong price zone, lower risk")
        return "low_risk"


def evaluate_region(region_name):
    """Demonstrate string comparisons and normalization."""
    print(f"\nInput region_name = '{region_name}'")

    normalized = region_name.strip().lower()

    if normalized == "maharashtra":
        print("Path: if -> Known target region: Maharashtra")
    elif normalized == "karnataka":
        print("Path: elif -> Neighboring market region: Karnataka")
    else:
        print("Path: else -> Region not in priority watchlist")


def evaluate_crop_decision(price, rainfall_mm, crop_name):
    """
    Show logical operators with practical farm decision rules.
    """
    print("\n--- Decision Rule Check ---")
    print(f"price={price}, rainfall_mm={rainfall_mm}, crop_name='{crop_name}'")

    # and: both conditions must be true
    if price >= 2000 and rainfall_mm >= 700:
        print("Path A (and): Favorable price and sufficient rainfall")
    else:
        print("Path A (and): At least one condition failed")

    # or: at least one condition must be true
    if crop_name.lower() == "rice" or crop_name.lower() == "wheat":
        print("Path B (or): Crop is in core recommendation group")
    else:
        print("Path B (or): Crop is outside core recommendation group")

    # not: invert boolean meaning
    is_drought = rainfall_mm < 500
    if not is_drought:
        print("Path C (not): Not drought conditions")
    else:
        print("Path C (not): Drought conditions detected")


def compare_types_safely():
    """
    Demonstrate correct numeric vs string comparisons and a safe conversion pattern.
    """
    print("\n=== Type Comparison Demo ===")

    numeric_price = 2100
    string_price = "2100"

    print(f"numeric_price ({type(numeric_price).__name__}) = {numeric_price}")
    print(f"string_price ({type(string_price).__name__}) = '{string_price}'")

    print("\nCorrect comparisons:")
    print(f"numeric_price > 2000 -> {numeric_price > 2000}")
    print(f"string_price == '2100' -> {string_price == '2100'}")

    print("\nSafe conversion before numeric compare:")
    converted = int(string_price)
    print(f"int(string_price) > 2000 -> {converted > 2000}")

    print("\nIncorrect pattern to avoid:")
    print("Comparing int and str directly, e.g., numeric_price > string_price, raises TypeError.")


def run_demo():
    print("=" * 64)
    print("CONDITIONALS, COMPARISONS, AND LOGICAL OPERATORS")
    print("=" * 64)

    # Numeric if/elif/else paths
    evaluate_price_risk(1400)  # if path
    evaluate_price_risk(2000)  # elif path
    evaluate_price_risk(2600)  # else path

    # String comparison paths
    evaluate_region("Maharashtra")
    evaluate_region("karnataka")
    evaluate_region("Gujarat")

    # Logical operator paths
    evaluate_crop_decision(price=2300, rainfall_mm=850, crop_name="Rice")
    evaluate_crop_decision(price=1700, rainfall_mm=420, crop_name="Millet")

    # Type-safe comparison examples
    compare_types_safely()

    print("\nSummary:")
    print("1. Use if/elif/else to model multiple decision paths.")
    print("2. Compare numbers with numbers, strings with strings.")
    print("3. Convert types explicitly before cross-type logic.")
    print("4. Use and/or/not to compose real-world decision rules.")


if __name__ == "__main__":
    run_demo()
