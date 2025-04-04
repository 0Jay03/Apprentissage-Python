import json
import requests
import os

# API Endpoint
UPLOAD_URL = "https://api.beratung-qng.com/api/files/save"

def upload_file(file_path):
    """Uploads a file to the API and returns the response filename."""
    if not file_path or not os.path.exists(file_path):
        return None  # Skip if the file does not exist

    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(UPLOAD_URL, files=files)  # No headers needed
        response.encoding = 'utf-8'  # Force UTF-8 encoding

        if response.status_code == 200:
            return response.text.strip().strip('"')  # Extract and clean filename
    return None  # Return None if upload fails

def update_files_image_requests_response(input_json_path, output_json_path):
    """Reads products from a JSON file, uploads pictures and files, and writes back to a new JSON file."""
    # Read the JSON file
    with open(input_json_path, "r", encoding='utf-8') as file:
        data = json.load(file)

    # Process each product in the JSON
    for product in data:
        # Upload picture and update JSON
        if "picture" in product:
            if product["picture"]:  # Check if there's a non-empty picture link
                uploaded_filename = upload_file(product.get("picture"))
                if uploaded_filename:
                    product["picture"] = uploaded_filename  # Update JSON with API response filename
            else:
                product["picture"] = ""  # Directly set the picture attribute to an empty string if it's empty

        # Upload each file in "files"
        if "files" in product and isinstance(product["files"], dict):
            updated_files = {}  # Store uploaded file names
            for key, file_path in product["files"].items():
                if file_path:  # Ensure the file path is not empty
                    uploaded_filename = upload_file(file_path)
                    if uploaded_filename:
                        updated_files[key] = uploaded_filename  # Store uploaded file name

            # Update the product with uploaded files, or set to an empty dictionary if no files were uploaded
            if updated_files:
                product["files"] = updated_files
            else:
                product["files"] = {}

    # Save the updated JSON file
    with open(output_json_path, "w", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
