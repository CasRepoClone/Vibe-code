import requests
from bs4 import BeautifulSoup
import os

# URL for the search endpoint
url = "https://fotopolska.eu/nowa/search.php"

# Start page index (0) and set the increment to 24
start_page = 0
page_increment = 24 # fixed -- dont change this -- it skips one page
max_pages = 10  # You can change this to the number of pages you want to scrape


# wroclaw = 'm44538'  # Wroclaw location ID (you can change this to any other location ID)
# -- to do add array of search terms -- 

# Parameters for the search (example values, you can modify them as needed)
params = {
    'fraza': 'opuszczony',  # The search term
    'gdzie': 'm37076',      # The location ID (you may change it)
    'co': 'all',            # Category
    'start': '0',           # Start page (this will change in the loop)
    'showBar': 'true',
    'zapiszDoBazy': 'true',
    'zrodlo': 'inne'        # Source (could be changed)
}

# Headers to simulate a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Create a session to handle cookies
session = requests.Session()

# Directory to save all pages (Create the directory if it doesn't exist)
output_dir = 'search_results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Iterate through pages
for page in range(max_pages):
    # Update the 'start' parameter to point to the correct page number
    params['start'] = str(start_page)

    # Send a POST request to the server
    response = session.post(url, data=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Page {page + 1} - Request Successful!")
    else:
        print(f"Page {page + 1} - Request Failed with status code: {response.status_code}")
        continue  # Skip to next page if failed

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the full HTML page as a file
    page_filename = f'{output_dir}/page_{page + 1}.html'
    with open(page_filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    # Increase the start page index by 24 for the next iteration
    start_page += page_increment
    print(f"Saved page {page + 1} to {page_filename}")

print("All pages have been saved successfully.")
