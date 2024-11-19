import json

def apply_padding(data_list):
    # Function to append "0000" before each JSON data
    padded_data_list = ["0000" + json.dumps(entry) for entry in data_list]
    return padded_data_list
 
def main():
    # Read data from the data1.json file
    input_file_path = r'C:\Users\abdul\Videos\python\data1.json'  # Replace with the actual path to your data.json file
    with open(input_file_path, 'r') as file:
        # Load each line as a JSON object
        data_list = [json.loads(line) for line in file]

    # Apply padding by appending "0000" before each JSON data
    modified_data_list = apply_padding(data_list)

    # Save the modified data back to a new file
    output_file_path = r'C:\Users\abdul\Videos\python\data1_padded.json'
    with open(output_file_path, 'w') as output_file:
        for entry in modified_data_list:
            output_file.write(entry + "\n")

    print(f"Padded data saved to: {output_file_path}")

if __name__ == "__main__":
    main()
