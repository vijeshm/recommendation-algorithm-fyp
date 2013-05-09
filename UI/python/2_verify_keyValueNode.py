import json
import string
import sys
import numpy 

filename = sys.argv[1]
def learnGraph(JSONdb):
    '''
    JSONdb (string) - file name of the db - a file of strings, each of which are in JSON format
    Given a database of items, this function generates the item relations graph that can be used to for recommending items to users in a content based manner.
    ''' 

    #open the file, read each line, parse it and put it onto the itemList
    itemList = []
    fp = open(JSONdb, "r")
    
    f = open(JSONdb + "_typeInfo.json", "w")
    typeInfo = json.loads(fp.readline())
    f.write(json.dumps(typeInfo))
    f.close()

    for line in fp:
        itemList.append(json.loads(line))
    fp.close()

    attributeAndNodes = {}  #{attribute1: {value1 : [item1, item2 ...], value2 : [item3, item4 ... ]}, attribute2 : ... }

    #Building the graph
    for item in itemList:
        uid = str(item['id'][0])

        for attrs in item:
            #check if the node already has the attribute.
            #If it does, for every attribute of the item, check if there is a list associated for the value. If the list exists, append the uid to the list. If it doesnt, initialize a list with the uid of the item.
            #If it doesnt, initialize the attributeAndNodes[attrs] to an empty dictionary. For every attribute of the item, update the attributeAndNodes dictionary.
            if attributeAndNodes.has_key(attrs):
                for attribute in item[attrs]:
                    if attributeAndNodes[attrs].has_key(attribute):
                        attributeAndNodes[attrs][attribute].append(uid)
                    else:
                        attributeAndNodes[attrs][attribute] = [uid]
            else:
                attributeAndNodes[attrs] = {}
                for attribute in item[attrs]:
                    attributeAndNodes[attrs][attribute] = [uid]

    for attr in attributeAndNodes:
        if typeInfo[attr]=="float" or typeInfo[attr] == "integer" or typeInfo[attr] == "date":
            inp = [float(value) for value in attributeAndNodes[attr]]
            inp.sort()
            
            dist = [ (inp[i+1] - inp[i]) for i in range(len(inp) - 1) ]
            avrg = numpy.average(dist)

            cutpoint = 0
            clusters = []
            for i in range(len(dist)):
                if dist[i] >= avrg:
                    clusters.append(inp[cutpoint:i+1])
                    cutpoint = i+1

            if cutpoint != len(dist):
                clusters.append(inp[cutpoint:])

            newVal = {}
            for cluster in clusters:
                nodes = []
                for value in cluster:
                    nodes.extend(attributeAndNodes[attr][value])
                newVal[str(cluster)] = nodes
            attributeAndNodes[attr] = newVal

    print "writing " + JSONdb + "_keyValueNodes.json"
    f = open(JSONdb + "_keyValueNodes.json", "w")
    f.write(json.dumps(attributeAndNodes))
    f.close()
    print "done writing " + JSONdb + "_keyValueNodes.json"

predefinedTypes = ["float", "integer", "date", "bool", "string"]
errorFlag = False
validAttribChars = string.letters + '1234567890_'
errorFile = open(filename+"_messages.log","w")
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
        errorFlag = True

    for attrib in e[1]:
        for char in attrib:
            if char not in validAttribChars:
                errorFile.write("      the attibute " + str(attrib) + " contains invalid characters.\n")
                errorFlag = True
                break
    
    for attrib in e[1]:
        if attrib not in typeInfo:
            errorFile.write("     the type of '" + str(attrib) + "' for the item at line " + str(e[0] + 2) + " is not defined.\n")
            errorFlag = True

    for attrib in e[1]:
        if type(e[1][attrib]) != list:
            errorFile.write("     " + str(attrib) + " for the item at line " + str(e[0] + 2) + " should be a list.\n")
            errorFlag = True

f = open(filename, "r")
count = 0
itemList = {}
for line in f:
    count += 1
    try :
        item = json.loads(line)
        itemList[str(item["id"][0])] = True
    except ValueError:
        errorFile.write("Error in " + str(count) + " of item data set\n")
        errorFlag = True
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
                errorFlag = True
    except ValueError:
        errorFile.write("Error in line " + str(count) + " of user data set. One of the items doesnt have rating.\n")
        errorFlag = True
f.close()
errorFile.close()

if not errorFlag:
    learnGraph(filename)
