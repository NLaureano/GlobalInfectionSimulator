# So i grab the 10k cities, and then pull information
# population, 
# urbanization of infectious rate, some sort of indicator to indicate whether theyll be more suceptible to infectious diseases

# are there neighbors, and the likelihood of going there, and the likeliness of infectious diseases getting spread base on neighbors



# Add to my script
# I want to generate a list of 10k popular cities. 
# I want to generate from each city their population, the cities they're most likely go to. 
# I want this to be a json file




import requests

# Replace this with your actual Gemini API key
API_KEY = "your_gemini_api_key"

# Base URL for Gemini API
BASE_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

def fetch_infectious_diseases():
    """
    Queries the Gemini API to generate a list of infectious diseases.
    """
    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Prompt for the AI
    prompt = "Generate a list of infectious diseases with their common names and descriptions."

    # Payload for the API request
    payload = {
        "prompt": prompt,
        "maxOutputTokens": 500,  # Adjust this based on the level of detail you need
        "temperature": 0.7  # Controls randomness in the response
    }

    try:
        # Send the request to the API
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the API response
        result = response.json()
        generated_text = result.get("candidates", [{}])[0].get("output", "")

        if generated_text:
            print("Generated List of Infectious Diseases:")
            print(generated_text)
        else:
            print("No output generated. Please check your request parameters.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
        
        
def generate_city_data():
    """
    Queries the Gemini API to generate a list of 10,000 popular cities, 
    their populations, and the cities residents are most likely to visit.
    """
    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Prompt for the AI
    prompt = (
        "Generate a detailed list of 10,000 popular cities. "
        "For each city, include: "
        "1) the city's population, "
        "2) the top 5 cities that residents are most likely to visit. "
        "Format the response as a JSON array with each object having the following keys: "
        "'city', 'population', 'popular_destinations'."
    )

    # Payload for the API request
    payload = {
        "prompt": prompt,
        "maxOutputTokens": 500,  # Adjust based on the amount of data returned per request
        "temperature": 0.7  # Controls randomness in the response
    }

    try:
        # Send the request to the API
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the API response
        result = response.json()
        generated_text = result.get("candidates", [{}])[0].get("output", "")

        if generated_text:
            print("Generated City Data:")
            print(generated_text)  # Optionally save or process the data further
        else:
            print("No output generated. Please check your request parameters.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Call the function to fetch infectious diseases
fetch_infectious_diseases()

# Call the function to generate city data
generate_city_data()

'''
EXAMPLE OUTPUT
[
    {
        "city": "New York",
        "population": 8419600,
        "popular_destinations": ["Los Angeles", "Chicago", "Miami", "Las Vegas", "San Francisco"]
    },
    {
        "city": "Tokyo",
        "population": 13929286,
        "popular_destinations": ["Osaka", "Kyoto", "Seoul", "Shanghai", "Hong Kong"]
    },
    ...
]


'''