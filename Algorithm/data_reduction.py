import json

# Open and read the JSON file
with open('data.json', 'r') as infile:
    data = json.load(infile)
data = data['elements']

# delete all nontraversable paths
oldid_newid = {0:0}
c=0
for ele in data:
    if ele['type'] == 'node':
        oldid_newid[ele['id']]=c
        ele['id'] = c
        c+=1
    elif 'nodes' in ele:
        to_remove = []
        for i in range(len(ele['nodes'])):
            ele2 = ele['nodes'][i]
            if ele2 in oldid_newid:
                ele['nodes'][i] = oldid_newid[ele2]
            else:
                to_remove.append(ele2)
        for rem_ele in to_remove:
            ele['nodes'].remove(rem_ele)
        

with open("data_compressed.json", "w") as outfile:
    json.dump(data, outfile)