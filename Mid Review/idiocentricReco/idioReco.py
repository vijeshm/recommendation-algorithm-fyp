import sys
import json

uid = sys.argv[1]

def egocentricRecommendation(keyValueNodes, userSequence, dbFileName, uid, userWeights):
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

    userSequenceRating = dict(userSequence)

    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            for userNode in userSequenceRating:
                if userNode in keyValueNodes[key][value]:
                    for node in keyValueNodes[key][value]:
                        score["after"][node] += userWeights["after"][key] * float(userSequenceRating[userNode])
                        score["before"][node] += userWeights["before"][key] * float(userSequenceRating[userNode])
                        score["equal"][node] += equalWeight * float(userSequenceRating[userNode])

    for item, rating in userSequence:
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

    itemRanking["after"] = [ item for itemScore,item in itemRanking["after"] ]
    itemRanking["before"] = [ item for itemScore,item in itemRanking["before"] ]
    itemRanking["equal"] = [ item for itemScore,item in itemRanking["equal"] ]

    return itemRanking

f = open("../../code/movielens_1m_keyValueNodes.json","r")
keyValueNodes = json.loads(f.read())
f.close()

f = open("../../code/movielens_1m_userData_trainset.json","r")
userSequenceTrain = {}
for line in f:
    userSequenceTrain.update(json.loads(line))
f.close()

f = open("../../code/movielens_1m_userData_testset.json","r")
userSequenceTest = {}
for line in f:
    userSequenceTest.update(json.loads(line))
f.close()

f = open("../../code/movielens_1m_userProfiles_afterNorming.json","r")
userProfileAfter = {}
for line in f:
    userProfileAfter.update(json.loads(line))
f.close()

f = open("../../code/movielens_1m_userProfiles_beforeNorming.json","r")
userProfileBefore = {}
for line in f:
    userProfileBefore.update(json.loads(line))
f.close()

userWeights = {}
userWeights["before"] = userProfileBefore[uid]["weights"]
userWeights["after"] = userProfileAfter[uid]["weights"]


#itemSequence = [ itemid for itemid,rating in userSequenceTrain[uid]]
itemSequence = userSequenceTrain[uid]
dbFileName = "movielens_1m"

itemRanking = egocentricRecommendation(keyValueNodes, itemSequence, dbFileName, uid, userWeights)
testData = [ itemid for itemid, rating in userSequenceTest[uid]]

upto = 20
'''
print "test data :"
print testData[:]
'''
print "Recommendation before Range Based Norming:"
print itemRanking["before"][:upto]

print "Recommendation after Range Based Norming:"
print itemRanking["after"][:upto]

print "Recommendation assuming equal weights:"
print itemRanking["equal"][:upto]


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