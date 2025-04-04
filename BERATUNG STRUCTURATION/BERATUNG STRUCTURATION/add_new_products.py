from models.add_products_to_beratung import process_materials_to_db
from models.get_materials_db import get_api_response
from models.image_files_requests import update_files_image_requests_response
from models.update_image_only import process_and_update_image
from services.check_image import find_images_in_directory
from services.extract_excel_encoding_brandl import process_excel_to_json
from services.filtered_db_beratung import process_filtered_db_materials
from services.missing_materials_db_brandl import compare_materials
from services.write_image import match_materials_to_images
from services.write_schema import write_schema_products_json
from utils.utils import merge_materials


def add_new_products_to_database():
    """
    Processes new products from an Excel file, compares them with existing database entries,
    matches images and files, and finally updates the database.
    """

    # Step 1: Extract the Excel file from customer
    excel_file_path = '../Eingabehilfe.xlsx'
    print("▶️ Étape 1: lecture Excel")
    process_excel_to_json(excel_file_path)  # Assumes existence of this function

    # Step 2: Extract data from the database Beratung QNG
    print("▶️ Étape 2: appel API")
    get_api_response()  # Fetch and store response in JSON, assumes function definition
    # data_beratung.json"  Input JSON file, assuming get_api_response() creates it
    print("▶️ Étape 3: filtrage API")
    process_filtered_db_materials()  # Assumes it processes data stored from get_api_response()

    # Step 3: Compare materials and find missing ones
    print("▶️ Étape 4: comparaison")
    compare_materials("output_eingabehilfe.json", "filtered_materials.json")  # Assumes existence of this function

    # Step 4: Find images in the directory

    find_images_in_directory()  # Assumes function definition

    # Step 5: Add image and file paths to the missing materials
    print("▶️ Étape 5: image matching")
    match_materials_to_images("missing_materials.json", "missing_materials.json")  # Assumes function definition

    # Step 6: Write schema for products and update files and image requests
    write_schema_products_json("missing_materials.json")  # Assumes function definition
    update_files_image_requests_response("brandl_data_to_beratung.json", "brandl_data_to_beratungQNG.json")  # Assumes function definition

    # Step 7: Write data to db
    # process_materials_to_db("brandl_data_to_beratungQNG.json", "failed_requests.log")  # Assumes function definition

    #Step 8 : actualize image in database
    # File paths for the two JSON files
    # get_api_response()  # Fetch and store response in JSON, assumes function definition
    # process_filtered_db_materials()  # Assumes it processes data stored from get_api_response()

    # Perform comparison and merging
    # merge_materials("missing_materials.json","filtered_materials.json")
    #process the update
    # process_and_update_image("merged_materials_output.json")