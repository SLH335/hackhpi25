import requests
import json

# Overpass API URL
url = "http://overpass-api.de/api/interpreter"

# Overpass Query (Example: Get footways in a bounding box)
query = """
[out:json][timeout:25];
(
 (way["highway"](52.34081, 12.97565,52.68062, 13.70956);
- way["highway"~"motoway|trunk|primary|secondary|cycleway|bridleway"](52.34081, 12.97565,52.68062, 13.70956);
 );
 way["footway"](52.34081, 12.97565,52.68062, 13.70956);
);
(._;>;);
out body;
"""

# Send request
response = requests.get(url, params={"data": query})

# Check response
if response.status_code == 200:
    data = response.json()
    with open("osm_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    print(data)  # Do something with the result
else:
    print(f"Error: {response.status_code}")


s