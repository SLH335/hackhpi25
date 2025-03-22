import json
import numpy as np

MAXDIST = int(2e4) #in sec (approx. 6h)
MAXNODE = int(1e6)

node_lat = []
node_lon = []

difficulties = ['accessible', 'challenging', 'difficult']

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
        'steps':0.2 * 1.25,

    }
}

def get_worse_accessibility(difficulty1, difficulty2):
    if (difficulty1 == 'difficult' or difficulty2 == 'difficult'):
        return 'difficult'
    if (difficulty1 == 'challenging' or difficulty2 == 'challenging'):
        return 'challenging'
    return 'accessible'

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
    
    distance_from_start = {
        'accessible': [(MAXDIST, -1, 'accessible') for i in range(MAXNODE)],
        'challenging': [(MAXDIST, -1, 'accessible') for i in range(MAXNODE)],
        'difficult': [(MAXDIST, -1, 'accessible') for i in range(MAXNODE)],
    }
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

    curr_dist = {
        'accessible': [[] for i in range(MAXNODE)],
        'challenging': [[] for i in range(MAXNODE)],
        'difficult': [[] for i in range(MAXNODE)],
    }
    curr_dist['accessible'][0].append((start_node, -1, 'accessible'))

    #dijkstra
    for time in range(MAXDIST):
        for diff in difficulties:
            for (node, prior_node, prior_diff) in curr_dist[diff][time]:
                if distance_from_start[diff][node][0]>time:
                    distance_from_start[diff][node]= (time, prior_node, prior_diff)
                    for neighbour in graph[node]:
                        newtime = time+dist(node, neighbour[0], neighbour[1], disability)
                        if newtime < MAXDIST:
                            comb_diff = get_worse_accessibility(diff, neighbour[1])
                            curr_dist[comb_diff][newtime].append((neighbour[0], node, diff))



    #go through from the back to get the coordinates
    paths = {
        'accessible': {"time": distance_from_start['accessible'][end_node][0], "path": []},
        'challenging': {"time": distance_from_start['challenging'][end_node][0], "path": []},
        'difficult': {"time": distance_from_start['difficult'][end_node][0], "path": []}
    }
    if paths['accessible']['time']<paths['challenging']['time']:
        paths['challenging'] = paths['accessible']
    if paths['challenging']['time']<paths['difficult']['time']:
        paths['difficult'] = paths['challenging']

    for diff in difficulties:
        curr = end_node
        curr_diff = diff
        while curr != -1:
            paths[curr_diff]['path'].append((node_lat[curr], node_lon[curr]))
            curr = distance_from_start[diff][curr_diff][1] 
            curr_diff = distance_from_start[diff][curr_diff][2] 

    #stats on length of accessible, challenging, difficult part
    #new output format with line segments and their accessibility


    with open("output_time_path.json", 'w') as outfile:
        json.dump(paths, outfile)

if __name__ == "__main__":
    short_path(1532,608, 'prosthetics', 'accessible')