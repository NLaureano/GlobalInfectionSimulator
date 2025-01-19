import csv
import json

def merge_jsons(json1_file, json2_file, output_file):
    # Load JSON files
    with open(json1_file, 'r') as file1, open(json2_file, 'r') as file2:
        json1_data = json.load(file1)  # List of dictionaries with neighbors
        json2_data = json.load(file2)  # List of dictionaries with additional data

    # Convert the second JSON to a dictionary for faster lookups by "name"
    json2_dict = {item["name"]: item for item in json2_data}

    # Merge the data
    merged_data = []
    for item in json1_data:
        name = item["name"]
        if name in json2_dict:
            # Combine the dictionaries
            merged_item = {**item, **json2_dict[name]}
            merged_data.append(merged_item)
        else:
            # Add the item from the first JSON if no match is found
            merged_data.append(item)

    # Add entries from the second JSON that are not in the first JSON
    for name, item in json2_dict.items():
        if name not in {entry["name"] for entry in json1_data}:
            merged_data.append(item)

    # Write the merged data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)

    print(f"Merged data has been written to {output_file}")

# Example usage
json1_file = 'countries_with_neighbors.json'  # Replace with your first JSON file
json2_file = 'datasets/merged.json'  # Replace with your second JSON file
output_file = 'merged.json'  # Replace with your desired output file

merge_jsons(json1_file, json2_file, output_file)
