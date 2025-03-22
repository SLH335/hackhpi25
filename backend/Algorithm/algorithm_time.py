import json
import numpy as np

MAXDIST = int(2e4) #in sec (approx. 6h)
MAXNODE = int(2e6)

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
    'pebblestone': 'difficult',
    'rock':'difficult',
    'metal':'accessible',
    'unhewn_cobblestone': 'challenging',
    'unhewn': 'challenging',
    'paved': 'accessible',
    'chipseal': 'difficult',
    'woodchips': 'difficult',
    'compound': 'difficult',
    'overgrown':'difficult',
    'metal_grid': 'accessible',
    'stone': 'challenging',
    'leaves': 'challenging',
    'macadam': 'challenging',
    'fine': 'difficult',
    'paving': 'accessible',
    'tartan': 'accessible',
    'brick': 'accessible',
    'rubber': 'challenging',
    'mulch': 'challenging',
    'grate': 'accessible',
    'sett':'challenging',
    'steps':'steps',
    'challenging': 'challenging',
    'accessable':'accessable',
    'difficult':'difficult'
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
    },
    'prosthetics_no_stairs': {
        'difficult': 0.6 * 1.25,
        'challenging': 0.8 * 1.25,
        'accessible': 1.0 * 1.25,
        'steps': 0.0,
    }
}

def get_worse_accessibility(difficulty1, difficulty2):
    if (difficulty1 == 'difficult' or difficulty2 == 'difficult'):
        return 'difficult'
    if (difficulty1 == 'challenging' or difficulty2 == 'challenging'):
        return 'challenging'
    return 'accessible'

def lat_to_meter(a, b):
    dLat = node_lat[a]- node_lat[b]
    dLon = node_lon[a]- node_lon[b]
    #coordinate to meter
    dLat*=np.pi/180.0
    dLon*=np.pi/180.0

    e = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(node_lat[a] * np.pi / 180) * np.cos(node_lat[b] * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    f = 2 * np.atan2(np.sqrt(e), np.sqrt(1-e))
    return 6371000*f

def dist(a,b, surface, disability):
    if surface_stats[disability][surface]==0.0:
        return int(MAXDIST)
    return int(lat_to_meter(a, b)/0.65/surface_stats[disability][surface])

def short_path(start_node, end_node, disability, default_surface):
    # Open and read the JSON file
    with open('Algorithm/json/data_compressed.json', 'r') as file:
        data = json.load(file)

    with open('Algorithm/json/graph.json', 'r') as file:
        graph = json.load(file)

    with open('Algorithm/json/stairs_and_uneven.json', 'r') as file:
        stairs_and_uneven = json.load(file)
    
    distance_from_start = {
        'accessible': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
        'challenging': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
        'difficult': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
    }
    distance_from_end = {
        'accessible': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
        'challenging': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
        'difficult': [(MAXDIST, -1, 'accessible', 'no info', 0, 0, 0, 0) for i in range(MAXNODE)],
    }

    for ele in data:
        if (ele['type']=='node'):
            node_lat.append(ele['lat'])
            node_lon.append(ele['lon'])

    curr_dist = {
        'accessible': [[] for i in range(MAXNODE)],
        'challenging': [[] for i in range(MAXNODE)],
        'difficult': [[] for i in range(MAXNODE)],
    }
    curr_dist['accessible'][0].append((start_node, -1, 'accessible', 'no info', 0, 0, 0, 0))

    #dijkstra
    for time in range(MAXDIST):
        for diff in difficulties:
            if (distance_from_start[diff][end_node][0] != MAXDIST):
                continue
            for (node, prior_node, prior_diff, surface, meter_total, meter_chal, meter_diff, steps) in curr_dist[diff][time]:
                if distance_from_start[diff][node][0]>time:
                    distance_from_start[diff][node]= (time, prior_node, prior_diff, surface, meter_total, meter_chal, meter_diff, steps)
                    for neighbour in graph[node]:
                        if (neighbour[1]=='no info'):
                            neighbour[1] = default_surface
                        newtime = time+dist(node, neighbour[0], neighbour[1], disability)
                        if newtime < MAXDIST:
                            comb_diff = get_worse_accessibility(diff, neighbour[1])
                            addmeter = lat_to_meter(neighbour[0], node)
                            newsteps = steps
                            newmeter_chal = meter_chal
                            newmeter_diff = meter_diff
                            if (neighbour[1]=='steps'):
                                comb_diff = get_worse_accessibility(comb_diff, 'challenging')
                                newsteps += addmeter*3
                                meter_chal+=addmeter
                            elif (neighbour[1]=='challenging'):
                                meter_chal+=addmeter
                            elif (neighbour[1] == 'difficult'):
                                meter_diff+=addmeter
                            curr_dist[comb_diff][newtime].append((neighbour[0], node, comb_diff, neighbour[1], meter_total+addmeter, meter_chal, meter_diff, int(newsteps)))

    curr_dist2 = {
        'accessible': [[] for i in range(MAXNODE)],
        'challenging': [[] for i in range(MAXNODE)],
        'difficult': [[] for i in range(MAXNODE)],
    }
    curr_dist2['accessible'][0].append((end_node, -1, 'accessible', 'no info', 0, 0, 0, 0))

    #dijkstra
    for time in range(MAXDIST):
        for diff in difficulties:
            if (distance_from_end[diff][start_node][0] != MAXDIST):
                continue
            for (node, prior_node, prior_diff, surface, meter_total, meter_chal, meter_diff, steps) in curr_dist2[diff][time]:
                if distance_from_end[diff][node][0]>time:
                    distance_from_end[diff][node]= (time, prior_node, prior_diff, surface, meter_total, meter_chal, meter_diff, steps)
                    for neighbour in graph[node]:
                        if (neighbour[1]=='no info'):
                            neighbour[1] = default_surface
                        newtime = time+dist(node, neighbour[0], neighbour[1], disability)
                        if newtime < MAXDIST:
                            comb_diff = get_worse_accessibility(diff, neighbour[1])
                            addmeter = lat_to_meter(neighbour[0], node)
                            newsteps = steps
                            newmeter_chal = meter_chal
                            newmeter_diff = meter_diff
                            if (neighbour[1]=='steps'):
                                comb_diff = get_worse_accessibility(comb_diff, 'challenging')
                                newsteps += addmeter*3
                                newmeter_chal+=addmeter
                            elif (neighbour[1]=='challenging'):
                                newmeter_chal+=addmeter
                            elif (neighbour[1] == 'difficult'):
                                newmeter_diff+=addmeter
                            curr_dist2[comb_diff][newtime].append((neighbour[0], node, comb_diff, neighbour[1], meter_total+addmeter, newmeter_chal, newmeter_diff, int(newsteps)))

    paths = {
        'accessible': {
            "time": distance_from_start['accessible'][end_node][0],
            "meter_total": distance_from_start['accessible'][end_node][4],
            "meter_challenging": distance_from_start['accessible'][end_node][5],
            "meter_difficult": distance_from_start['accessible'][end_node][6],
            "steps": distance_from_start['accessible'][end_node][7],
            "path": []
        },
        'challenging': {
            "time": distance_from_start['challenging'][end_node][0], 
            "meter_total": distance_from_start['challenging'][end_node][4],
            "meter_challenging": distance_from_start['challenging'][end_node][5],
            "meter_difficult": distance_from_start['challenging'][end_node][6],
            "steps": distance_from_start['challenging'][end_node][7],
            "path": []
        },
        'difficult': {
            "time": distance_from_start['difficult'][end_node][0], 
            "meter_total": distance_from_start['difficult'][end_node][4],
            "meter_challenging": distance_from_start['difficult'][end_node][5],
            "meter_difficult": distance_from_start['difficult'][end_node][6],
            "steps": distance_from_start['difficult'][end_node][7],
            "path": []
        }
    }
    if paths['accessible']['time']<paths['challenging']['time']:
        paths['challenging'] = paths['accessible']
        distance_from_start['challenging'] = distance_from_start['accessible']
        distance_from_end['challenging'] = distance_from_end['accessible']
    if paths['challenging']['time']<paths['difficult']['time']:
        paths['difficult'] = paths['challenging']
        distance_from_start['difficult'] = distance_from_start['challenging']
        distance_from_end['difficult'] = distance_from_end['challenging']


    obstacle_assessment = {
        'accessible': {},
        'challenging': {},
        'difficult': {},
    }

    for ele in stairs_and_uneven:
            begin = ele['nodes'][0]
            end = ele['nodes'][-1]
            for diff in difficulties:
                delta1 = distance_from_start[diff][begin][0]+distance_from_end[diff][end][0]
                delta2 = distance_from_start[diff][end][0]+distance_from_end[diff][begin][0]
                savings = distance_from_start[diff][end_node][0] - min(delta1, delta2)
                if ele['surface']=='steps':    
                    savings-=dist(begin, end, 'accessible', disability)
                    if (savings>30):
                        obstacle_assessment[diff][ele['id']] = (savings, 'steps')
                if ele['surface'] != 'no info':
                    type = ele['surface'].split(':')[0].split('/')[0].split(',')[0].split(';')[0].split('_')[0].split('=')[-1]
                    if (type in surface_groups):
                        surface = surface_groups[type]
                        savings-=dist(begin, end, 'accessible', disability)
                    if get_worse_accessibility(diff, surface)!=diff and savings>30:
                        obstacle_assessment[diff][ele['id']] = max(savings, surface)
                        

    

    #go through from the back to get the coordinates
    for diff in difficulties:
        curr = end_node
        curr_diff = diff

        while curr != -1:
            nextcurr = distance_from_start[curr_diff][curr][1] 
            surface = distance_from_start[curr_diff][curr][3] 
            if (nextcurr != -1):
                paths[diff]['path'].append((node_lat[nextcurr], node_lon[nextcurr], node_lat[curr], node_lon[curr], surface))
            curr = nextcurr
            curr_diff = distance_from_start[curr_diff][curr][2] 
        paths[diff]['path'].reverse()

    with open("Algorithm/json/output_time_path.json", 'w') as outfile:
        json.dump(paths, outfile)
    
    with open("Algorithm/json/output_obstacle_assessment.json", 'w') as outfile:
        json.dump(obstacle_assessment, outfile)

if __name__ == "__main__":
    short_path(1435424,378331, 'prosthetics', 'accessible')