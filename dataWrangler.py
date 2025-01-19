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

# Specify input and output file names
input_file = 'HDIData.txt'  # Replace with your input file name
output_file = 'hdi_data.json'  # Replace with your desired output file name

# Parse and convert the data to JSON
parse_hdi_data(input_file, output_file)

# Specify input and output file names
#input_file = 'populations.txt'  # Replace with your input file
#output_file = 'countries.json'  # Replace with your desired output file

# Parse and convert to JSON
#parse_and_convert_to_json(input_file, output_file)
