import json
import os
import glob
from rapidfuzz import process, fuzz

from utils.params import IMAGE_EXTENSIONS, IMAGE_EXTENSIONS_PDF
from utils.utils import save_json, load_json, fuzzy_match

# Main Functions
def find_images_in_directory():
    """
    Traverse a directory to find all images and save the results to JSON and TXT files.
    """
    base_directory = "../data_pic_pdf"  # Replace with your actual path
    log_json_path_img = "log_found_images.json"
    log_json_path_pdf = "log_found_pdf.json"
    folders_with_images = []
    folders_with_pdf = []
    image_count = 0
    pdf_count = 0

    # Recursively traverse all subdirectories
    for root, _, files in os.walk(base_directory):
        found_images = []

        # Search for image files in this folder
        for ext in IMAGE_EXTENSIONS:
            images = glob.glob(os.path.join(root, f"*.{ext}"))  # Find all images with current extension
            if images:
                found_images.extend(images)  # Add to found images list

        # If images are found, add to log
        if found_images:
            image_count += len(found_images)

            # Store full paths of images
            image_pfad_list = [os.path.join(root, os.path.basename(image)) for image in found_images]

            folders_with_images.append({
                "image_folder": root,
                "image_pfad": image_pfad_list,  # Store full paths of images
                "image_count": len(found_images)
            })

    # Save log to JSON
    save_json(folders_with_images, log_json_path_img)


    for root, _, files in os.walk(base_directory):
        found_pdf = []

        # Search for image files in this folder
        for ext in IMAGE_EXTENSIONS_PDF:
            images = glob.glob(os.path.join(root, f"*.{ext}"))  # Find all images with current extension
            if images:
                found_pdf.extend(images)  # Add to found images list

        # If images are found, add to log
        if found_pdf:
            pdf_count += len(found_pdf)

            # Store full paths of images
            pdf_pfad_list = [os.path.join(root, os.path.basename(image)) for image in found_pdf]

            folders_with_pdf.append({
                "pdf_folder": root,
                "pdf_pfad": pdf_pfad_list,  # Store full paths of images
                "pdf_count": len(found_pdf)
            })

    # Save log to JSON
    save_json(folders_with_pdf, log_json_path_pdf)
    '''
        # Save log to TXT
        with open(log_txt_path, "w", encoding="utf-8") as txt_file:
            for folder in folders_with_images:
                txt_file.write(f"{folder['image_folder']} ({folder['image_count']} images)\n")
                for image_path in folder["image_pfad"]:
                    txt_file.write(f"   - {image_path}\n")
    '''
    print(f"✅ Total images found: {image_count}")
    print(f"✅ Total pdf found: {pdf_count}")
    print(f"📜 Log JSON saved at: {log_json_path_img}")
    print(f"📜 Log JSON saved at: {log_json_path_pdf}")

    return None  # Return the path to the JSON file for the next function



