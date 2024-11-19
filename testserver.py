import socket
import json
import hashlib
import numpy as np
import logging
from logging.handlers import SysLogHandler



#server code

# Initialize the logger
logger = logging.getLogger()
logger.addHandler(SysLogHandler(address=("192.168.0.103", 514)))
logger.setLevel(logging.INFO)

# function to calculate the hash of sensor data
def calculate_hash(sensor_data):
    sorted_keys = sorted(sensor_data["weatherObservation"].keys())
    serialized_keys = json.dumps(sorted_keys, separators=(',', ':'))
    print("serielzed keys", serialized_keys)
    my_hash= hashlib.sha256(serialized_keys.encode()).hexdigest()
    
    
    print("my hash", my_hash)
    return my_hash
# function to check if the received sensor data is malicious
# wind direction is sometimes added in the API , sometimes not, 
def CheckDataIntegrity(sensor_data):
    Originalkeys = '["ICAO","clouds","cloudsCode","countryCode","datetime","dewPoint","elevation","hectoPascAltimeter","humidity","lat","lng","observation","stationName","temperature","weatherCondition","windDirection","windSpeed"]'
    Originalkeys2 = '["ICAO","clouds","cloudsCode","countryCode","datetime","dewPoint","elevation","hectoPascAltimeter","humidity","lat","lng","observation","stationName","temperature","weatherCondition","windSpeed"]'
    hash_value = calculate_hash(sensor_data)
    known_hash = hashlib.sha256(Originalkeys.encode()).hexdigest()
    known_hash2 = hashlib.sha256(Originalkeys2.encode()).hexdigest()
    print("hash1",known_hash)
    print("hash2",known_hash2)
    if (hash_value == known_hash) or (hash_value ==known_hash2):
        return False
    return True

# Define the function to handle incoming sensor data and detect anomalies
def handle_sensor_data(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Decode and process the received data
            sensor_data = json.loads(data.decode('utf-8'))
            print("Received sensor data:", sensor_data)

            # Check if the packet is malicious
            if CheckDataIntegrity(sensor_data):
                response = "Hash is not same , Data integrity is compromised , Malicious packet detected!"
            else:
                # Check for anomalies
                anomalies = detect_anomalies(sensor_data)
                if anomalies:
                    response = "Anomalies detected"
                else:
                    response = "Data received successfully"
                # Send acknowledgment back to the client
            client_socket.sendall(response.encode('utf-8'))
            #send alert to WAZUH
            logging.info(response)
        except Exception as e:
            print("Error:", e)
            break
def detect_anomalies(sensor_data):
    anomalies = []

    # Define mean values and standard deviations for each field for each location
    mean_values = {
        "LSZH": {
            "elevation": 500,
            "lng": 9.0,
            "dewPoint": 8,
            "temperature": 15,
            "humidity": 60,
            "hectoPascAltimeter": 1013,
            "windSpeed": 5
        },
        # Add more locations here
    }

    std_devs = {
        "LSZH": {
            "elevation": 50,
            "lng": 1.0,
            "dewPoint": 5,
            "temperature": 10,
            "humidity": 20,
            "hectoPascAltimeter": 5,
            "windSpeed": 3
        },
        # Add more locations here
    }

    # Iterate over numeric fields in the sensor data
    numeric_fields = ["elevation", "lng", "dewPoint", "temperature", "humidity", "hectoPascAltimeter", "windSpeed"]
    location = sensor_data["weatherObservation"]["ICAO"]
    if location in mean_values and location in std_devs:
        for field in numeric_fields:
            if field in sensor_data["weatherObservation"]:
                value = sensor_data["weatherObservation"][field]
                if isinstance(value, (int, float)):
                    # Calculate the threshold for anomaly detection
                    mean = mean_values[location][field]
                    std_dev = std_devs[location][field]
                    threshold = mean + 3 * std_dev
                    # Check if the value exceeds the threshold
                    if value > threshold or value < (mean - 3 * std_dev):
                        anomalies.append((field, value))
    
    return anomalies

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 12345)  # Change to your desired server address and port

    try:
        server_socket.bind(server_address)

        server_socket.listen(5)

        print("Server is listening for incoming connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            handle_sensor_data(client_socket)

            client_socket.close()

    except Exception as e:
        print("Error:", e)
    finally:
        server_socket.close()

# Execute the main function
if __name__ == "__main__":
    main()
