import json
import pickle
fin = open("ratings.dat", "r")
fout = open("movielens_userData.json", "w")
userData = {}

for line in fin:
    data = line.split("::")
    print data
    if data[0] in userData:
        userData[data[0]].append( (data[1], data[2]) )
    else:
        userData[data[0]] = [(data[1], data[2])]
fout.write(json.dumps(userData))
fout.close()
fin.close()