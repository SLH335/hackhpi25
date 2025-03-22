import requests
import json

# Overpass API URL
url = "http://overpass-api.de/api/interpreter"

# Overpass Query (Example: Get footways in a bounding box)
query = """
[out:json][timeout:25];
(
 (way["highway"](52.377537, 13.096930,52.68062, 13.70956);
- way["highway"~"motoway|trunk|primary|secondary|cycleway|bridleway"](52.377537, 13.096930,52.68062, 13.70956);
 );
 way["footway"](52.377537, 13.096930,52.68062, 13.70956);
);
(._;>;);
out body;
"""

smallerQuery = """
[out:json][timeout:25];
(
 (way["highway"](52.377537, 13.096930,52.398261,13.134915);
- way["highway"~"motoway|trunk|primary|secondary|cycleway|bridleway"](52.377537, 13.096930,52.398261,13.134915);
 );
 way["footway"](52.377537, 13.096930,52.398261,13.134915);
);
(._;>;);
out body;
"""

houseSmallQuery = """
[out:json][timeout:25];
(
  way[~"^addr:.*$"~"."](52.377537, 13.096930,52.3950581,13.1355584);
  - way["entrence"="yes"](52.377537, 13.096930,52.3950581,13.1355584);
);
(._;>;);
out body;
"""

def scrape():
    # Send request
    response = requests.get(url, params={"data": smallerQuery})

    # Check response
    if response.status_code == 200:
        data = response.json()
        with open("Algorithm/json/osm_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        #print(data)  # Do something with the result
    else:
        print(f"Error: {response.status_code}")

    # Send request
    response = requests.get(url, params={"data": houseSmallQuery})

    # Check response
    if response.status_code == 200:
        data = response.json()
        with open("Algorithm/json/house_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        #print(data)  # Do something with the result
    else:
        print(f"Error: {response.status_code}")
