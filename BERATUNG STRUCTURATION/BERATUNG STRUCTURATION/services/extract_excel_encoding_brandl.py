import pandas as pd
import json

from utils.utils import clean_and_trim_string


def process_excel_to_json(excel_file_path, output_json_path='output_eingabehilfe.json'):
    """
    Process an Excel file to extract specific data and save it as a JSON file.

    Args:
        excel_file_path (str): Path to the input Excel file.
        output_json_path (str): Path to the output JSON file. Default is 'output_eingabehilfe.json'.

    Returns:
        str: Path to the generated JSON file.
    """
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    # Function to convert space-separated strings to lists
    def convert_to_list(cell_value):
        return str(cell_value).split()

        # Function to trim string to a maximum length

        # Function to clean and trim string to a maximum length
        # Function to clean, remove spaces around slashes, and trim string to a maximum length


    # Filter rows starting from row 20 (index 19 in zero-based indexing)
    df_filtered = df.iloc[18:]

    # Rename columns to match desired names
    df_filtered = df_filtered.rename(columns={
        df.columns[5]: 'name',          # Rename "Produktname" to "name"
        df.columns[6]: 'manufacturer',  # Rename "Herstellername" to "manufacturer"
        df.columns[0]: 'costGroups2',   # Rename column 0 to "costGroups2"
        df.columns[1]: 'costGroups3'    # Rename column 1 to "costGroups3"
    })

    # Drop rows where 'name' is None
    df_filtered = df_filtered.dropna(subset=['name'])

    # Trim name and manufacturer fields
    df_filtered['name'] = df_filtered['name'].apply(clean_and_trim_string)
    df_filtered['manufacturer'] = df_filtered['manufacturer'].apply(clean_and_trim_string)

    # Convert costGroups2 and costGroups3 to lists
    df_filtered['costGroups2'] = df_filtered['costGroups2'].apply(convert_to_list)
    df_filtered['costGroups3'] = df_filtered['costGroups3'].apply(convert_to_list)

    # Select only the required columns
    df_filtered = df_filtered[['name', 'manufacturer', 'costGroups2', 'costGroups3']]

    # Convert the DataFrame to a list of dictionaries
    filtered_data = df_filtered.to_dict('records')

    # Write the filtered data to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    print(f"Le fichier JSON a été créé avec succès : {output_json_path}")
    return output_json_path