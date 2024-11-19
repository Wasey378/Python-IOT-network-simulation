import socket
import json
import hashlib

def calculate_hash(sensor_data):
    sorted_keys = sorted(sensor_data["weatherObservation"].keys())
    serialized_keys = json.dumps(sorted_keys, separators=(',', ':'))
    return hashlib.sha256(serialized_keys.encode()).hexdigest()

def is_malicious(sensor_data):
    Originalkeys = '["ICAO","clouds","cloudsCode","countryCode","datetime","dewPoint","elevation","hectoPascAltimeter","humidity","lat","lng","observation","stationName","temperature","weatherCondition","windSpeed"]'
    hash_value = calculate_hash(sensor_data)
    known_good_hash = hashlib.sha256(Originalkeys.encode()).hexdigest()
    if hash_value != known_good_hash:
        return True
    return False

# Function to handle incoming sensor data
# Function to handle incoming sensor data
def handle_sensor_data(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Decode and process the received data
            sensor_data = json.loads(data.decode('utf-8'))
            # Here you can implement your logic to process the sensor data
            # For now, let's just print the received data
            print("Received sensor data:", sensor_data)

            # Check if the packet is malicious
            if is_malicious(sensor_data):
                response = "Hash is not same , Data integrity is compromised , Malicious packet detected!"
                client_socket.sendall(response.encode('utf-8'))
                # Implement action to handle malicious packet, e.g., logging, blocking, etc.
            else:
                # Send acknowledgment back to the client
                response = "Data received successfully"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            break
# Function to handle incoming sensor data
def handle_sensor_data(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Decode and process the received data
            sensor_data = json.loads(data.decode('utf-8'))
            # Here you can implement your logic to process the sensor data
            # For now, let's just print the received data
            print("Received sensor data:", sensor_data)

            # Check if the packet is malicious
            if is_malicious(sensor_data):
                print("Malicious packet detected!")
                response = "Malicious packet detected!"
                client_socket.sendall(response.encode('utf-8'))
                # Implement action to handle malicious packet, e.g., logging, blocking, etc.
            else:
                # Send acknowledgment back to the client
                response = "Data received successfully"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            break


# Main function
def main():
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
            handle_sensor_data(client_socket)

            # Close the client socket
            client_socket.close()

    except Exception as e:
        print("Error:", e)
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
