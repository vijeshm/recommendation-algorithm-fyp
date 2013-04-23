import json
import sys

key = sys.argv[1]

f = open("../movielens_100k_keyValueNodes.json", "r")
keyValueNodes = json.loads(f.read())
f.close()

for value in keyValueNodes[key]:
    if len(keyValueNodes[key][value]) > 1:
        print key, value, keyValueNodes[key][value]