import requests
import json

# API URL Template
API_URL_TEMPLATE = "https://api.beratung-qng.com/api/materials/{code}"

# Headers for the API request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'
}


def update_material_files(material_code, files_dict):
    """
    Updates the files field of a material using a PATCH request.

    Args:
        material_code (str): The unique code of the material (e.g., "MAT-GFUP2N").
        files_dict (dict): Dictionary of files with keys as file types (e.g., "sdb") and values as filenames.

    Returns:
        dict: Response JSON if successful, otherwise error message.
    """
    # Filter out empty or missing files
    valid_files = {key: value for key, value in files_dict.items() if value and value.strip()}

    # Ensure at least one file is present
    if not valid_files:
        print(f"⚠️ No valid files found for material {material_code}. Skipping update.")
        return {"error": "No valid files to update."}

    url = API_URL_TEMPLATE.format(code=material_code)

    # Prepare the payload
    payload = json.dumps({
        "files": valid_files
    })

    # Send the request
    response = requests.patch(url, headers=HEADERS, data=payload)

    # Handle response
    if response.status_code == 200:
        print(f"✅ Files updated successfully for {material_code}.")
        return response.json()
    else:
        print(f"❌ Failed to update files for {material_code}. Status: {response.status_code}")
        print(f"Response: {response.text}")
        return {"error": response.text}