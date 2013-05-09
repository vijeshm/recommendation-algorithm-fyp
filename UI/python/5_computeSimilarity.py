import json
import sys
import fileinput
import itertools

dbFileName = sys.argv[1]

def readKeyValueNodes(fileName):
    f = open(fileName, "r")
    keyValueNodes = json.loads(f.read())
    f.close()
    return keyValueNodes

def readUserSequence(fileName):
    userSequence = {}
    for line in fileinput.input(fileName):
        jsonUser = json.loads(line)
        userSequence.update(jsonUser)
    return userSequence

def readTypeInfo(fileName):
    f = open(fileName, "r")
    datatype = json.loads(f.read())
    f.close()
    return datatype

class buildUserSimilarityDictNew(object):
    '''
    parllelizing the user profile generation with G object 
    '''
    def __init__(self, keyValueNodes, userSequence, userProfiles, dbFileName):
        nodes = keyValueNodes.keys()
        #self.G = buildGraph(keyValueNodes)
        self.keyValueNodes = keyValueNodes
        self.userProfiles = userProfiles
        self.dbFileName = dbFileName
        self.userSimilarity = {}
        self.userList = userSequence.keys()
        self.userSequence = userSequence

        for user in self.userList:
            self.userSimilarity[user]={}
        
        for user in self.userSequence:
            self.userSequence[user] = [item for item, rating in self.userSequence[user]]
    
    def buildSimilarity(self):
        itemLookup = {}
        for user in self.userSequence:
            for item in self.userSequence[user]:
                try:
                    itemLookup[item].append(user)
                except KeyError:
                    itemLookup[item] = [user]

        for key in self.keyValueNodes:
            for value in self.keyValueNodes[key]:
                for item in self.keyValueNodes[key][value]:
                    if not itemLookup.has_key(item):
                        itemLookup[item] = []

        keyCount = 0
        keyTotal = float(len(self.keyValueNodes))
        for key in self.keyValueNodes:
            keyCount += 1

            valueCount = 0
            valueTotal = float(len(self.keyValueNodes[key]))
            for value in self.keyValueNodes[key]:
                valueCount += 1

                combo = list(itertools.combinations(self.keyValueNodes[key][value], 2))
                pairCount = 0
                pairTotal = float(len(combo))

                for itemPair in combo:
                    pairCount += 1

                    usersList1 = set(itemLookup[itemPair[0]])
                    usersList2 = set(itemLookup[itemPair[1]])
                    intersection = usersList1.intersection(usersList2)
                    union = usersList1.union(usersList2)
                    intersectionPairs = set(itertools.combinations(list(intersection), 2))
                    unionPairs = set(itertools.combinations(list(union), 2))
                    diffPairs = unionPairs.difference(intersectionPairs)

                    for userPair in intersectionPairs:
                        try:
                            incValue = self.userProfiles[userPair[0]]["weights"][key]["@RAI"] + self.userProfiles[userPair[1]]["weights"][key]["@RAI"]
                            self.userSimilarity[userPair[0]][userPair[1]][0] += incValue
                            self.userSimilarity[userPair[0]][userPair[1]][1] += incValue
                        except KeyError:
                            if not self.userSimilarity.has_key(userPair[0]):
                                self.userSimilarity[userPair[0]] = {}

                            if not self.userSimilarity[userPair[0]].has_key(userPair[1]):
                                self.userSimilarity[userPair[0]][userPair[1]] = [0,0]

                            self.userSimilarity[userPair[0]][userPair[1]][0] += incValue
                            self.userSimilarity[userPair[0]][userPair[1]][1] += incValue            

                    for userPair in diffPairs:
                        try:
                            self.userSimilarity[userPair[0]][userPair[1]][1] += self.userProfiles[userPair[0]]["weights"][key]["@RAI"] + self.userProfiles[userPair[1]]["weights"][key]["@RAI"]
                        except KeyError:
                            if not self.userSimilarity.has_key(userPair[0]):
                                self.userSimilarity[userPair[0]] = {}

                            if not self.userSimilarity[userPair[0]].has_key(userPair[1]):
                                self.userSimilarity[userPair[0]][userPair[1]] = [0,0]
        
                            self.userSimilarity[userPair[0]][userPair[1]][1] += self.userProfiles[userPair[0]]["weights"][key]["@RAI"] + self.userProfiles[userPair[1]]["weights"][key]["@RAI"]
                    
                    print keyCount / keyTotal, valueCount / valueTotal, pairCount / pairTotal
                #print keyCount / keyTotal, valueCount / valueTotal
            #print keyCount / keyTotal

        print "writing " + self.dbFileName + "_userSimilarity.json"
        f = open(self.dbFileName+"_userSimilarity.json","w")
        f.write(json.dumps(self.userSimilarity))
        f.close()
        print "done writing " + self.dbFileName + "_userSimilarity.json"

f = open(dbFileName + "_normalizedUserProfiles.json", "r")
userProfiles = {}
for line in f:
    userProfiles.update(json.loads(line))
f.close()

keyValueNodes = readKeyValueNodes(dbFileName + "_keyValueNodes.json")
userSequence = readUserSequence(dbFileName + "_userData.json") 
datatype = readTypeInfo(dbFileName + "_typeInfo.json")

print "building user similarity"
buildUserSimilarityDictNew(keyValueNodes, userSequence, userProfiles, dbFileName).buildSimilarity()
print "done building user similarity"