"""
Data Structures Demo: Lists, Tuples, and Dictionaries
======================================================

This script demonstrates creation, access, modification, and immutability
of Python's core data structures with practical agriculture examples.
"""


def demonstrate_lists():
    """
    Demonstrate list creation, indexing, slicing, and modification.
    Lists are MUTABLE - they can be modified after creation.
    """
    print("=" * 70)
    print("LISTS (MUTABLE)")
    print("=" * 70)
    
    # List creation
    crops = ["Rice", "Wheat", "Maize", "Sugarcane", "Cotton"]
    prices = [2100, 1950, 1800, 2500, 5000]
    
    print(f"\nList Creation:")
    print(f"  crops = {crops}")
    print(f"  prices = {prices}")
    print(f"  type(crops) = {type(crops)}")
    
    # Indexing (0-based)
    print(f"\nIndexing (0-based):")
    print(f"  crops[0] = '{crops[0]}' (first element)")
    print(f"  crops[-1] = '{crops[-1]}' (last element)")
    print(f"  crops[2] = '{crops[2]}' (third element)")
    
    # Slicing
    print(f"\nSlicing:")
    print(f"  crops[0:3] = {crops[0:3]} (first 3 elements)")
    print(f"  crops[1:4] = {crops[1:4]} (elements 1-3)")
    print(f"  crops[::2] = {crops[::2]} (every other element)")
    print(f"  crops[::-1] = {crops[::-1]} (reversed)")
    
    # Length
    print(f"\nLength:")
    print(f"  len(crops) = {len(crops)}")
    
    # MODIFICATION - Lists are mutable
    print(f"\nMODIFICATION (Mutable behavior):")
    print(f"  Original: crops = {crops}")
    
    crops[0] = "Paddy"  # Change first element
    print(f"  After crops[0] = 'Paddy': {crops}")
    
    crops.append("Barley")  # Add element
    print(f"  After crops.append('Barley'): {crops}")
    
    crops.insert(2, "Pulses")  # Insert at position
    print(f"  After crops.insert(2, 'Pulses'): {crops}")
    
    crops.remove("Cotton")  # Remove by value
    print(f"  After crops.remove('Cotton'): {crops}")
    
    popped = crops.pop()  # Remove last element
    print(f"  After crops.pop(): {crops} (popped: '{popped}')")
    
    # List operations
    print(f"\nList Operations:")
    combined = crops + ["Sorghum"]
    print(f"  crops + ['Sorghum'] = {combined}")
    
    repeated = ["Rice", "Wheat"] * 2
    print(f"  ['Rice', 'Wheat'] * 2 = {repeated}")
    
    print(f"  'Maize' in crops = {'Maize' in crops}")
    print(f"  'Cotton' in crops = {'Cotton' in crops}")


def demonstrate_tuples():
    """
    Demonstrate tuple creation, indexing, and IMMUTABILITY.
    Tuples are IMMUTABLE - they cannot be modified after creation.
    """
    print("\n" + "=" * 70)
    print("TUPLES (IMMUTABLE)")
    print("=" * 70)
    
    # Tuple creation
    coordinates = (28.6139, 77.2090)  # Latitude, Longitude
    crop_info = ("Rice", 2100, 1200, True)
    empty_tuple = ()
    single_tuple = (42,)  # Note comma for single element
    
    print(f"\nTuple Creation:")
    print(f"  coordinates = {coordinates}")
    print(f"  crop_info = {crop_info}")
    print(f"  empty_tuple = {empty_tuple}")
    print(f"  single_tuple = {single_tuple}")
    print(f"  type(coordinates) = {type(coordinates)}")
    
    # Indexing (same as lists)
    print(f"\nIndexing:")
    print(f"  coordinates[0] = {coordinates[0]} (latitude)")
    print(f"  coordinates[-1] = {coordinates[-1]} (longitude)")
    print(f"  crop_info[1] = {crop_info[1]} (price)")
    
    # Slicing (same as lists)
    print(f"\nSlicing:")
    print(f"  crop_info[0:2] = {crop_info[0:2]}")
    print(f"  crop_info[1:] = {crop_info[1:]}")
    
    # IMMUTABILITY - Tuples cannot be modified
    print(f"\nIMMUTABILITY (Cannot modify):")
    print(f"  Attempting: crop_info[0] = 'Wheat'")
    try:
        crop_info[0] = "Wheat"
    except TypeError as e:
        print(f"  ✗ ERROR: {e}")
    
    print(f"  Attempting: crop_info.append('Sugarcane')")
    try:
        crop_info.append("Sugarcane")
    except AttributeError as e:
        print(f"  ✗ ERROR: {type(e).__name__} - tuples have no append method")
    
    print(f"  Original tuple unchanged: crop_info = {crop_info}")
    
    # Tuple unpacking
    print(f"\nTuple Unpacking:")
    lat, lon = coordinates
    print(f"  lat, lon = coordinates")
    print(f"  lat = {lat}, lon = {lon}")
    
    crop_name, price, yield_amt, is_certified = crop_info
    print(f"  crop_name, price, yield_amt, is_certified = crop_info")
    print(f"  crop_name = '{crop_name}', price = {price}, yield = {yield_amt}, certified = {is_certified}")
    
    # Immutable use cases
    print(f"\nWhy Tuples (Immutable)?")
    print(f"  1. Safer as function arguments - cannot be accidentally modified")
    print(f"  2. Can be used as dictionary keys (unlike lists)")
    print(f"  3. Slightly more memory efficient than lists")


def demonstrate_dictionaries():
    """
    Demonstrate dictionary creation, key access, and modification.
    Dictionaries are MUTABLE - keys and values can be changed.
    """
    print("\n" + "=" * 70)
    print("DICTIONARIES (MUTABLE)")
    print("=" * 70)
    
    # Dictionary creation
    crop_dict = {
        "name": "Rice",
        "price": 2100,
        "yield_per_ha": 1200,
        "is_organic": True,
        "region": "Tamil Nadu"
    }
    
    print(f"\nDictionary Creation:")
    print(f"  crop_dict = {crop_dict}")
    print(f"  type(crop_dict) = {type(crop_dict)}")
    
    # Key access
    print(f"\nKey Access:")
    print(f"  crop_dict['name'] = '{crop_dict['name']}'")
    print(f"  crop_dict['price'] = {crop_dict['price']}")
    print(f"  crop_dict.get('region') = '{crop_dict.get('region')}'")
    print(f"  crop_dict.get('area', 'N/A') = '{crop_dict.get('area', 'N/A')}' (with default)")
    
    # Dictionary methods
    print(f"\nDictionary Methods:")
    print(f"  crop_dict.keys() = {list(crop_dict.keys())}")
    print(f"  crop_dict.values() = {list(crop_dict.values())}")
    print(f"  crop_dict.items() = {list(crop_dict.items())}")
    print(f"  len(crop_dict) = {len(crop_dict)}")
    
    # MODIFICATION - Dictionaries are mutable
    print(f"\nMODIFICATION (Mutable behavior):")
    print(f"  Original: crop_dict = {crop_dict}")
    
    crop_dict["price"] = 2200  # Update existing key
    print(f"  After crop_dict['price'] = 2200: {crop_dict['price']}")
    
    crop_dict["area_hectares"] = 25.5  # Add new key
    print(f"  After crop_dict['area_hectares'] = 25.5:")
    print(f"    Keys now include 'area_hectares': {list(crop_dict.keys())}")
    
    crop_dict.update({"market": "APMC", "harvest_date": "2026-10-15"})  # Add multiple keys
    print(f"  After update with market and harvest_date:")
    print(f"    crop_dict = {crop_dict}")
    
    removed_value = crop_dict.pop("region")  # Remove key and get value
    print(f"  After crop_dict.pop('region'): removed '{removed_value}'")
    print(f"    Remaining keys: {list(crop_dict.keys())}")
    
    # Nested dictionaries
    print(f"\nNested Dictionaries:")
    farm_data = {
        "farm_id": 101,
        "location": {"latitude": 28.6139, "longitude": 77.2090},
        "crops": {
            "rice": {"area": 10, "yield": 50},
            "wheat": {"area": 15, "yield": 45}
        }
    }
    print(f"  farm_data = {farm_data}")
    print(f"  farm_data['location']['latitude'] = {farm_data['location']['latitude']}")
    print(f"  farm_data['crops']['rice']['yield'] = {farm_data['crops']['rice']['yield']}")
    
    farm_data["crops"]["rice"]["yield"] = 55  # Modify nested value
    print(f"  After modifying rice yield to 55:")
    print(f"    farm_data['crops']['rice'] = {farm_data['crops']['rice']}")


def demonstrate_iteration():
    """
    Demonstrate iteration over lists, tuples, and dictionaries.
    """
    print("\n" + "=" * 70)
    print("ITERATION OVER DATA STRUCTURES")
    print("=" * 70)
    
    # List iteration
    print(f"\nIterating over List:")
    crops = ["Rice", "Wheat", "Maize"]
    for i, crop in enumerate(crops):
        print(f"  {i}: {crop}")
    
    # Tuple iteration
    print(f"\nIterating over Tuple:")
    prices = (2100, 1950, 1800)
    for price in prices:
        print(f"  Price: {price}")
    
    # Dictionary iteration
    print(f"\nIterating over Dictionary:")
    crop_info = {"name": "Rice", "price": 2100, "region": "Asia"}
    
    print(f"  Keys:")
    for key in crop_info.keys():
        print(f"    {key}")
    
    print(f"  Values:")
    for value in crop_info.values():
        print(f"    {value}")
    
    print(f"  Key-Value pairs:")
    for key, value in crop_info.items():
        print(f"    {key}: {value}")


def demonstrate_practical_usage():
    """
    Demonstrate practical agriculture data structure usage.
    """
    print("\n" + "=" * 70)
    print("PRACTICAL AGRICULTURE DATA STRUCTURES")
    print("=" * 70)
    
    # Farm inventory: list of dictionaries
    print(f"\nFarm Inventory (List of Dictionaries):")
    inventory = [
        {"crop": "Rice", "quantity_kg": 5000, "location": "Warehouse A"},
        {"crop": "Wheat", "quantity_kg": 3500, "location": "Warehouse B"},
        {"crop": "Maize", "quantity_kg": 2000, "location": "Warehouse A"}
    ]
    print(f"  inventory = {inventory}")
    
    print(f"\n  Accessing first crop: {inventory[0]['crop']} in {inventory[0]['location']}")
    total_quantity = sum(item["quantity_kg"] for item in inventory)
    print(f"  Total quantity: {total_quantity} kg")
    
    # Crop properties: dictionary with tuple keys
    print(f"\nCrop Properties (Dictionary with Tuple Keys):")
    crop_properties = {
        ("Rice", "Asia"): {"rainfall": 1500, "temperature": 25},
        ("Wheat", "Europe"): {"rainfall": 500, "temperature": 15},
        ("Maize", "Americas"): {"rainfall": 600, "temperature": 20}
    }
    print(f"  Looking up rice in Asia: {crop_properties[('Rice', 'Asia')]}")
    
    rice_props = crop_properties[("Rice", "Asia")]
    print(f"  Rice requires {rice_props['rainfall']}mm rainfall and {rice_props['temperature']}°C temp")
    
    # Immutable coordinates as dictionary keys
    print(f"\nUsing Tuples as Dictionary Keys (Immutable):")
    field_locations = {
        (28.6139, 77.2090): "Field A",
        (28.7041, 77.1025): "Field B",
        (28.5355, 77.3910): "Field C"
    }
    print(f"  Field at (28.6139, 77.2090): {field_locations[(28.6139, 77.2090)]}")


def demonstrate_mutability_example():
    """
    Demonstrate the practical implications of mutability vs immutability.
    """
    print("\n" + "=" * 70)
    print("MUTABILITY IMPLICATIONS")
    print("=" * 70)
    
    print(f"\nScenario: Passing data to a function")
    
    def process_crop_list(crops):
        """Function that modifies a list."""
        crops.append("Sorghum")
        return len(crops)
    
    def process_crop_tuple(crops):
        """Function that tries to modify a tuple (will fail safely)."""
        try:
            crops = crops + ("Sorghum",)  # Creates new tuple
            return crops
        except TypeError:
            return crops
    
    # List: modified by function
    print(f"\n  List (Mutable):")
    my_crops = ["Rice", "Wheat"]
    print(f"    Before: {my_crops}")
    count = process_crop_list(my_crops)
    print(f"    After function call: {my_crops} (MODIFIED)")
    
    # Tuple: safe from modification
    print(f"\n  Tuple (Immutable):")
    my_crops_tuple = ("Rice", "Wheat")
    print(f"    Before: {my_crops_tuple}")
    result = process_crop_tuple(my_crops_tuple)
    print(f"    After function call: {my_crops_tuple} (UNCHANGED - Safe!)")


if __name__ == "__main__":
    demonstrate_lists()
    demonstrate_tuples()
    demonstrate_dictionaries()
    demonstrate_iteration()
    demonstrate_practical_usage()
    demonstrate_mutability_example()
    
    print("\n" + "=" * 70)
    print("SUMMARY & KEY TAKEAWAYS")
    print("=" * 70)
    print("""
1. LISTS [item1, item2] - MUTABLE
   - Use: Dynamic data that needs modification
   - Access: By index (0-based)
   - Methods: append, insert, remove, pop
   - Ordered, can have duplicates

2. TUPLES (item1, item2) - IMMUTABLE
   - Use: Fixed data that cannot change, or as dict keys
   - Access: By index (0-based)
   - Cannot be modified after creation
   - Slightly more efficient than lists

3. DICTIONARIES {key: value} - MUTABLE
   - Use: Structured named data, fast lookups
   - Access: By key (can be any immutable type)
   - Keys must be unique and immutable (use tuples, not lists)
   - Methods: keys(), values(), items(), get(), update(), pop()

4. MUTABILITY MATTERS
   - Mutable (list, dict): Can be modified in place
   - Immutable (tuple, str): Cannot be changed; functions are safer
   - Use tuples as dict keys; lists cannot be keys
   - Pass tuples to functions if you don't want unintended modifications

5. PRACTICAL USAGE IN DATA SCIENCE
   - Lists: Collections of records that grow or shrink
   - Dictionaries: Structured records with named fields
   - Tuples: Coordinates, fixed configurations, dictionary keys
    """)
