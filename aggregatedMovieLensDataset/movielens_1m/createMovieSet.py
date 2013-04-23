import json

fin = open("movielens_10m", "r")
fout = open("movielens_1m", "w")
websiteList = open("movies_1m.dat", "r")

movieList = {}

for line in fin:
    jsonObj = json.loads(line)
    movieList[jsonObj["id"][0]] = jsonObj

for line in websiteList:
    data = line.split("::")
    if movieList.has_key(int(data[0])):
        fout.write(json.dumps(movieList[int(data[0])]) + "\n")
    else:
        print data[0] + " is unavailable."

websiteList.close()
fout.close()
fin.close()