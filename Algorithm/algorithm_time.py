import json
import numpy as np

MAXDIST = int(2e4) #in sec (approx. 6h)
MAXNODE = int(1e6)

node_lat = []
node_lon = []

def dist(a,b):
    dLat = node_lat[a]- node_lat[b]
    dLon = node_lon[a]- node_lon[b]
    #coordinate to meter
    dLat*=np.pi/180.0
    dLon*=np.pi/180.0

    e = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(node_lat[a] * np.pi / 180) * np.cos(node_lat[b] * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    f = 2 * np.atan2(np.sqrt(e), np.sqrt(1-e))
    return int(6371000*f/0.65)

def short_path(start_node, end_node):
    # Open and read the JSON file
    with open('data_compressed.json', 'r') as file:
        data = json.load(file)
    
    distance_from_start = [(MAXDIST, -1) for i in range(MAXNODE)]
    distance_from_end = [(MAXDIST, -1) for i in range(MAXNODE)]
    graph = [[] for i in range(MAXNODE)]

    for ele in data:
        if (ele['type']=='node'):
            node_lat.append(ele['lat'])
            node_lon.append(ele['lon'])


    #create graph from data
    for ele in data:
        if ele['type']=='way' and 'tags' in ele and 'highway' in ele['tags']:    
            #restriction for some ways (stairs, ...
            way_type = ele['tags']['highway']
            surface = "no info"
            if 'surface' in ele['tags']:
                surface = ele['tags']['surface']
            if way_type=='steps':
                surface = 'steps'
            prior_node = -1
            for ele2 in ele['nodes']:
                if (prior_node>=0):
                    graph[prior_node].append((ele2, surface))
                    graph[ele2].append((prior_node, surface))
                prior_node = ele2

    curr_dist = [[] for i in range(MAXNODE)]
    curr_dist[0].append((start_node, -1))

    #dijkstra
    for time in range(MAXDIST):
        for (node, prior) in curr_dist[time]:
            if distance_from_start[node][0]>time:
                distance_from_start[node]= (time, prior)
                for neighbour in graph[node]:
                    curr_dist[time+dist(node, neighbour[0])].append((neighbour[0], node))

    #go through from the back to get the coordinates
    print(distance_from_start[end_node])

    time_path = {"time": distance_from_start[end_node][0], "path": []}
    curr = end_node
    while curr != -1:
        time_path['path'].append((node_lat[curr], node_lon[curr]))
        curr = distance_from_start[curr][1]

    with open("output_time_path.json", 'w') as outfile:
        json.dump(time_path, outfile)

if __name__ == "__main__":
    short_path(1532,608)