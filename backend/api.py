from flask import Flask, request
import requests
import json

from Algorithm.steps import getSteps
from Algorithm.algorithm_time import short_path
from Algorithm.address import find_near_address

app = Flask("hackhpi-backend")

@app.route("/steps/")
def hello():
    return getSteps()

# way colors
colors = {
    "accessible": "rgb(35, 155, 86)",
    "challenging": "rgb(243, 156, 18)",
    "difficult": "rgb(169, 50, 38)"
}

@app.route("/way/")
def way():
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))

    # start = 1532
    # end = 608

    geoJson = {
        "type": "FeatureCollection", 
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [

                    ]
                }
            }
        ]
    }

    shortest_path = short_path(start, end, "prosthetics", "challenging")

    for node in shortest_path["path"]:
        geoJson["features"][0]["geometry"]["coordinates"].append([node[1], node[0]])

    return geoJson

@app.route("/way/full")
def full_way():
    startAddress = request.args.get("start")
    endAddress = request.args.get("end")

    start_node = int(find_near_address(startAddress))
    end_node = int(find_near_address(endAddress))
    
    #print(str(start_node) + " " + str(end_node))

    short_path(start_node,end_node, 'prosthetics', 'accessible')

    with open("Algorithm/json/output_time_path.json", "r") as file:
        data = json.load(file);
    
    output = {}
    types = ["accessible", "challenging", "difficult"]

    for type in types:
        path = data[type]["path"]
        geoJson = {
            "type": "FeatureCollection", 
            "features": [

            ]
        }

        for way in path:
            geoJson["features"].append({
                    "type": "Feature",
                    "properties": {
                        "route-color": colors[way[4]]
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [
                                way[1], way[0]
                            ],
                            [
                                way[3], way[2]
                            ]
                        ]
                    }
                })
            
        output[type] = geoJson

    return output

# Test
# Stahnsdorfer Straße 140 14482
# Stahnsdorfer Straße 152 14482