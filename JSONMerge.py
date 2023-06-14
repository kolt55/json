import os
import json

def merge_json_files(directory_path, output_file_path):
    # Get a list of all JSON files in the directory
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.jsonl')]

    # Open the output file in append mode
    with open(output_file_path, 'a') as output_file:
        # Iterate over each JSON file
        for file_name in json_files:
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as json_file:
                # Read the file content
                content = json_file.read().strip()
                # Split the content by newlines to get individual JSON objects
                json_objects = content.split('\n')
                # Iterate over each JSON object
                for json_obj in json_objects:
                    try:
                        # Load the JSON content
                        data = json.loads(json_obj)
                        # Write the content to the output file
                        json.dump(data, output_file)
                        output_file.write('\n')  # Add a new line after each JSON object
                    except json.JSONDecodeError:
                        # Skip invalid JSON objects
                        continue

# Provide the directory containing the JSON files
directory_path = "/Users/kbittner/Desktop/Skywalk Files/Annotator 1"


output_file_path = "/Users/kbittner/Desktop/Skywalk Files/Annotator 1/FullFile.jsonl"

# Call the function to merge the JSON files
merge_json_files(directory_path, output_file_path)
