import requests
from bs4 import BeautifulSoup
import os
from googletrans import Translator
import json
from urllib.parse import unquote
global error_counter  # Keeps track of the error number
error_counter = 0
# Base URL for the site
base_url = "https://fotopolska.eu"

# Initialize the Translator
translator = Translator()

# Initialize the list to store pins (lat, long, and description)
pins = []

# Function to extract description and latitude/longitude from a single photo page
def extract_description_and_latlong(url):
    # Send request to fetch the page
    response = requests.get(url)
    global error_counter  # Access the global error counter

    if error_counter > 10:
        return None, None, None
    
    if response.status_code == 200:
        print(f"Successfully fetched: {url}")
    else:
        print(f"Failed to fetch: {url}")
        return None, None, None

    # Parse the HTML content of the photo page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the content within the <div class="OpisZdjecia">
    description_div = soup.find('div', class_='OpisZdjecia')

    # Extract lat/lon from iframe
    iframe = soup.find('iframe', id='mapa')
    lat, lon = None, None  # Default values for lat and lon

    if iframe:
        # Find the lat/lon from the iframe's data-src
        data_src = iframe.get('data-src')
        if data_src:
            try:
                # Check if the 'lat=' and '&zoom' parameters exist in the data_src
                if "lat=" in data_src and "&zoom" in data_src:
                    # Extract lat, lon part (handle the encoded URL)
                    lat_lng_str = data_src.split("lat=")[1].split("&zoom")[0]  # Extract lat,lng part
                    lat_lng_str = unquote(lat_lng_str)  # Decode the URL-encoded string
                    lat, lon = lat_lng_str.strip('()').split(',')  # Now lat and lon should be decoded
                    lat = float(lat)  # Convert lat to float
                    lon = float(lon)  # Convert lon to float

                    # Ensure no leading '+' in the longitude
                    lon = abs(lon)  # Use absolute value to ensure no leading '+'
                else:
                    print(f"Warning: 'lat=' or '&zoom' not found in data-src for URL: {url}")
                    lat, lon = None, None  # Return None for lat/lon if not found
            except Exception as e:
                print(f"Error parsing lat/lon from iframe: {e}")
                lat, lon = None, None  # In case of any parsing error
        else:
            print(f"No data-src found in iframe for URL: {url}")
            lat, lon = None, None
    else:
        print(f"No iframe found for lat/lon extraction on {url}")
    
    # Return the description and lat/lon (lat and lon could be None if extraction failed)
    if description_div:
        return description_div.get_text(strip=True), lat, lon
    else:
        print(f"No description found for: {url}")
        error_counter += 1
        return None, lat, lon

# Function to translate text to English
def translate_to_english(text):
    try:
        translated = translator.translate(text, src='pl', dest='en')  # Translate from Polish to English
    except:
        return ""  # Return empty if error
    return translated.text

# Iterate through saved HTML pages to extract hrefs
page_counter = 0  # Keeps track of the page number

for page_num in range(1, 83):  # Adjust the range to iterate through your saved pages will get x*6 results


    if error_counter > 10:
        break
    page_filename = f'search_results/page_{page_num}.html'
    
    # Check if the page file exists
    if not os.path.exists(page_filename):
        print(f"Page file {page_filename} does not exist, skipping...")
        continue
    
    page_counter += 1  # Increment page number
    
    # Open the page file and parse it
    with open(page_filename, 'r', encoding='utf-8') as f:
        page_content = f.read()

    soup = BeautifulSoup(page_content, 'html.parser')

    # Find all links with href that contain the photo page URL pattern
    links = soup.find_all('a', href=True)

    result_counter = 0  # Keeps track of the result number on this page
    
    for link in links:
        href = link['href']
        # Check if the href contains a valid link to a photo page
        if href.startswith('/'):
            # Construct the full URL
            photo_url = base_url + href
            result_counter += 1  # Increment result number

            print(f"Extracting from: {photo_url}")

            # Extract the description and lat/lon from the photo page
            description, lat, lon = extract_description_and_latlong(photo_url)

            if description:
                # Translate the description to English
                translated_description = translate_to_english(description)

                # Add the pin (lat, lon, and description) to the pins list
                if lat and lon:
                    pins.append({
                        "name": f"Result {result_counter}",
                        "lat": lat,
                        "lng": lon,
                        "description": translated_description
                    })

# Save the pins data to a JSON file
with open('pins.json', 'w', encoding='utf-8') as json_file:
    json.dump(pins, json_file, ensure_ascii=False, indent=4)

print(f"Pins data saved to pins.json.")
print(f"Total pages processed: {page_counter}")
