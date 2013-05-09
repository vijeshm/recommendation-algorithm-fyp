import json
import sys
import fileinput
import itertools

dbFileName = sys.argv[1]
uid = sys.argv[2]

clusteredUsers = []
f = open(dbFileName+"_clusteredUsers.json","r")
clusteredUsers = json.loads(f.read())
f.close()

f = open(dbFileName+"_userClusters.json","w")
for cluster in clusteredUsers:
	if uid in cluster:
		f.write(str(cluster)+"\n")
f.close
