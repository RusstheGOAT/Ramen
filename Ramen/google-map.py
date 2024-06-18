import googlemaps
import json
from tqdm import tqdm

# Initialize the Google Maps client
gmaps = googlemaps.Client(key='My_API_Key')

def get_place_details(place_name):
    # Using Google Maps Places API to search for the place
    place_name += "拉麵"
    search_result = gmaps.places(query=place_name, language='zh-TW')
    if search_result['status'] == 'OK':
        place_id = search_result['results'][0]['place_id']
        
        # Get the details of the place
        place_details = gmaps.place(place_id=place_id, language='zh-TW')
        
        if place_details['status'] == 'OK':
            result = place_details['result']
            details = {
                '店名': result.get('name'),
                '店家地址': result.get('formatted_address'),
                '聯絡電話': result.get('formatted_phone_number'),
                '營業時間': result.get('opening_hours', {}).get('weekday_text'),
            }
            return details
        else:
            print(f"Error fetching details: {place_details['status']}")
    else:
        print(f"Error searching place: {search_result['status']}, {place_name}")
    return None

# From the file, read the places to search
with open('places.txt', 'r', encoding='utf-8') as file:
    places = [line.strip() for line in file.readlines()]

# Save the results
results = []

# Search for each place
for place in tqdm(places):
    details = get_place_details(place)
    if details:
        results.append(details)

# Save the results to a JSON file
with open('places_details_ch.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Done!")