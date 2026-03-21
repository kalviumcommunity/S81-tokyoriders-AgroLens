"""
Data Preparation Script for AgroLens Project
============================================

This script demonstrates basic data processing logic for the AgroLens project.
It handles crop price normalization and risk score calculation.
"""

import csv


def load_crop_data(file_path):
    """
    Load crop price data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing crop data.
        
    Returns:
        list: List of dictionaries with crop data.
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []


def normalize_prices(crop_data):
    """
    Normalize crop prices to a 0-100 scale based on min-max normalization.
    
    Args:
        crop_data (list): List of dictionaries with 'crop' and 'price' keys.
        
    Returns:
        list: Data with added 'normalized_price' field.
    """
    if not crop_data:
        return crop_data

    # Parse prices defensively to avoid breaking the pipeline on bad rows.
    prices = []
    for row in crop_data:
        try:
            prices.append(float(row.get('price', 0)))
        except ValueError:
            prices.append(0)
    
    price_min = min(prices) if prices else 0
    price_max = max(prices) if prices else 0
    price_range = price_max - price_min if price_max > price_min else 1
    
    for index, row in enumerate(crop_data):
        normalized = ((prices[index] - price_min) / price_range) * 100 if price_range > 0 else 0
        row['normalized_price'] = round(normalized, 2)
    
    return crop_data


def calculate_risk_score(crop_data):
    """
    Calculate a simple risk score for each crop based on price volatility.
    
    Args:
        crop_data (list): List of dictionaries with price data.
        
    Returns:
        list: Data with added 'risk_score' field (0-10 scale).
    """
    for row in crop_data:
        try:
            # Higher normalized price is treated as lower downside risk.
            normalized = float(row.get('normalized_price', 50))
            risk_score = max(0, 10 - (normalized / 10))
            row['risk_score'] = round(risk_score, 2)
        except (ValueError, TypeError):
            row['risk_score'] = 5.0
    
    return crop_data


def save_processed_data(data, output_file_path):
    """
    Save processed data to a CSV file.
    
    Args:
        data (list): List of dictionaries with processed data.
        output_file_path (str): Path where output CSV will be saved.
    """
    if not data:
        print("No data to save.")
        return

    try:
        fieldnames = list(data[0].keys())
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to '{output_file_path}'")
    except Exception as error:
        print(f"Error saving file: {error}")


def process_crop_data(input_file, output_file):
    """
    Main pipeline: load, normalize, calculate risk, and save crop data.
    
    Args:
        input_file (str): Input CSV filepath.
        output_file (str): Output CSV filepath.
    """
    print(f"Processing crop data from '{input_file}'...")

    crop_data = load_crop_data(input_file)
    if not crop_data:
        print("No data loaded. Exiting.")
        return

    print(f"Loaded {len(crop_data)} records.")

    crop_data = normalize_prices(crop_data)
    print("Prices normalized.")

    crop_data = calculate_risk_score(crop_data)
    print("Risk scores calculated.")

    save_processed_data(crop_data, output_file)
    print("Processing complete.")


if __name__ == "__main__":
    input_path = "../data/raw/sample_crops.csv"
    output_path = "../data/processed/processed_crops_v1.csv"

    process_crop_data(input_path, output_path)
