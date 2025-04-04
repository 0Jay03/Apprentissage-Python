from collections import defaultdict
import json

from utils.utils import load_json


# Ensure this import is correct

def normalize_string(text):
    """Normalize a string by converting ß to ss, removing extra spaces, and making it lowercase."""
    return str(text).replace('ß', 'ss').strip().lower().replace("  ", " ")

def get_material_key(material):
    """Create a unique key for a material based on name and manufacturer."""
    name = normalize_string(material.get("name", ""))
    manufacturer = normalize_string(material.get("manufacturer", ""))
    return (name, manufacturer)

def find_duplicate_keys(materials):
    """Find materials with duplicate (name, manufacturer) keys."""
    key_count = defaultdict(int)
    for material in materials:
        key = get_material_key(material)
        key_count[key] += 1

    # Filter keys that appear more than once
    duplicates = {key: count for key, count in key_count.items() if count > 1}
    return duplicates

def compare_materials(file1_path, file2_path, output_json_path="missing_materials.json"):
    """
    Compare two JSON files to find duplicate keys in file1 and missing materials in file2.

    Args:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_json_path (str): Path to save the missing materials JSON file. Default is "missing_materials.json".

    Returns:
        list: A list of missing materials.
    """
    # Load JSON data
    materials1 = load_json(file1_path)
    materials2 = load_json(file2_path)

    # Find and print duplicate keys in file1
    duplicate_keys = find_duplicate_keys(materials1)
    print(f"Found {len(duplicate_keys)} duplicate keys:")
    for key, count in duplicate_keys.items():
        print(f"Key: {key}, Count: {count}")

    # Create sets of unique material keys
    keys1 = {get_material_key(material) for material in materials1}
    keys2 = {get_material_key(material) for material in materials2}

    # Find missing keys
    missing_keys = keys1 - keys2

    # Find corresponding materials
    missing_materials = [
        material for material in materials1
        if get_material_key(material) in missing_keys
    ]

    # Save missing materials to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as outfile:
        json.dump(missing_materials, outfile, ensure_ascii=False, indent=4)
    print(f"\nMissing materials saved to '{output_json_path}'.")

    # Print missing materials
    print(f"\nFound {len(missing_materials)} missing materials:")
    for material in missing_materials:
        print(f"Name: {material['name']}, Manufacturer: {material['manufacturer']}")

    return missing_materials