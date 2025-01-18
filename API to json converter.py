import requests
import json

def get_city_coordinates(city_name, username):
    url = f"http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username={username}"
    response = requests.get(url)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response Text: {response.text}")
        return None
    
    if data.get('geonames'):
        lat = data['geonames'][0]['lat']
        lon = data['geonames'][0]['lng']
        return lat, lon
    return None

    """if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    return None
    """
    
def create_json(latitude, longitude, filename):
    data = {
        "coordinates":{
            "latitude": latitude,
            "longitude": longitude
        }
    }

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON file '{filename}' has been created with coordinates.")


username = "username"
city_name = "Portland"
coordinates = get_city_coordinates(city_name, username)
if coordinates:
    print(f"Coordinates of {city_name}: Latitude = {coordinates[0]}, Longitude = {coordinates[1]}")
    filename = "geocoordinates.json"
    create_json(coordinates[0], coordinates[1], filename)
else:
    print(f"No results found for {city_name}")

