import json

def process_and_compare_materials(file1_path, file2_path, output_file_path):
    """
    Load, compare two JSON files based on specific attributes (name, manufacturer, cost groups),
    and output the results and discrepancies to another JSON file, ensuring cost group entries are trimmed.

    Parameters:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_file_path (str): Path where the comparison result JSON will be written.
    """
    try:
        # Load JSON data from both files
        with open(file1_path, 'r', encoding='utf-8') as file:
            file1_data = json.load(file)
        with open(file2_path, 'r', encoding='utf-8') as file:
            file2_data = json.load(file)

        # List to store results of comparison
        results = []

        # Compare the data based on 'name' and 'manufacturer', then check 'cost groups'
        for item1 in file1_data:
            for item2 in file2_data:
                if item1['name'] == item2['name'] and item1['manufacturer'] == item2['manufacturer']:
                    # Trim spaces and compare cost groups
                    cost_group2_match = sorted([cg.strip() for cg in item1.get('costGroup2', [])]) == sorted([cg.strip() for cg in item2.get('costGroups2', [])])
                    cost_group3_match = sorted([cg.strip() for cg in item1.get('costGroup3', [])]) == sorted([cg.strip() for cg in item2.get('costGroups3', [])])

                    # Prepare result entry
                    result_entry = {
                        'code': item1.get('code'),
                        'name': item1['name'],
                        'manufacturer': item1['manufacturer'],
                        'costGroup2': item1.get('costGroup2', []),
                        'costGroups2': item2.get('costGroups2', []),
                        'costGroup2_match': cost_group2_match,
                        'costGroup3': item1.get('costGroup3', []),
                        'costGroups3': item2.get('costGroups3', []),
                        'costGroup3_match': cost_group3_match
                    }

                    # Append result if there's a full match or partial mismatch to report differences
                    if not cost_group2_match or not cost_group3_match:
                        results.append(result_entry)

        # Write the comparison results to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=4)

        print("Comparison complete. Results written to:", output_file_path)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


