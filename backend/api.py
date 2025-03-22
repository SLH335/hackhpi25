from flask import Flask, request
import requests
import json

from Algorithm.steps import getSteps
from Algorithm.algorithm_time import short_path

app = Flask("hackhpi-backend")

@app.route("/steps/")
def hello():
    return getSteps()

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

    shortest_path = short_path(start, end)

    for node in shortest_path["path"]:
        geoJson["features"][0]["geometry"]["coordinates"].append([node[1], node[0]])

    return geoJson