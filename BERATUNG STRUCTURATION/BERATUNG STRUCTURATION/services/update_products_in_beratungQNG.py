import requests
import json
import time

def update_materials_database(json_file_path):
    """
    Update the materials in the database by sending PATCH requests to the API.
    The updates are based on the contents of a JSON file.

    Parameters:
        json_file_path (str): Path to the JSON file containing materials and their new cost group data.
    """
    # Load the comparison results from the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            materials = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error parsing JSON from the file '{json_file_path}'.")
        return

    # Define the headers for the API request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'
    }

    # Process each material in the JSON file
    for material in materials:
        # Send the PATCH request to update the material
        update_material(material['code'], applicationArea=material['applicationArea'], quantity =material['quantity'],
                        useArea=material['useArea'], company=material['company'],
                        constructionNearSurface=material['constructionNearSurface'],
                        svhc=material['svhc'],
                        employeesConcerned=material['employeesConcerned'],verificationDocument=material['verificationDocument'])
        # Example usage
        #update_material_database(material['code'], manufacturerName="Remmers GmbH", costGroups2=["340", "350"], costGroups3=["342", "353"])
        #response = requests.patch(url, headers=headers, data=payload)


def update_material(material_code, **kwargs):
    """
    Update a material in the database by sending a PATCH request to the API.
    Allows updating multiple attributes of a material dynamically and implements retries for certain server errors.

    Parameters:
        material_code (str): The unique code for the material to update.
        **kwargs (dict): Key-value pairs of attributes to update.
    """
    url = f"https://api.beratung-qng.com/api/materials/{material_code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'
    }
    payload = json.dumps(kwargs)

    attempt = 0
    max_attempts = 5  # Maximum number of retry attempts

    while attempt < max_attempts:
        attempt += 1
        try:
            response = requests.patch(url, headers=headers, data=payload)

            if response.status_code == 200:
                print(f"✅ Successfully updated material {material_code}.")
                return True  # Success
            else:
                print(
                    f"❌ Attempt {attempt}: Failed to update {material_code} | Status: {response.status_code} | Response: {response.text}")
                if response.status_code in [429, 500, 502, 503, 504]:  # Retry for server errors
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    break  # Don't retry on other failures

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request error for {material_code}: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff

    return False  # Return False to indicate failure after all retries