import json



from utils.utils import fuzzy_match, find_existing_files, load_json, filter_pdf_folders


def match_materials_to_images(materials_data_path, output_json_path):
    """Matches materials to images based on fuzzy matching of material and manufacturer names."""
    # Load data

    materials_data = load_json(materials_data_path)

    # Define predefined file patterns outside the loop
    predefined_patterns = {
        "sdb": "sdb.pdf",
        "tm" : "tm.pdf",
        "pdb": "pdb.pdf",
        "epd": "epd.pdf",
        "ndb": "ndb.pdf",
        "qnd": "qnd.pdf",
        "ec1": "ec1.pdf",
        "tdb": "tdb.pdf",
        "qng": "qng.pdf",
        "upd": "upd.pdf"
    }

    # Process and match data
    matched_materials = []
    for material in materials_data:
        material_name = material.get("name", "").strip().lower()
        manufacturer_name = material.get("manufacturer", "").strip().lower()

        best_match = filter_pdf_folders("log_found_images.json",'image_folder', manufacturer_name, material_name)
        if best_match:
            material["picture"] = best_match['image_pfad'][0]
            files_path = find_existing_files(best_match['image_folder'], predefined_patterns)
            material["files"] = files_path
        else:
            material["picture"] = ""
            best_match_pdf = filter_pdf_folders("log_found_pdf.json", 'pdf_folder', manufacturer_name, material_name)
            if best_match_pdf:
               files_path = find_existing_files(best_match_pdf["pdf_folder"], predefined_patterns)
               material["files"] = files_path

        matched_materials.append(material)

    # Save the matched data to a new JSON file
    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(matched_materials, outfile, ensure_ascii=False, indent=4)

    print(f"✅ Matching complete. Output saved to {output_json_path}")

