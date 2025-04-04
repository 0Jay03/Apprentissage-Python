import json
import os
import glob
from rapidfuzz import process  # Fuzzy matching


def normalize_text(text):
    """Normalize text by converting to lowercase and replacing special characters."""
    if text:
        return text.lower().replace("ß", "ss").strip()
    return ""


def find_closest_match(target, folder_list, threshold=80):
    """Finds the best matching folder using fuzzy matching with normalization."""
    if not folder_list:
        return None

    target_normalized = normalize_text(target)
    folder_list_normalized = [normalize_text(f) for f in folder_list]

    result = process.extractOne(target_normalized, folder_list_normalized)

    if result:
        match, score, *_ = result  # Extract relevant values
        if score >= threshold:
            return folder_list[folder_list_normalized.index(match)]  # Return the original folder name

    return None  # Return None if no good match is found


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


def update_json_with_pictures_and_files(json_path, output_path, image_extensions):
    """Updates JSON file with the correct image paths and associated PDF files."""
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    updated_data = []  # Store updated entries

    for product in data:
        manufacturer = normalize_text(product.get('manufacturerName', ''))
        name = normalize_text(product.get('name', ''))
        application_field_position = product.get('applicationFieldPosition', '').split('.')

        # Construct the base path for file storage
        base_path = os.path.join('data_pic_pdf', application_field_position[0],
                                 '.'.join(application_field_position[:2]))

        # Step 1: Match manufacturer first
        available_folders = [f for f in os.listdir(base_path) if
                             os.path.isdir(os.path.join(base_path, f))] if os.path.exists(base_path) else []
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

        # Find the image (already implemented)
        picture_path = ""
        if final_directory_path:
            for ext in image_extensions:
                image_file = glob.glob(os.path.join(final_directory_path, f"*.{ext}"))
                if image_file:
                    picture_path = image_file[0]
                    break

        # Find the required files in the directory and dynamically replace missing ones
        files_path = {}
        if final_directory_path:
            predefined_patterns = {
                "sdb": "sbd.pdf",
                "tm": "tm.pdf",
                "pdb": "pdb.pdf",
                "epd": "epd.pdf",
                "ndb": "ndb.pdf",
                "qnd": "qnd.pdf",
                "ec1": "ec1.pdf",
                "tdb": "tdb.pdf"
            }
            files_path = find_existing_files(final_directory_path, predefined_patterns)

        # Ensure "picture" is positioned immediately after "company" and add "files"
        updated_product = {
            'applicationArea': product.get('applicationArea', ''),
            'verificationDocument': product.get('verificationDocument', ''),
            'manufacturerName': manufacturer,
            'name': name,
            'costGroups2': product.get('costGroups2', []),
            'costGroups3': product.get('costGroups3', []),
            'productLinks': product.get('productLinks', []),
            'quantity': product.get('quantity', "Nicht spezifiziert"),
            'useArea': product.get('useArea', "Nicht spezifiziert"),
            'company': product.get('company', ''),
            'picture': picture_path,  # Placed immediately after 'company'
            'files': files_path if files_path else []  # If no files exist, set to []
        }

        # Add remaining fields
        updated_product.update({
            'employeesConcerned': product.get('employeesConcerned', []),
            'compartmentsConcerned': product.get('compartmentsConcerned', []),
            'applicationFieldPosition': product.get('applicationFieldPosition', ''),
        })

        updated_data.append(updated_product)

    # Save the updated JSON file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(updated_data, outfile, ensure_ascii=False, indent=4)


# **Image extensions to consider**
image_extensions = ['jpeg', 'png', 'svg', 'jpg', 'html', 'htm', 'webp', 'bmp', 'gif', 'tiff', 'ico', 'dds', 'heic']

# **Paths for input and output JSON files**
input_json_path = 'data_to_add2.json'#'data_to_add.json'
output_json_path = 'final_data_to_br.json'

# **Run the function**
update_json_with_pictures_and_files(input_json_path, output_json_path, image_extensions)
