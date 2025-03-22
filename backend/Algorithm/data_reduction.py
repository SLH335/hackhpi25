import json

# Open and read the JSON file
with open('osm_data.json', 'r') as infile:
    data = json.load(infile)
data = data['elements']

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


print(oldid_newid[12670697443], oldid_newid[2513869310])        

with open("data_compressed.json", "w") as outfile:
    json.dump(data, outfile)