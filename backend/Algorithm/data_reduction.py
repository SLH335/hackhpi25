import json

MAXNODE = int(2e6)

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
}

def reduce():

    with open('Algorithm/json/osm_data.json', 'r') as infile:
        data = json.load(infile)
    data = data['elements']

    c=0

    # delete all nontraversable paths
    oldid_newid = {}
    c=0
    to_remove1 = []
    for i in range(len(data)):
        ele = data[i]
        if ele['type'] == 'node':
            oldid_newid[ele['id']]=c
            ele['id'] = c
            c+=1
        elif ele['type']=='way':
            if 'nodes' in ele:
                to_remove = []
                for i in range(len(ele['nodes'])):
                    ele2 = ele['nodes'][i]
                    if ele2 in oldid_newid:
                        ele['nodes'][i] = oldid_newid[ele2]
                    else:
                        to_remove.append(ele2)
                for rem_ele in to_remove:
                    ele['nodes'].remove(rem_ele)
                if len(ele['nodes'])==0:
                    to_remove1.append(ele)

    for ele in to_remove1:
        data.remove(ele)

    for i in range(len(data)):
        ele = data[i]
        if ele['type']=='way':
            surface = "no info"
            if surface in ele['tags']:
                surface = ele['tags']['surface']
            if 'highway' in ele['tags'] and ele['tags']['highway']== 'steps':
                surface = 'steps'
            data[i] = {'type':'way', 'id':ele['id'], 'surface':surface, 'nodes':ele['nodes']}


    #print(oldid_newid[12670697443], oldid_newid[2513869310])        

    with open("Algorithm/json/data_compressed.json", "w") as outfile:
        json.dump(data, outfile)

    graph = [[] for i in range(MAXNODE)]

    for ele in data:
        if ele['type']=='way':  
            surface = "no info"  
            if ele['surface'] != 'no info':
                type = ele['surface'].split(':')[0].split('/')[0].split(',')[0].split(';')[0].split('_')[0].split('=')[-1]
                if (type in surface_groups):
                    surface = surface_groups[type]
            prior_node = -1
            for ele2 in ele['nodes']:
                if (prior_node>=0):
                    graph[prior_node].append((ele2, surface))
                    graph[ele2].append((prior_node, surface))
                prior_node = ele2

    with open("Algorithm/json/graph.json", "w") as outfile:
        json.dump(graph, outfile)

    stairs_and_uneven = []

    for ele in data:
        if ele['type']=='way':
            if ele['surface']=='steps':    
                stairs_and_uneven.append(ele)
            elif ele['surface'] != 'no info':
                type = ele['surface'].split(':')[0].split('/')[0].split(',')[0].split(';')[0].split('_')[0].split('=')[-1]
                if (type in surface_groups and surface_groups[type]!='accessible'):
                    stairs_and_uneven.append(ele)

    with open("Algorithm/json/stairs_and_uneven.json", "w") as outfile:
        json.dump(stairs_and_uneven, outfile)
                    
                            

