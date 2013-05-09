import json
import string
import sys

predefinedTypes = ["float", "integer", "date", "bool", "string"]
validAttribChars = string.letters + '1234567890_'
filename = sys.argv[1]
errorFile = open("messages.log","w")
f = open(filename, "r")
typeInfo = json.loads(f.readline())
for attrib in typeInfo:
    if typeInfo[attrib] not in predefinedTypes:
        errorFile.write("invalid type definition for "+ str(attrib) +"\n")

itemJson = [json.loads(line) for line in f]
f.close()

attribs = []
ids = []
for e in enumerate(itemJson):
    if not e[1].has_key("id"):
        errorFile.write("item at line number" + str(e[0] + 1) + " doesnt have an id\n")

    for attrib in e[1]:
        for char in attrib:
            if char not in validAttribChars:
                errorFile.write("      the attibute " + str(attrib) + " contains invalid characters.\n")
                break
    
    for attrib in e[1]:
        if attrib not in typeInfo:
            errorFile.write("     the type of '" + str(attrib) + "' for the item at line " + str(e[0] + 2) + " is not defined.\n")

    for attrib in e[1]:
        if type(e[1][attrib]) != list:
            errorFile.write("     " + str(attrib) + " for the item at line " + str(e[0] + 2) + " should be a list.\n")

f = open(filename, "r")
count = 0
itemList = {}
for line in f:
    count += 1
    try :
        item = json.loads(line)
        itemList[str(item["id"][0])] = True
    except ValueError:
        errorFile.write("Error in " + str(count) + " of user item data set\n")
f.close()

userSequence = {}
f = open(filename+"_userData.json", "r")
count = 0
for line in f:
    count += 1
    #print count
    try :
        userData = json.loads(line)
        userSequence.update(userData)
        for item,rating in userData[userData.keys()[0]]:
            #print item
            if not itemList.has_key(str(item)) :
                errorFile.write("Item " + str(item) + " is not in ItemData set\n")
    except ValueError:
        errorFile.write("Error in " + str(count) + "of user data set\n")
f.close()
errorFile.close()