import requests
import time
import json
import logging
from logging.handlers import SysLogHandler

# Initialize the logger
logger = logging.getLogger()
logger.addHandler(SysLogHandler(address=("192.168.0.103", 514)))
logger.setLevel(logging.INFO)

# Replace 'YOUR_USERNAME' with your Geonames username (API key)
username = 'mohtashim'
geonames_base_url = 'http://api.geonames.org/'

# Function to get country information using Geonames API
def get_country_info(location):
    endpoint = 'weatherIcaoJSON'
    params = {
        'ICAO': location,
        'username': username
    }

    response = requests.get(geonames_base_url + endpoint, params=params)
    data = response.json()

    return data

# Function to generate and process data without threading using Geonames API
def generate_and_process_data():
    data_repository = []

    for i in range(100):  # Loop 1000 times
        # Geonames API data generation logic
        location = 'LSZH'  # Replace with your desired location
        country_info = get_country_info(location)
        
        if country_info:
            # Check if country_info is not None before attempting to assign the "id"
            country_info["id"] = i
            data_repository.append(country_info)
        else:
            print(f"{i}: failed")
        
        # Sleep to control the data speed
        time.sleep(0.1)
    
    save_data_to_file(data_repository, f"data1.json")

# Function to save data to a JSON file
def save_data_to_file(data, file_path):
    with open(file_path, 'w') as file:  # Using 'w' mode to overwrite existing data
        json.dump(data, file)

# Generate and process data without threading
generate_and_process_data()
