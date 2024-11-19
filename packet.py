#packet size for every object

import json
def print_packet_sizes(json_file):
    with open(json_file, 'r') as file:
        # Read each line in the file and load JSON separately
        data_list = [json.loads(line) for line in file]

        # Print packet size for each object
        for i, entry in enumerate(data_list):
            packet_size = len(json.dumps(entry).encode('utf-8'))
            print(f"Packet {i + 1} size: {packet_size} bytes")

json_file = f'data1_padded.json'
print_packet_sizes(json_file)