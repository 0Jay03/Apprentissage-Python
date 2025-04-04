import json
import re

import pandas as pd
from rapidfuzz import process, fuzz
import os, glob
from datetime import datetime

# Helper Functions
def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



def fuzzy_match(target, choices, threshold=90):
    """Performs fuzzy matching on a target against a list of choices, with a specified threshold."""
    match, score, *_ = process.extractOne(target, choices, scorer=fuzz.token_sort_ratio) or (None, 0)
    return match if score >= threshold else None

# Function to capitalize the first letter of manufacturerName
def capitalize_first_letter(text):
    """Ensures only the first letter is capitalized, leaving the rest as is."""
    return text.capitalize() if text else text

def handle_na(value):
    return "" if pd.isna(value) else value


def find_closest_match(target, candidates):

        # This is a placeholder for actual matching logic, which might use fuzzy matching, etc.
        from difflib import get_close_matches
        matches = get_close_matches(target, candidates)
        return matches[0] if matches else None

def get_storage_path(name, manufacturer, application_field_pos):
        """
        Construct a directory path based on the given name and manufacturer.

        Args:
            name (str): The name of the product.
            manufacturer (str): The manufacturer of the product.
            application_field_pos (str): The application_field_pos of the product.

        Returns:
            str or None: The path to the storage directory, or None if no match is found.
        """
        # Construct the base path for file storage
        base_path = os.path.join('"../data_pic_pdf"', application_field_pos[0],
                                 '.'.join(application_field_pos[:2]))

        # Check if the base path exists and list folders
        available_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))] \
            if os.path.exists(base_path) else []

        # Step 1: Match manufacturer first
        best_manufacturer_match = find_closest_match(manufacturer, available_folders) if manufacturer else None

        if best_manufacturer_match:
            # Step 2: Match name inside the best manufacturer folder
            manufacturer_path = os.path.join(base_path, best_manufacturer_match)
            available_names = [f for f in os.listdir(manufacturer_path) if
                               os.path.isdir(os.path.join(manufacturer_path, f))]
            best_name_match = find_closest_match(name, available_names) if available_names else None
        else:
            # No manufacturer match, try to match name directly in base path
            best_name_match = find_closest_match(name, available_folders)

        # Finalize the folder path
        if best_manufacturer_match and best_name_match:
            final_directory_path = os.path.join(base_path, best_manufacturer_match, best_name_match)
        elif best_name_match:
            final_directory_path = os.path.join(base_path, best_name_match)
        else:
            final_directory_path = None

        return final_directory_path

def find_existing_files(directory, predefined_patterns):
    """Search for multiple specific files in a directory and replace missing ones with extra PDFs."""
    files_found = {}
    # Find predefined files
    for key, pattern in predefined_patterns.items():
        found_files = glob.glob(os.path.join(directory, pattern))
        if found_files:
            files_found[key] = found_files[0]

    # Find all available PDFs
    all_pdfs = glob.glob(os.path.join(directory, "*.pdf"))
    predefined_files = set(files_found.values())

    # Replace missing predefined keys with extra PDFs
    missing_keys = [key for key in predefined_patterns.keys() if key not in files_found]
    extra_pdfs = [pdf for pdf in all_pdfs if pdf not in predefined_files]

    for key, pdf in zip(missing_keys, extra_pdfs):  # Assign extra PDFs to missing keys
        files_found[key] = pdf

    return files_found  # Returns only existing or replaced files

def extract_numeric_prefix_regex(text):
        if not text.strip():  # Check if the text is empty or whitespace
            return None
        # Use a regex pattern to find the first occurrence of one or more numbers separated by dots
        match = re.search(r'\d+(\.\d+)*', text)
        if match:
            return match.group(0).strip()  # Return the matched group, stripped of any surrounding whitespace
        return None  # Return None if no match is found

def clean_and_trim_string(cell_value, max_length=100):
            if isinstance(cell_value, str):
                # Replace tabs, newlines, and remove spaces around slashes
                cleaned_value = cell_value.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
                #cleaned_value = cleaned_value.replace(' /', '/').replace('/ ', '/')
                # Trim the string to the maximum length
                return cleaned_value.strip()[:max_length]
            return cell_value

def filter_pdf_folders(input_path,folder_field, manufacturer_name, product_name, manufacturer_similarity_threshold=85,
                       product_similarity_threshold=40):
    """
    Filters JSON entries based on the manufacturer name and then selects entries with the highest similarity score for a product name within the 'pdf_folder'.

    Args:
    input_path (str): Path to the input JSON file.
    manufacturer_name (str): Manufacturer name to search for in the 'pdf_folder' paths.
    product_name (str): Product name to search for within the filtered results.
    manufacturer_similarity_threshold (int): Similarity threshold for manufacturer name matching (default 85).
    product_similarity_threshold (int): Similarity threshold for product name matching (default 40).

    Returns:
    dict: The entry with the highest product name similarity score within the manufacturer filtered results.
    """
    # Load JSON data from the specified file with UTF-8 encoding
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Precompute lowercase versions of the names to avoid repeated computation
    manufacturer_name_lower = manufacturer_name.lower()
    product_name_lower = product_name.lower()

    # Filter data based on manufacturer name and product name in a single pass
    best_match = None
    highest_score = 0

    for entry in data:
        pdf_folder_lower = extract_first_four_elements(entry[folder_field].lower())

        # Check manufacturer similarity
        manufacturer_score = fuzz.partial_ratio(manufacturer_name_lower, pdf_folder_lower)
        if manufacturer_score < manufacturer_similarity_threshold:
            continue  # Skip if manufacturer similarity is below threshold

        # Check product similarity
        product_score = fuzz.partial_ratio(product_name_lower, entry[folder_field].lower())
        if product_score >= product_similarity_threshold and product_score > highest_score:
            best_match = entry
            highest_score = product_score

            # Early exit if a perfect match is found
            if highest_score == 100:
                break

    return best_match

def extract_first_four_elements(path):
    """
    Extracts the first 4 elements from a path and joins them back into a string.

    Args:
        path (str): The input path string.

    Returns:
        str: The first 4 elements of the path joined by backslashes.
    """
    parts = path.split('\\')
    first_four_elements = parts[:4]
    return '\\'.join(first_four_elements)


def normalize_key(name, manufacturer):
    """ Normalize and create a composite key for quick comparison. """
    return f"{name.lower()}_{manufacturer.lower()}"


def create_lookup_table(materials):
    """Create a lookup table (dictionary) for quick access by name and manufacturer."""
    lookup_table = {}
    for material in materials:
        key = normalize_key(material['name'], material['manufacturer'])
        lookup_table[key] = material
    return lookup_table


def merge_materials(materials_file1, materials_file2):
    """
    Merge materials from materials2 into materials1 based on matching name and manufacturer.
    Transfer 'code' from materials2 to materials1 where matches occur.
    """
    materials1 = load_json(materials_file1)  # Ensure this loads a list of materials
    materials2 = load_json(materials_file2)  # Ensure this also loads a list of materials

    lookup_table = create_lookup_table(materials2)
    updated_materials = []

    for material in materials1:
        key = normalize_key(material['name'], material['manufacturer'])
        if key in lookup_table:
            material['code'] = lookup_table[key].get('code', '')  # Add 'code' from the second file
        updated_materials.append(material)

    save_json(updated_materials, 'merged_materials_output.json')

    return updated_materials


class DateTimeEncoder(json.JSONEncoder):
    """Custom encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format datetime object to string in ISO 8601 format
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def convert_iso_to_ddmmyyyy(iso_date):
    """Converts an ISO formatted date string to dd/mm/yyyy format. If input is already a datetime object, formats it directly."""
    # Check if input is a datetime object
    if isinstance(iso_date, datetime):
        # Directly format the datetime object to the desired string format
        return iso_date.strftime("%d/%m/%Y")
    # Check if input is a string that matches the expected ISO format
    elif isinstance(iso_date, str):
        iso_format_check = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        if re.match(iso_format_check, iso_date):
            try:
                # Convert the ISO formatted string to a datetime object
                date_object = datetime.fromisoformat(iso_date)
                return date_object.strftime("%d/%m/%Y")
            except ValueError:
                return "Invalid date format"
        else:
            # Return the original input if it does not match the ISO format
            return iso_date
    else:
        # Return the original input if it's not a datetime object or a string
        return ""