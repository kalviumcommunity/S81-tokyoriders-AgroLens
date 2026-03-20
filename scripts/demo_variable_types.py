"""
Variable Types and Operations Demo
===================================

This script demonstrates the differences between numeric and string variables,
their operations, and proper type usage for data science workflows.
"""


def demonstrate_numeric_variables():
    """
    Demonstrate numeric variable operations (int and float).
    """
    print("=" * 60)
    print("NUMERIC VARIABLES")
    print("=" * 60)
    
    # Integer variables
    crop_count = 5
    total_yield = 1200
    
    print(f"\nInteger Variables:")
    print(f"  crop_count = {crop_count} (type: {type(crop_count).__name__})")
    print(f"  total_yield = {total_yield} (type: {type(total_yield).__name__})")
    
    # Numeric operations on integers
    print(f"\nInteger Operations:")
    print(f"  {crop_count} + 3 = {crop_count + 3}")
    print(f"  {total_yield} * 2 = {total_yield * 2}")
    print(f"  {total_yield} / {crop_count} = {total_yield / crop_count}")
    print(f"  {total_yield} // {crop_count} = {total_yield // crop_count} (integer division)")
    print(f"  {total_yield} % {crop_count} = {total_yield % crop_count} (modulo)")
    
    # Float variables
    avg_price = 1950.75
    rainfall = 45.3
    
    print(f"\nFloat Variables:")
    print(f"  avg_price = {avg_price} (type: {type(avg_price).__name__})")
    print(f"  rainfall = {rainfall} (type: {type(rainfall).__name__})")
    
    # Numeric operations on floats
    print(f"\nFloat Operations:")
    print(f"  {avg_price} + 100.5 = {avg_price + 100.5}")
    print(f"  {rainfall} * 2 = {rainfall * 2}")
    print(f"  {avg_price} / 5 = {avg_price / 5}")
    print(f"  round({rainfall}, 1) = {round(rainfall, 1)}")
    
    # Mixed numeric operations
    print(f"\nMixed Numeric (int + float):")
    result = crop_count + avg_price
    print(f"  {crop_count} (int) + {avg_price} (float) = {result} (type: {type(result).__name__})")


def demonstrate_string_variables():
    """
    Demonstrate string variable operations.
    """
    print("\n" + "=" * 60)
    print("STRING VARIABLES")
    print("=" * 60)
    
    # String variables
    crop_name = "Rice"
    region = "Maharashtra"
    
    print(f"\nString Variables:")
    print(f"  crop_name = '{crop_name}' (type: {type(crop_name).__name__})")
    print(f"  region = '{region}' (type: {type(region).__name__})")
    
    # String operations
    print(f"\nString Operations:")
    print(f"  Concatenation: '{crop_name}' + ' from ' + '{region}' = '{crop_name} from {region}'")
    print(f"  Repetition: '{crop_name}' * 3 = '{crop_name * 3}'")
    print(f"  Length: len('{crop_name}') = {len(crop_name)}")
    print(f"  Uppercase: '{crop_name}'.upper() = '{crop_name.upper()}'")
    print(f"  Lowercase: '{region}'.lower() = '{region.lower()}'")
    
    # String indexing and slicing
    print(f"\nString Indexing & Slicing:")
    print(f"  '{crop_name}'[0] = '{crop_name[0]}' (first character)")
    print(f"  '{crop_name}'[-1] = '{crop_name[-1]}' (last character)")
    print(f"  '{crop_name}'[0:2] = '{crop_name[0:2]}' (slice: characters 0-1)")


def demonstrate_type_conversion():
    """
    Demonstrate conversion between numeric and string types.
    """
    print("\n" + "=" * 60)
    print("TYPE CONVERSION")
    print("=" * 60)
    
    # String to numeric
    price_str = "2100"
    quantity_str = "5.5"
    
    print(f"\nString to Numeric:")
    print(f"  price_str = '{price_str}' (type: {type(price_str).__name__})")
    price_num = int(price_str)
    print(f"  int(price_str) = {price_num} (type: {type(price_num).__name__})")
    
    print(f"\n  quantity_str = '{quantity_str}' (type: {type(quantity_str).__name__})")
    quantity_num = float(quantity_str)
    print(f"  float(quantity_str) = {quantity_num} (type: {type(quantity_num).__name__})")
    
    # Numeric to string
    crop_id = 42
    avg_yield = 1500.75
    
    print(f"\nNumeric to String:")
    print(f"  crop_id = {crop_id} (type: {type(crop_id).__name__})")
    id_str = str(crop_id)
    print(f"  str(crop_id) = '{id_str}' (type: {type(id_str).__name__})")
    
    print(f"\n  avg_yield = {avg_yield} (type: {type(avg_yield).__name__})")
    yield_str = str(avg_yield)
    print(f"  str(avg_yield) = '{yield_str}' (type: {type(yield_str).__name__})")


def demonstrate_type_errors():
    """
    Demonstrate common type-related errors and how to avoid them.
    """
    print("\n" + "=" * 60)
    print("TYPE ERRORS & HOW TO AVOID THEM")
    print("=" * 60)
    
    # Error 1: Adding number and string
    print(f"\nError 1: Cannot add int + str directly")
    price = 100
    currency = " Rs"
    print(f"  price = {price} (int)")
    print(f"  currency = '{currency}' (str)")
    print(f"  price + currency → TypeError!")
    print(f"  Solution: str(price) + currency = '{str(price) + currency}'")
    
    # Error 2: String math operations
    print(f"\nError 2: String operations behave differently than numeric")
    num1 = 5
    num2 = 3
    str1 = "5"
    str2 = "3"
    print(f"  num1 = {num1}, num2 = {num2} → {num1} + {num2} = {num1 + num2} (arithmetic)")
    print(f"  str1 = '{str1}', str2 = '{str2}' → str1 + str2 = '{str1 + str2}' (concatenation)")
    print(f"  To add strings as numbers: int(str1) + int(str2) = {int(str1) + int(str2)}")
    
    # Error 3: Empty string vs zero
    print(f"\nCommon Confusion: Empty string vs zero")
    empty_str = ""
    zero_int = 0
    zero_float = 0.0
    print(f"  empty_str = '{empty_str}' → bool(empty_str) = {bool(empty_str)} (False)")
    print(f"  zero_int = {zero_int} → bool(zero_int) = {bool(zero_int)} (False)")
    print(f"  zero_float = {zero_float} → bool(zero_float) = {bool(zero_float)} (False)")
    print(f"  BUT: '0' (string zero) → bool('0') = {bool('0')} (True, non-empty string)")


def demonstrate_practical_usage():
    """
    Demonstrate practical type usage in data science workflows.
    """
    print("\n" + "=" * 60)
    print("PRACTICAL DATA SCIENCE USAGE")
    print("=" * 60)
    
    # Simulating a crop record
    print(f"\nCrop Record Example:")
    
    crop_id = 101                    # int: unique identifier
    crop_name = "Wheat"              # str: descriptive label
    area_hectares = 25.5             # float: precise measurement
    yield_kg = 1500                  # int: count-based metric
    price_per_kg = 32.75             # float: currency value
    is_organic = True                # bool: flag
    
    print(f"  crop_id = {crop_id} ({type(crop_id).__name__})")
    print(f"  crop_name = '{crop_name}' ({type(crop_name).__name__})")
    print(f"  area_hectares = {area_hectares} ({type(area_hectares).__name__})")
    print(f"  yield_kg = {yield_kg} ({type(yield_kg).__name__})")
    print(f"  price_per_kg = {price_per_kg} ({type(price_per_kg).__name__})")
    print(f"  is_organic = {is_organic} ({type(is_organic).__name__})")
    
    # Calculations
    print(f"\nCalculations:")
    total_yield = area_hectares * yield_kg
    print(f"  Total yield = area_hectares * yield_kg")
    print(f"               = {area_hectares} * {yield_kg} = {total_yield} kg")
    
    total_revenue = total_yield * price_per_kg
    print(f"  Total revenue = total_yield * price_per_kg")
    print(f"                = {total_yield} * {price_per_kg} = Rs {total_revenue:.2f}")
    
    # String formatting for output
    report = f"Crop {crop_id}: {crop_name.upper()} | {area_hectares} ha | Rs {total_revenue:.2f}"
    print(f"  Report: {report}")


if __name__ == "__main__":
    demonstrate_numeric_variables()
    demonstrate_string_variables()
    demonstrate_type_conversion()
    demonstrate_type_errors()
    demonstrate_practical_usage()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
Key Takeaways:
1. Numeric types (int, float) support arithmetic: +, -, *, /, //, %
2. String types support concatenation (+), repetition (*), and methods (upper, lower)
3. Mixing numeric + string without conversion causes TypeError
4. Always convert types explicitly when needed: int(), float(), str()
5. In data science: use numbers for calculations, strings for labels/descriptions
6. Boolean type (True/False) is useful for flags and conditions
    """)
