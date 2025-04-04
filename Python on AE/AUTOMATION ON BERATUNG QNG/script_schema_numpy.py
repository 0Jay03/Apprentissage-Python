import json
import pandas as pd


# Load the JSON data with UTF-8 encoding
with open('filtered_data.json', 'r', encoding='utf-8') as file:
    products = json.load(file)

# Load the main Excel file into a DataFrame
df_main = pd.read_excel('PRODUKTLISTE.xlsx')

# Load the additional Excel file for cost groups into a DataFrame
df_costs = pd.read_excel('Eingabehilfe.xlsx')



# Prepare a list to store the results
results = []

# Process each product in the JSON file
for product in products:
    name = str(product['name']).strip().lower()  # Normalize to lowercase and strip whitespace
    manufacturer = str(product.get('manufacturerName', '')).strip().lower()  # Corrected manufacturer key
    code = str(product.get("code", "")).strip()  # Use correct code from JSON

    # Search for the corresponding row in the main DataFrame
    found_row = df_main[df_main.iloc[:, 2].str.strip().str.lower() == name]
    application_field_position ="2.3.1" #str(df_main.iloc[:, 4]) if not df_main.empty else field_name
    # If a matching row is found
    if not found_row.empty:
        found_row = found_row.iloc[0]  # Get the first matching row
        field_name = str(found_row[4]).strip().lower() if not pd.isna(found_row[4]) else ""  # Fix for NoneType error

        # Search for the code for the application field position in the mapping DataFrame

        # Extract the company name
        company = found_row[10] if not pd.isna(found_row[10]) else "Unknown"

        # Structure the data to be saved in the new JSON file
        output_data = {
            'manufacturerName': manufacturer,
            'name': name,
            'company': company,
            'code': code,  # Corrected to take from JSON
            'applicationFieldPosition': application_field_position
        }

        results.append(output_data)
    else:
        print(f"⚠️ Le nom '{name}' n'est pas trouvé dans le fichier Excel principal.")

# Save the results in a new JSON file with UTF-8 encoding
with open('company_to_update.json', 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"✅ Successfully processed {len(results)} materials and saved them in 'company_to_update.json'")