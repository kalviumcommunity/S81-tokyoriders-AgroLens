"""
Loops Demo: for, while, range/collections, break, continue
===========================================================

This script demonstrates:
1. for loops and while loops
2. Iteration over ranges and collections
3. Conditional control inside loops
4. Correct use of break and continue
"""


def demo_for_with_range():
    print("=" * 62)
    print("FOR LOOP WITH RANGE")
    print("=" * 62)

    # Iterate over numeric range
    for day in range(1, 6):
        demand_index = day * 10
        print(f"Day {day}: demand_index={demand_index}")


def demo_for_with_collection():
    print("\n" + "=" * 62)
    print("FOR LOOP WITH COLLECTION")
    print("=" * 62)

    crops = ["Rice", "Wheat", "Maize", "Cotton", "Millet"]

    # Iterate directly over values
    for crop in crops:
        print(f"Crop: {crop}")

    # Iterate with index + value
    print("\nIndexed iteration:")
    for idx, crop in enumerate(crops):
        print(f"Index {idx}: {crop}")


def demo_continue_in_for():
    print("\n" + "=" * 62)
    print("FOR LOOP WITH CONTINUE")
    print("=" * 62)

    rainfall_mm = [450, 820, 300, 910, 700]

    print("Skipping low-rainfall entries (< 500 mm):")
    for value in rainfall_mm:
        if value < 500:
            print(f"{value} mm -> continue (skip)")
            continue
        print(f"{value} mm -> accepted for analysis")


def demo_break_in_for():
    print("\n" + "=" * 62)
    print("FOR LOOP WITH BREAK")
    print("=" * 62)

    market_prices = [1750, 1880, 2050, 2120, 1980]
    alert_threshold = 2000

    for price in market_prices:
        if price >= alert_threshold:
            print(f"Break condition met at price={price} (>= {alert_threshold})")
            break
        print(f"Price {price} below threshold, continue scanning")


def demo_while_loop():
    print("\n" + "=" * 62)
    print("WHILE LOOP WITH CONDITION")
    print("=" * 62)

    soil_moisture = 30

    # Continue until target moisture reached
    while soil_moisture < 50:
        print(f"Current moisture: {soil_moisture}% -> irrigation step")
        soil_moisture += 5

    print(f"Target reached: {soil_moisture}%")


def demo_while_break_continue():
    print("\n" + "=" * 62)
    print("WHILE LOOP WITH BREAK AND CONTINUE")
    print("=" * 62)

    readings = [42, -1, 46, 49, 60, 48]
    i = 0

    # Rules:
    # - continue on invalid reading (-1)
    # - break if critical high reading (>= 60)
    while i < len(readings):
        value = readings[i]
        i += 1

        if value == -1:
            print("Invalid sensor value -> continue")
            continue

        if value >= 60:
            print(f"Critical reading {value} detected -> break")
            break

        print(f"Normal reading {value} processed")


def run_demo():
    demo_for_with_range()
    demo_for_with_collection()
    demo_continue_in_for()
    demo_break_in_for()
    demo_while_loop()
    demo_while_break_continue()

    print("\nSummary:")
    print("1. for loop is best for known ranges/collections.")
    print("2. while loop is best for condition-driven repetition.")
    print("3. continue skips current iteration safely.")
    print("4. break exits loop immediately when stop condition is met.")


if __name__ == "__main__":
    run_demo()
