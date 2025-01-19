import csv
import json

def parse_and_convert_to_json(input_file, output_file):
    parsed_data = []

    # Open the input file and use csv.reader to parse
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            # Extract fields from the row
            name = row[0].strip('"')
            alternate_name = row[1].strip('"')
            print(row[2])
            population = int(row[2].replace(',', ''))

            # Create a dictionary for the line
            country_data = {
                "name": name,
                "alternate_name": alternate_name,
                "population": population,
            }

            # Append to the list of parsed data
            parsed_data.append(country_data)

    # Write parsed data to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(parsed_data, outfile, indent=4)

def parse_hdi_data(input_file, output_file):
    parsed_data = []

    # Open the input file and parse each line
    with open(input_file, 'r') as infile:
        for line in infile:
            # Split the line into country name and HDI value
            parts = line.rsplit('\t', 1)
            print(parts)
            if len(parts) == 2:
                country = parts[0].strip()
                hdi = float(parts[1].strip())
                
                # Add the data to the list as a dictionary
                parsed_data.append({
                    "name": country,
                    "hdi": hdi
                })

    # Write parsed data to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(parsed_data, outfile, indent=4)

import json

def merge_json_files(file1, file2, output_file):
    # Load the data from the JSON files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    # Create a dictionary to store the merged data by "name"
    merged_data = {}

    # Add data from the first file
    for item in data1:
        name = item["name"]
        merged_data[name] = item

    # Merge data from the second file
    for item in data2:
        name = item["name"]
        if name in merged_data:
            # Merge the dictionaries
            merged_data[name].update(item)
        else:
            # Add new entries
            merged_data[name] = item

    # Convert the merged data back into a list
    merged_list = list(merged_data.values())

    # Write the merged data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(merged_list, outfile, indent=4)

    print(f"Merged data has been written to {output_file}")

def extract_names_to_txt(json_file, output_txt_file):
    # Open and load the JSON file
    with open(json_file, 'r') as infile:
        data = json.load(infile)

    # Extract names from the JSON
    names = [item["name"] for item in data if "name" in item]

    names.sort()
    # Write names to the output text file
    with open(output_txt_file, 'w') as outfile:
        for name in names:
            outfile.write(name + '\n')

    print(f"Extracted {len(names)} names and written to {output_txt_file}")

# Example usage
input_json_file = 'datasets/totalData.json'  # Replace with your input JSON file
output_txt_file = 'names.txt'  # Replace with your desired output TXT file
extract_names_to_txt(input_json_file, output_txt_file)

# Specify input and output file names
#input_file1 = 'datasets/hdi_data.json'  # Replace with your input file name
#input_file2 = 'datasets/countries.json'  # Replace with your input file
#output_file = 'totalData.json'  # Replace with your desired output file name

#merge_json_files(input_file1, input_file2, output_file)

# Parse and convert the data to JSON
#parse_hdi_data(input_file, output_file)

# Specify input and output file names
#input_file = 'populations.txt'  # Replace with your input file
#output_file = 'countries.json'  # Replace with your desired output file

# Parse and convert to JSON
#parse_and_convert_to_json(input_file, output_file)
