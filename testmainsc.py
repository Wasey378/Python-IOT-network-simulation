import socket
import json
import numpy as np

# Function to calculate z-score for a given value and mean/std deviation
def calculate_z_score(value, mean, std_dev):
    if std_dev == 0:
        return 0  # Avoid division by zero
    return (value - mean) / std_dev

# Function to detect anomalies using z-score
def detect_anomalies(sensor_data, mean_values, std_dev_values, threshold=3):
    anomalies = []
    for key, value in sensor_data.items():
        if key in mean_values:
            mean = mean_values[key]
            std_dev = std_dev_values[key]
            z_score = calculate_z_score(value, mean, std_dev)
            if abs(z_score) > threshold:
                anomalies.append((key, value, z_score))
    return anomalies

# Function to calculate mean and standard deviation for each sensor attribute
def calculate_statistics(data):
    attribute_values = {key: [] for key in data[0]["weatherObservation"]}
    for item in data:
        observation = item["weatherObservation"]
        for key, value in observation.items():
            attribute_values[key].append(value)
    
    mean_values = {key: np.mean(values) for key, values in attribute_values.items()}
    std_dev_values = {key: np.std(values) for key, values in attribute_values.items()}
    return mean_values, std_dev_values

# Function to handle incoming sensor data
def handle_sensor_data(client_socket, mean_values, std_dev_values):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Decode and process the received data
            sensor_data = json.loads(data.decode('utf-8'))
            print("Received sensor data:", sensor_data)

            # Detect anomalies
            anomalies = detect_anomalies(sensor_data["weatherObservation"], mean_values, std_dev_values)
            if anomalies:
                print("Anomalies detected:")
                for anomaly in anomalies:
                    print(anomaly)
                response = "Anomalies detected!"
            else:
                response = "No anomalies detected"

            # Send response back to the client
            client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            break

# Main function
def main():
    # Load sensor data from a file or API
    # For demonstration, let's assume sensor data is provided in a list named 'sensor_data'
    sensor_data = [
        {"weatherObservation": {"temperature": 20, "humidity": 40, "windSpeed": 10}},
        {"weatherObservation": {"temperature": 25, "humidity": 45, "windSpeed": 12}},
        {"weatherObservation": {"temperature": 30, "humidity": 50, "windSpeed": 15}}
    ]

    # Calculate mean and standard deviation for sensor attributes
    mean_values, std_dev_values = calculate_statistics(sensor_data)

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address
    server_address = ('localhost', 12345)  # Change to your desired server address and port

    try:
        # Bind the socket to the server address
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen(5)

        print("Server is listening for incoming connections...")

        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Handle incoming sensor data
            handle_sensor_data(client_socket, mean_values, std_dev_values)

            # Close the client socket
            client_socket.close()

    except Exception as e:
        print("Error:", e)
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
