import socket
import json
import time
import threading
import matplotlib.pyplot as plt
import requests

#client code



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

def send_data(location):
    country_info = get_country_info(location)
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the server address
    server_address = ('localhost', 12345)  # Change to your server address and port
    # Connect to the server
    client_socket.connect(server_address)
    client_socket.sendall(json.dumps(country_info).encode('utf-8'))
    response = client_socket.recv(1024)
    print("Received:", response.decode('utf-8'))
    client_socket.close()    
       
# Function to send sensor data and receive response
def send_sensor_data(location, node_count, result_list):
    try:
        threads = []
        start_time = time.time()
        for _ in range(node_count):  # corrected line here
            thread = threading.Thread(target=send_data, args=(location,))  # corrected line here
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        end_time = time.time()
        # Close the connection
        
        result_list.append(end_time - start_time)
    except Exception as e:
        print("Error:", e)


# Function to handle multithreading for different node counts
def handle_multithreading(node_counts, location):
    result_list = []
    for count in node_counts:
        send_sensor_data(location, count, result_list)
    return result_list

# Main function
def main():
    #  number of nodes
    node_counts = [10,20,40,60,80,100]
    location = 'LSZH'  # Replace with  desired location

    print("Sending sensor data with multithreading ")
    time_taken = handle_multithreading(node_counts, location)

    # Plot the graph
    plt.plot(node_counts, time_taken, marker='o')
    plt.title('Time taken for different numbers of nodes')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time taken (seconds)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
