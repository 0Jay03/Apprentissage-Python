import json
import re


def process_filtered_db_materials():
    # File paths
    input_json_path = "data_beratung.json"  # Input JSON file
    cleaned_json_path = "cleaned_input.json"  # Cleaned JSON file
    output_json_path = "filtered_materials.json"  # Output JSON file

    # Function to clean invalid control characters in JSON
    def clean_json_file(input_file, output_file):
        with open(input_file, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        # Remove problematic characters (null bytes, newlines, unexpected escape sequences)
        cleaned_content = re.sub(r"[\x00-\x1F\x7F]", " ", content)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cleaned_content)

        print(f"✅ Cleaned JSON saved as {output_file}")

    # Clean the input JSON before loading
    clean_json_file(input_json_path, cleaned_json_path)

    # Load the cleaned JSON file
    try:
        with open(cleaned_json_path, "r", encoding="utf-8") as file:
            materials = json.load(file)
    except json.JSONDecodeError as e:
        print(f"❌ JSONDecodeError: {e}")
        exit()

    # Filtered list
    filtered_materials = []

    # Process materials
    for material in materials:
        code = str(material.get("code", "")).strip()  # Ensure code is a string
        name = str(material.get("name", "")).strip()  # Ensure name is a string
        manufacturer = str(material.get("_manufacturer", {}).get("name", "")).strip()  # Ensure manufacturer exists
        picture = str(material.get("picture", "No image")).strip()  # Get picture or default value
        costGroups2 = material.get("costGroups2", [])  # Default to an empty list if the key doesn't exist
        costGroups3 = material.get("costGroups3", [])  # Default to an empty list if the key doesn't exist

        # Extract additional fields (applicationField)
        application_field_position = str(material.get("applicationField", {}).get("position", "")).strip()
        application_field_name = str(material.get("applicationField", {}).get("name", "")).strip()

        # Only add materials where "code" starts with "MAT"
        if code.startswith("MAT"):
            filtered_materials.append({
                "code": code,
                "name": name,
                "manufacturer": manufacturer,
                "picture": picture,
                "costGroup2": costGroups2,
                "costGroup3": costGroups3,
                "applicationField_position": application_field_position,
                "applicationField_name": application_field_name
            })

    # Save filtered data
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(filtered_materials, json_file, ensure_ascii=False, indent=4)

    # Summary
    print(f"✅ {len(filtered_materials)} materials extracted and saved to '{output_json_path}'.")
