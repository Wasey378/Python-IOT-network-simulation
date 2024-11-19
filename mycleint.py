import socket
import json
import time
import matplotlib.pyplot as plt

# Define the sensor data
sensor_data = [{"weatherObservation": {"elevation": 432, "lng": 8.533333333333333, "observation": "LSZH 271720Z 14011KT CAVOK 18/M01 Q1007 NOSIG", "ICAO": "LSZH", "clouds": "clouds and visibility OK", "dewPoint": "-1", "cloudsCode": "CAVOK", "datetime": "2024-04-27 17:20:00", "countryCode": "CH", "temperature": "18", "humidity": 27, "stationName": "Zurich-Kloten", "weatherCondition": "n/a", "windDirection": 140, "hectoPascAltimeter": 1007, "windSpeed": "11", "lat": 47.483333333333334}, "id": 133}]

# Function to send sensor data and receive response
def send_sensor_data(node_count):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address
    server_address = ('localhost', 12345)  # Change to your server address and port

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send sensor data
        start_time = time.time()
        for _ in range(node_count):
            for data in sensor_data:
                client_socket.sendall(json.dumps(data).encode('utf-8'))
                response = client_socket.recv(1024)
                print("Received:", response.decode('utf-8'))
                

        # Close the connection
        client_socket.close()

        # Calculate and return the time taken
        return time.time() - start_time
    except Exception as e:
        print("Error:", e)

# Main function
def main():
    # Define the number of nodes
    node_counts = [10, 20, 40, 60, 80, 100]

    # Lists to store time taken for each count
    time_taken = []

    # Loop through different node counts
    for count in node_counts:
        print(f"Sending data for {count} nodes...")
        # Send sensor data and get time taken
        time_taken.append(send_sensor_data(count))

    # Plot the graph
    plt.plot(node_counts, time_taken, marker='o')
    plt.title('Time taken for different numbers of nodes')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time taken (seconds)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
