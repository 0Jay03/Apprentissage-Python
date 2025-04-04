import json
import requests
import os

from services.update_products_in_beratungQNG import update_material


def upload_file(file_path, upload_url):
    """Uploads a file to the API and returns the response filename."""
    if not file_path or not os.path.exists(file_path):
        return None  # Skip if the file does not exist

    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(upload_url, files=files)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            return response.text.strip().strip('"')
    return None

def process_and_update_image(input_json_path):
    """Processes product data from a JSON file, uploads images, updates product information, and saves the updated data."""

    upload_url = "https://api.beratung-qng.com/api/files/save"

    try:
        # Load the JSON data
        with open(input_json_path, "r", encoding='utf-8') as file:
            data = json.load(file)

        # Process each product in the JSON
        for product in data:
            if "picture" in product and product["picture"]:
                uploaded_filename = upload_file(product["picture"], upload_url)
                code = product.get("code")
                if uploaded_filename:
                    product["picture"] = uploaded_filename  # Update JSON with API response filename
                    # Assuming update_material and update_materials_database are available from import
                    update_material(code, picture=uploaded_filename)
                    # Example function call (commented out):
                    # update_materials_database(code, manufacturerName="Remmers GmbH", costGroups2=["340", "350"], costGroups3=["342", "353"])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

