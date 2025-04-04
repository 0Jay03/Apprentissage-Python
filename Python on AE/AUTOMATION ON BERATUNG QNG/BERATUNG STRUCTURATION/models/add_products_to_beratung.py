import json
import requests

from services.update_products_in_beratungQNG import update_material

# API Endpoint
API_URL = "https://api.beratung-qng.com/api/materials/automate"


# Function to capitalize every word in a string
def capitalize_words(text):
    if isinstance(text, str) and text.strip():
        return text.title()  # Capitalize every word
    return text  # Return original value if it's not a string


def process_materials_to_db(json_file_path, log_file_path):
    """
    Processes and sends each material entry from a JSON file to an API endpoint,
    and logs any failed requests to a log file.

    Parameters:
        json_file_path (str): Path to the JSON file containing material data.
        log_file_path (str): Path to the log file where failed requests will be recorded.
    """
    # Read the JSON file
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    failed_requests = []  # Prepare a list to store failed requests

    # Process each material entry in the JSON
    for index, material in enumerate(data, start=1):
        material["name"] = capitalize_words(material.get("name", ""))
        material["applicationArea"] = capitalize_words(material.get("applicationArea", ""))
        material["manufacturerName"] = capitalize_words(material.get("manufacturerName", ""))

        code = material.get("code")
        if not code:
            print(f"⚠️ Matériau sans 'code', ignoré : {material}")
            continue

        print(f"📤 Sending data {index}/{len(data)}: {material['name']}")

        try:
            response = requests.post(API_URL, json=material)

            if response.status_code in (200, 201):
                print(f"✅ Successfully sent: {material['name']}")
                if material.get("picture"):
                    update_material(code, picture=material["picture"])
            else:
                print(f"❌ Error sending {material['name']}: {response.status_code} - {response.text}")
                failed_requests.append(
                    {"name": material["name"], "status": response.status_code, "response": response.text})


        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request failed for {material['name']}: {str(e)}")
            failed_requests.append({"name": material["name"], "error": str(e)})

    # Save failed requests to a log file
    if failed_requests:
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            json.dump(failed_requests, log_file, ensure_ascii=False, indent=4)
        print(f"⚠️ Some requests failed. See details in {log_file_path}")

    print("🚀 All data has been processed!")
