import json
import pickle
fin = open("ratings_1m.dat", "r")
fout = open("movielens_userData_1m.json", "w")
userData = {}

for line in fin:
    data = line.split("::")
    if data[0] in userData:
        userData[data[0]].append( (data[3], data[1], data[2]) )
    else:
        userData[data[0]] = [(data[3], data[1], data[2])]

for user in userData:
    userData[user].sort()
    userData[user] = [ (movie,rating) for timestamp, movie, rating in userData[user]]

for user in userData:
    fout.write(json.dumps({user: userData[user]}) + "\n")
fout.close()
fin.close()