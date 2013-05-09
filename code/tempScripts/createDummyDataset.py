import sys
import random
import string
import json

numberOfItems = 100
numberOfUsers = 1000
numberOfAttribs = 10
maxNumberOfValues = 10
minNumberOfValues = 3
maxNumberOfItems = 40
minNumberOfItems = 20
ratings = ['1', '2', '3', '4', '5']
attribs = [''.join(random.sample(string.lowercase, random.randint(1,15))) for i in range(numberOfAttribs)]
attribValues = {}
for attrib in attribs:
    attribValues[attrib] = [''.join(random.sample(string.lowercase, random.randint(1,15))) for i in range(minNumberOfValues, maxNumberOfValues)]

typeInfo = {attrib:"string" for attrib in attribs}
items = []
for i in range(numberOfItems):
    item = {}
    item["id"] = [str(i)]
    for attrib in attribs:
        item[attrib] = random.sample(attribValues[attrib], random.randint(1, len(attribValues[attrib])))
    items.append(item)

f = open("dummy_itemset", "w")
f.write(json.dumps(typeInfo) + "\n")
for item in items:
    #print item
    f.write(json.dumps(item) + "\n")
f.close()

userInfo = {}
for i in range(numberOfUsers):
    items = random.sample(items, min(len(items), random.randint(minNumberOfItems, maxNumberOfItems)))
    userInfo[i] = [(item["id"][0], random.choice(ratings)) for item in items]

f = open("dummy_userset", "w")
for user in userInfo:
    f.write(json.dumps({user: userInfo[user]}) + "\n")
f.close()