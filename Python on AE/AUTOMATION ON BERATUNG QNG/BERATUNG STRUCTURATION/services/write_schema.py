import json
import logging

import pandas as pd

from utils.utils import extract_numeric_prefix_regex, clean_and_trim_string, handle_na, DateTimeEncoder, \
    convert_iso_to_ddmmyyyy


def write_schema_products_json(input_json_path):
    # Load the JSON data with UTF-8 encoding
    with open(input_json_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    # Load the main Excel file with pandas
    df = pd.read_excel('../PRODUKTLISTE.xlsx')

    # Prepare a list to store the results
    results = []

    # Process each product in the JSON file
    for product in products:
        name = str(product['name']).strip().lower()  # Normalize to lowercase and strip whitespace
        manufacturer = str(product.get('manufacturer', '')).strip().lower()

        # Search for the corresponding row in the main Excel using pandas
        found_row = df[df.iloc[:, 2].str.strip().str.lower() == name]

        if not found_row.empty:
            # Extract necessary information from the first matching row
            application_area = clean_and_trim_string(found_row.iloc[0, 3])
            application_field_position = found_row.iloc[0, 4]
            verification_document = handle_na(found_row.iloc[0, 6])
            company = handle_na(found_row.iloc[0, 10])
            qng_requirement = clean_and_trim_string(handle_na(found_row.iloc[0, 5]))
            formal_de_hyd = handle_na(found_row.iloc[0, 7])
            expiry_date = handle_na(found_row.iloc[0, 11])
            svhc = handle_na(found_row.iloc[0, 9])
            voc  = handle_na(found_row.iloc[0, 7])
            constructionNearSurface = handle_na(found_row.iloc[0, 14])
            # Extract concerned employees
            employees_concerned = list(found_row.columns[15:31][found_row.iloc[0, 15:31] == 'ja'])
            # Structure the data to be saved in the new JSON file

            output_data = {
                'applicationArea': application_area,
                'verificationDocument': verification_document,
                'manufacturerName': manufacturer,
                'name': product['name'],
                #'costGroups2': product['costGroups2'],
                #'costGroups3': product['costGroups3'],
                #'productLinks': [],
                'quantity': formal_de_hyd,   #Formaldehyd
                'useArea': qng_requirement,    #QNG-Anforderungen
                'company': company,
                #"particular": False,
                "constructionNearSurface": False if str(constructionNearSurface).lower() == 'ja' else True,
                "expiryDate": convert_iso_to_ddmmyyyy(expiry_date) if expiry_date!="abgelaufen" else "" ,
                "svhc": svhc,
                "voc": voc,
                #'picture': product['picture'],  # Placed immediately after 'company'
                #'files': product['files'],
                'employeesConcerned': [employee.strip() for employee in employees_concerned],
                #'compartmentsConcerned': [],
                #'applicationFieldPosition': extract_numeric_prefix_regex(application_field_position)
            }
            results.append(output_data)
        else:
            print(f"⚠️ Le nom '{name}' n'est pas trouvé dans PRODUKTLISTE.xlsx.")

    # Save the results in a new JSON file with UTF-8 encoding
    with open('brandl_data_to_beratung.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4, cls=DateTimeEncoder)

    print(f"✅ Successfully processed {len(results)} items and saved them in brandl_data_to_beratung.json")
