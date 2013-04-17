import sys
import json

uid = sys.argv[1]

def egocentricRecommendation(keyValueNodes, itemSequence, dbFileName, uid, userWeights):
    '''
    graphDb (networkx Graph object): The database containing the relation between items in a graphical form
    userSequence (list) : the sequence in which the user has been associated with items
    This function applies our content based filtering algorithm to generate a score ranging from 0-1 for every item. This object will be written to contentReco.pickle as a pickle object. This pickle object is a dictionary with uid and score as the key and value respectively.
    '''

    nodes = []
    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            nodes.extend(keyValueNodes[key][value])
    nodes = list(set(nodes))

    score = {}
    score["after"] = {}
    score["before"] = {}
    score["equal"] = {}
    equalWeight = 1.0 / len(userWeights["after"])

    for node in nodes:
        score["after"][node] = 0
        score["before"][node] = 0
        score["equal"][node] = 0

    userSequenceSet = set(itemSequence)

    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            if value != "@RAI" and value in userWeights["after"][key]:
                common = len(userSequenceSet.intersection(set(keyValueNodes[key][value])))
                for node in keyValueNodes[key][value]:
                    score["after"][node] += common * userWeights["after"][key][value] * userWeights["after"][key]["@RAI"]
                    score["before"][node] += common * userWeights["before"][key][value] * userWeights["before"][key]["@RAI"]
                    score["equal"][node] += common * equalWeight

    for item in itemSequence:
        score["after"].pop(item)
        score["before"].pop(item)
        score["equal"].pop(item)

    itemRanking = {}
    itemRanking["after"] = [ (itemScore, item) for item, itemScore in score["after"].items()]
    itemRanking["before"] = [ (itemScore, item) for item, itemScore in score["before"].items()]
    itemRanking["equal"] = [ (itemScore, item) for item, itemScore in score["equal"].items()]

    itemRanking["after"].sort(reverse=True)
    itemRanking["before"].sort(reverse=True)
    itemRanking["equal"].sort(reverse=True)

    itemRanking["after"] = dict([ (item, itemScore) for itemScore,item in itemRanking["after"] ])
    itemRanking["before"] = dict([ (item, itemScore) for itemScore,item in itemRanking["before"] ])
    itemRanking["equal"] = dict([ (item, itemScore) for itemScore,item in itemRanking["equal"] ])

    return itemRanking

f = open("../movielens_1m_keyValueNodes.json","r")
keyValueNodes = json.loads(f.read())
f.close()

f = open("../movielens_1m_userData_trainset.json","r")
userSequenceTrain = {}
for line in f:
    userSequenceTrain.update(json.loads(line))
f.close()

f = open("../movielens_1m_userData_testset.json","r")
userSequenceTest = {}
for line in f:
    userSequenceTest.update(json.loads(line))
f.close()

f = open("../movielens_1m_userProfiles_afterNorming.json","r")
userProfileAfter = {}
for line in f:
    userProfileAfter.update(json.loads(line))
f.close()

f = open("../movielens_1m_userProfiles_beforeNorming.json","r")
userProfileBefore = {}
for line in f:
    userProfileBefore.update(json.loads(line))
f.close()

userWeights = {}
userWeights["before"] = userProfileBefore[uid]["weights"]
userWeights["after"] = userProfileAfter[uid]["weights"]


itemSequence = [ itemid for itemid,rating in userSequenceTrain[uid]]
dbFileName = "movielens_1m"

itemRanking = egocentricRecommendation(keyValueNodes, itemSequence, dbFileName, uid, userWeights)
#testData = [ itemid for itemid, rating in userSequenceTest[uid]]

#upto = 100
userTestData = dict(userSequenceTest[uid])

#print "reco after :"
#print itemRanking["after"][:upto]
'''
print "score of testData in itemRanking[\"after\"]"
print [ (itemid, itemRanking["after"][itemid]) for itemid, rating in userSequenceTest[uid]]

print "score of testData in itemRanking[\"befor\"]"
print [ (itemid, itemRanking["before"][itemid]) for itemid, rating in userSequenceTest[uid]]

print "score of testData in itemRanking[\"equal\"]"
print [ (itemid, itemRanking["equal"][itemid]) for itemid, rating in userSequenceTest[uid]]
'''

print "score of testData: "
a = [ (float(userTestData[itemid]), itemid, itemRanking["after"][itemid], itemRanking["before"][itemid], itemRanking["equal"][itemid]) for itemid, rating in userSequenceTest[uid]]
a.sort()
for i in a:
    print i

'''
print "index of testData in itemRanking[\"after\"]"
indexRanking = [itemRanking["after"].index(itemid) for itemid in testData]
indexRanking.sort()
print indexRanking, sum(indexRanking)

print "index of testData in itemRanking[\"before\"]"
indexRanking = [itemRanking["before"].index(itemid) for itemid in testData]
indexRanking.sort()
print indexRanking, sum(indexRanking)

print "index of testData in itemRanking[\"equal\"]"
indexRanking = [itemRanking["equal"].index(itemid) for itemid in testData]
indexRanking.sort()
print indexRanking, sum(indexRanking)
'''

"""
print "Intersection of reco after and testData:"
print set(itemRanking["after"][:upto]).intersection(testData[:])

print "reco before :"
print itemRanking["before"][:upto]

print "reco equal :"
print itemRanking["equal"][:upto]
"""