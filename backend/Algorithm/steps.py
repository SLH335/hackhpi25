import json
 
def getSteps():
    data = {}

    steps = {
        "obstacles": [

        ]
    }

    with open("Algorithm/json/data.json") as json_file:
        data = json.load(json_file)

    nodes = {}

    for element in data["elements"]:
        if (element["type"] == "node"):
            nodes[element["id"]] = [
                element["lat"],
                element["lon"]
            ]

        if element["type"] != "way": continue
        if not("highway" in element["tags"]): continue
        if element["tags"]["highway"] != "steps": continue

        wayLenght = len(element["nodes"])
        nodeId = element["nodes"][wayLenght//2]

        step = {
            "type": "steps",
            "lat": nodes[nodeId][0],
            "lon": nodes[nodeId][1]
        }

        steps["obstacles"].append(step);

    return steps