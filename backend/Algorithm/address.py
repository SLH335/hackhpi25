import json
import math
 
def node_dist(node_1, node_2):
    return math.fabs((node_1["lat"] - node_2["lat"])) + math.fabs((node_1["lon"] - node_2["lon"]))
    

def find_nearest_node(target):
    currentMin = 10000000
    currentId = 0

    with open("Algorithm/nodes.json", "r") as file:
        data = json.load(file)

    with open("Algorithm/houses_nodes.json", "r") as file:
        house_data = json.load(file)
    
    print(house_data[str(target)])

    for node in data:
        dist = node_dist(data[node], house_data[str(target)])
        if dist < currentMin:
            #print(str(currentMin) + " " + node)
            currentMin = dist
            currentId = node

    return currentId

def find_near_address(address):
    with open("Algorithm/houses.json", "r") as file:
        data = json.load(file)

    targetId = data[address]

    return find_nearest_node(targetId);

print(find_near_address('Stahnsdorfer Straße 140 14482'))

# 9000787832