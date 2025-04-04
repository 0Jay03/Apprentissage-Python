import requests
import json

# API endpoint
url = "https://api.beratung-qng.com/api/materials"

# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'  # Replace with your actual authorization token
}

def get_api_response(save_to_file=True, filename="data_beratung.json"):
        """
        Sends a GET request to the specified API endpoint and returns the JSON response.

        Args:
            save_to_file (bool): Whether to save the response to a JSON file. Default is False.
            filename (str): The name of the file to save the response. Default is "data_beratung.json".

        Returns:
            dict: The JSON response from the API as a Python dictionary.
            None: If the request fails.
        """
        try:
            # Send GET request to the API
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Save the JSON response to a file if requested
                if save_to_file:
                    with open(filename, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                    print(f"API response saved to '{filename}'.")

                return data
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None