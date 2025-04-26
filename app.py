from flask import Flask, render_template
import json
import os
# Replace with your actual Google Maps API Key

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


app = Flask(__name__)

# Load locations (pins) from the JSON file
with open('pins_no_duplicates.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)



@app.route('/')
def map_view():
    print("Rendering map view...")
    return render_template('map.html', locations=locations, api_key=API_KEY)

if __name__ == '__main__':
    app.run(debug=True)
