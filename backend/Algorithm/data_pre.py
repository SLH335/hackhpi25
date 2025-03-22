import json

"""Needs data form this query
[out:json][timeout:25];

(
  way[~"^addr:.*$"~"."](52.389144,13.122695,52.3950581,13.1355584);
  - way["entrence"="yes"](52.389144,13.122695,52.3950581,13.1355584);
);
  
(._;>;);
out body;
"""

def pre_houses():
    with open("Algorithm/house_data.json", "r") as file:
        data = json.load(file)["elements"]

    newHouseJson = {}

    # schlechte Variante
    nodes = {}

    for element in data:
        
        if element["type"] == "node":
            nodes[element["id"]] = {
                    "lat": element["lat"],
                    "lon": element["lon"]
                }      

        if element["type"] != "way": continue
        if not("addr:housenumber" in element["tags"]): continue

        currentAddress = element["tags"]["addr:street"] + " " + element["tags"]["addr:housenumber"] + " " + element["tags"]["addr:postcode"]

        newHouseJson[currentAddress] = element["nodes"][0]

    with open("Algorithm/houses.json", 'w', encoding="utf-8") as outfile:
        json.dump(newHouseJson, outfile)

    with open("Algorithm/houses_nodes.json", "w") as outfile:
        json.dump(nodes, outfile)

def pre_nodes():
    with open("Algorithm/data.json") as file:
        data = json.load(file)["elements"]
    
    nodes = {}

    for element in data:
        if element["type"] != "node": continue

        nodes[element["id"]] = {
                    "lat": element["lat"],
                    "lon": element["lon"]
                }      

    with open("Algorithm/nodes.json", "w") as file:
        json.dump(nodes, file)

def pre_calc():
    pre_houses()
    pre_nodes()

if __name__ == "__main__":
    pre_calc()