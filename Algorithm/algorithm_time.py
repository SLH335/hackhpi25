import json
import numpy as np

MAXDIST = int(2e4) #in sec (approx. 6h)
MAXNODE = int(1e6)

node_lat = []
node_lon = []

surface_groups = {
    'asphalt': 'accessible',
    'cobblestone': 'difficult',
    'paving_stones': 'accessible',
    'concrete': 'accessible',
    'wood': 'accessible',
    'unpaved': 'challenging',
    'compacted': 'challenging',
    'gravel': 'challenging',
    'fine_gravel': 'difficult',
    'grass_paver': 'accessible',
    'ground':'difficult',
    'earth':'difficult',
    'dirt':'difficult',
    'mud':'difficult',
    'grass':'difficult',
    'sand':'difficult',
    'metal':'accessible',
    'sett':'challenging',
    'steps':'steps',
}

surface_stats = {
    'wheelchair': {
        'difficult': 0.0,
        'challenging': 0.5 * 0.65,
        'accessible': 1.0 * 0.65,
        'steps':0.0,
    },
    'prosthetics': {
        'difficult': 0.6 * 1.25,
        'challenging': 0.8 * 1.25,
        'accessible': 1.0 * 1.25,
        'steps':0.0,
    }
}

def dist(a,b, surface, disability):
    if surface_stats[disability][surface]==0.0:
        return int(MAXDIST)
    dLat = node_lat[a]- node_lat[b]
    dLon = node_lon[a]- node_lon[b]
    #coordinate to meter
    dLat*=np.pi/180.0
    dLon*=np.pi/180.0

    e = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(node_lat[a] * np.pi / 180) * np.cos(node_lat[b] * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    f = 2 * np.atan2(np.sqrt(e), np.sqrt(1-e))
    return int(6371000*f/0.65/surface_stats[disability][surface])

def short_path(start_node, end_node, disability, default_surface):
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
            surface = default_surface
            if 'surface' in ele['tags']:
                surface = surface_groups[ele['tags']['surface'].split(':')[0]]
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
                    newtime = time+dist(node, neighbour[0], neighbour[1], disability)
                    if newtime < MAXDIST:
                        curr_dist[newtime].append((neighbour[0], node))

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
    short_path(1532,608, 'prosthetics', 'accessible')