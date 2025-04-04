import json
import requests



def delete_materials(input_json_path, failed_deletions_path):
    """
    Deletes materials from an API based on the codes provided in a JSON file.

    Parameters:
        input_json_path (str): Path to JSON file containing material codes.
        failed_deletions_path (str): Path to output JSON file for logging failed deletions.
    """

    # Example usage of the function:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'
    }
    api_url_template = "https://api.beratung-qng.com/api/materials/{code}"


    # Load material codes from JSON file
    try:
        with open(input_json_path, 'r', encoding='utf-8') as file:
            materials = json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: File '{input_json_path}' not found.")
        exit()

    # List to track failed deletions
    failed_deletions = []

    # Loop through materials and delete them
    for material in materials:
        code = material.get("code", "").strip()

        if code:  # Ensure code is not empty
            url = api_url_template.format(code=code)
            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                print(f"✅ Successfully deleted material with code: {code}")
            else:
                print(f"❌ Failed to delete material with code: {code} | Status: {response.status_code} | Response: {response.text}")
                failed_deletions.append({"code": code, "status": response.status_code, "response": response.text})

    # Save failed deletions to a log file
    if failed_deletions:
        with open(failed_deletions_path, "w", encoding="utf-8") as json_file:
            json.dump(failed_deletions, json_file, ensure_ascii=False, indent=4)
        print(f"⚠️ {len(failed_deletions)} deletions failed. Check '{failed_deletions_path}' for details.")
    else:
        print("✅ All materials deleted successfully!")

