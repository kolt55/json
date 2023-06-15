import os
import json
import tkinter as tk
from tkinter import filedialog

def split_json_file(input_file_path, output_directory, objects_per_file):
    # Open the input file for reading
    with open(input_file_path, 'r') as input_file:
        # Initialize variables
        output_file_index = 0
        objects_count = 0
        output_file_path = os.path.join(output_directory, f"output_{output_file_index + 1}.jsonl")
        output_file = open(output_file_path, 'w')

        # Read the file line by line
        for line in input_file:
            try:
                # Attempt to load the line as JSON
                data = json.loads(line)

                # Write the JSON object to the output file
                json.dump(data, output_file)
                output_file.write('\n')

                # Increment the count of objects
                objects_count += 1

                # Check if the maximum number of objects per file has been reached
                if objects_count == objects_per_file:
                    # Close the current output file
                    output_file.close()

                    # Increment the output file index
                    output_file_index += 1

                    # Create a new output file
                    output_file_path = os.path.join(output_directory, f"output_{output_file_index + 1}.jsonl")
                    output_file = open(output_file_path, 'w')

                    # Reset the objects count
                    objects_count = 0

            except json.JSONDecodeError:
                # Ignore invalid JSON objects
                continue

        # Close the last output file
        output_file.close()

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask for the input file
input_file_path = filedialog.askopenfilename(
    title="Select Input File",
    filetypes=(("JSON Lines Files", "*.jsonl"), ("All Files", "*.*"))
)

# Ask for the number of objects per output file
objects_per_file = tk.simpledialog.askinteger(
    title="Objects per Output File",
    prompt="Enter the number of objects per output file:"
)

# Ask for the output directory
output_directory = filedialog.askdirectory(title="Select Output Directory")

if input_file_path and objects_per_file and output_directory:
    # Call the function to split the JSON file
    split_json_file(input_file_path, output_directory, objects_per_file)
else:
    print("Input file, objects per file, or output directory not provided.")
