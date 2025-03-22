import json
import math
 
def node_dist(node_1, node_2):
    return math.fabs((node_1["lat"] - node_2["lat"])) + math.fabs((node_1["lon"] - node_2["lon"]))
    
# target -> point on map
def find_nearest_node(target):
    currentMin = 10000000
    currentId = 0

    with open("Algorithm/json/nodes.json", "r") as file:
        data = json.load(file)

    for node in data:
        dist = node_dist(data[node], target)
        if dist < currentMin:
            #print(str(currentMin) + " " + node)
            currentMin = dist
            currentId = node

    print(data[currentId])

    return currentId

def find_near_address(address):
    with open("Algorithm/json/houses.json", "r") as file:
        data = json.load(file)


    with open("Algorithm/json/houses_nodes.json", "r") as file:
        house_data = json.load(file)

    targetId = data[address]

    return find_nearest_node(house_data[str(targetId)]);

# Format {"lat": 12123, "lon": 123}
def find_near_koords(koords):
    return find_nearest_node(koords)

#print(find_near_address('Stahnsdorfer Straße 140 14482'))
#print(find_near_koords({"lat": 52.391884, "lon": 13.124553}))

# 9000787832