import json
import fileinput
import sys

dbfilename = sys.argv[1]
uid = sys.argv[2]

f = open(dbfilename + "_userProfiles_afterNorming.json", "r")
jsonString = f.read()
f.close()

f = open("attribList.txt", "w")
userSequence = json.loads(jsonString)
for attrib in userSequence[uid]["weights"]:
	f.write(attrib + "\n")
f.close()