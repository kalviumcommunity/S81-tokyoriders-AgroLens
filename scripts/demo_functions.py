"""
Functions Demo: def, arguments, calls, and execution flow
=========================================================

This script demonstrates:
1. Defining functions using def
2. Calling functions from code
3. Passing arguments correctly
4. Observing function execution step by step
"""


def calculate_total_revenue(crop_name, quantity_kg, price_per_kg):
    """Return total revenue for a crop sale."""
    print(f"[calculate_total_revenue] Called with crop_name={crop_name}, quantity_kg={quantity_kg}, price_per_kg={price_per_kg}")
    total = quantity_kg * price_per_kg
    print(f"[calculate_total_revenue] Computed total={total}")
    return total


def classify_risk(expected_rainfall_mm, min_required_mm=600):
    """Classify rainfall risk using a required threshold."""
    print(f"[classify_risk] Called with expected_rainfall_mm={expected_rainfall_mm}, min_required_mm={min_required_mm}")

    if expected_rainfall_mm >= min_required_mm:
        result = "low_risk"
    elif expected_rainfall_mm >= 450:
        result = "moderate_risk"
    else:
        result = "high_risk"

    print(f"[classify_risk] Returning {result}")
    return result


def build_crop_report(crop_name, revenue, risk_level):
    """Create and return a formatted crop report string."""
    print(f"[build_crop_report] Called with crop_name={crop_name}, revenue={revenue}, risk_level={risk_level}")
    report = f"Crop={crop_name} | Revenue=Rs {revenue:.2f} | RainfallRisk={risk_level}"
    print("[build_crop_report] Report built")
    return report


def demo_argument_passing():
    """Show positional, keyword, and default argument usage."""
    print("\n=== Argument Passing Demo ===")

    # Positional arguments
    rev1 = calculate_total_revenue("Rice", 1200, 32.5)
    print(f"Positional call result: {rev1}\n")

    # Keyword arguments (order does not matter)
    rev2 = calculate_total_revenue(quantity_kg=800, price_per_kg=28.0, crop_name="Wheat")
    print(f"Keyword call result: {rev2}\n")

    # Default argument used (min_required_mm defaults to 600)
    risk1 = classify_risk(520)
    print(f"Default-arg call result: {risk1}\n")

    # Override default argument
    risk2 = classify_risk(expected_rainfall_mm=520, min_required_mm=500)
    print(f"Override-default call result: {risk2}\n")


def run_pipeline(crop_name, quantity_kg, price_per_kg, rainfall_mm):
    """Run a mini function pipeline and show call chain clearly."""
    print("\n=== Function Execution Pipeline ===")
    print("Step 1: calculate_total_revenue")
    revenue = calculate_total_revenue(crop_name, quantity_kg, price_per_kg)

    print("Step 2: classify_risk")
    risk_level = classify_risk(rainfall_mm)

    print("Step 3: build_crop_report")
    report = build_crop_report(crop_name, revenue, risk_level)

    print("Step 4: return final report")
    return report


def main():
    print("=" * 66)
    print("PYTHON FUNCTIONS: DEFINITION, CALLS, ARGUMENTS, EXECUTION FLOW")
    print("=" * 66)

    demo_argument_passing()

    final_report = run_pipeline(
        crop_name="Maize",
        quantity_kg=1500,
        price_per_kg=24.75,
        rainfall_mm=430,
    )

    print("\nFinal Output:")
    print(final_report)

    print("\nObservations:")
    print("1. Functions are defined with def and reusable for different inputs.")
    print("2. Arguments can be positional or keyword-based.")
    print("3. Default values simplify calls when common settings exist.")
    print("4. Return values let one function feed another in a pipeline.")


if __name__ == "__main__":
    main()
