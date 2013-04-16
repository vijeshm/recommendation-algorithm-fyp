import random
import json
import sys

noOfUsers= int(sys.argv[1])
f = open("../movielens_1m_userData_6040.json","r")
userData = {}
for line in f:
	userData.update(json.loads(line))
f.close()

newUsers = dict(random.sample(userData.items(),noOfUsers))
f = open("../movielens_1m_userData.json","w")
for key in newUsers:
	f.write(json.dumps({key:newUsers[key]}))
	f.write("\n")
f.close()
