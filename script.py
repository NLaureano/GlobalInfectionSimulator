import os
import json
import google.generativeai as genai
import time
from random import uniform

# Configure with your API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable with your API key from https://makersuite.google.com/app/apikey")

# Configure the library
genai.configure(api_key=GOOGLE_API_KEY)

def read_cities_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_neighbors_for_city(model, city_name, max_retries=3):
    prompt = f"""Given the country {city_name}, list 3-5 neighboring countries that directly share a border with {city_name}.
    Only include countries that share a land or maritime border.
    
    Format the response as a JSON object with country names as keys without any values.
    Example format: {{"Country1": "", "Country2": "", "Country3": ""}}"""
    
    for attempt in range(max_retries):
        try:
            # Add a random delay between requests (1-3 seconds)
            time.sleep(uniform(1, 3))
            
            response = model.generate_content(prompt)
            # Try to parse the response as JSON
            response_text = response.text.strip()
            # Remove any markdown code block markers if present
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            neighbors_dict = json.loads(response_text)
            # Convert to list of just country names
            return list(neighbors_dict.keys())
        except Exception as e:
            if attempt < max_retries - 1:
                # If it's not the last attempt, wait longer (5-10 seconds) before retrying
                print(f"Attempt {attempt + 1} failed for {city_name}: {str(e)}. Retrying...")
                time.sleep(uniform(5, 10))
            else:
                print(f"Error generating neighbors for {city_name} after {max_retries} attempts: {str(e)}")
                return []

def process_cities(input_file, output_file):
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Read input cities
        data = read_cities_json(input_file)
        
        # Create new data structure with generated neighbors
        new_data = []
        
        print("Generating travel destinations for each city...")
        total_cities = len(data)
        
        for index, city in enumerate(data, 1):
            city_name = city["name"]
            print(f"Processing {city_name}... ({index}/{total_cities})")
            
            neighbors = generate_neighbors_for_city(model, city_name)
            
            city_data = {
                "name": city_name,
                "neighbors": neighbors
            }
            new_data.append(city_data)
            
            # Save progress after each city
            with open(output_file, 'w') as f:
                json.dump(new_data, f, indent=2)
        
        print(f"\nResults saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure:")
        print("1. You have a valid API key from https://makersuite.google.com/app/apikey")
        print("2. You have set the GOOGLE_API_KEY environment variable with your key")
        print("3. Your input JSON file exists and is properly formatted")

if __name__ == "__main__":
    input_file = "countries.json"  # Your input JSON file
    output_file = "cities_with_neighborsflash.json"  # Where to save the results
    process_cities(input_file, output_file)
