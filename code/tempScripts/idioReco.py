import sys
import json

uid = sys.argv[1]

def egocentricRecommendation(keyValueNodes, userSequence, dbFileName, uid, userWeights, testNodes):
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
        score["after"][node] = []
        score["before"][node] = []
        score["equal"][node] = []

    nodeImpact = {}
    nodeImpact["after"] = {}
    nodeImpact["before"] = {}
    nodeImpact["equal"] = {}

    for node in nodes:
        nodeImpact["after"][node] = 0
        nodeImpact["before"][node] = 0

    userSequenceRating = dict(userSequence)

    '''
    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            if value in userWeights["after"][key]:
                for userNode in userSequenceRating:
                    if userNode in keyValueNodes[key][value]:
                        for node in keyValueNodes[key][value]:
                            score["after"][node] += userWeights["after"][key][value] * userWeights["after"][key]["@RAI"] * float(userSequenceRating[userNode])
                            score["before"][node] += userWeights["before"][key][value] * userWeights["before"][key]["@RAI"] * float(userSequenceRating[userNode])
                            score["equal"][node] += equalWeight * float(userSequenceRating[userNode])

                            nodeImpact["after"][node] += userWeights["after"][key][value] * userWeights["after"][key]["@RAI"]
                            nodeImpact["before"][node] += userWeights["before"][key][value] * userWeights["before"][key]["@RAI"]
    '''

    impact = {}
    impact["after"] = {}
    impact["before"] = {}
    impact["equal"] = {}

    for userNode in userSequenceRating:
        impact["after"][userNode] = {}
        impact["before"][userNode] = {}
        impact["equal"][userNode] = {}

    numOfRatings = float(len(userSequenceRating))
    freqOfRating = {}
    ratings = userSequenceRating.values()
    for rating in ratings:
        try:
            freqOfRating[rating] += 1
        except KeyError:
            freqOfRating[rating] = 1
    relFreqOfRating = {rating: freqOfRating[rating] / numOfRatings for rating in ratings}

    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            if value in userWeights["after"][key]:
                for userNode in userSequenceRating:
                    if userNode in keyValueNodes[key][value]:
                        for node in keyValueNodes[key][value]:
                            try:
                                impact["after"][userNode][node] += userWeights["after"][key][value] * userWeights["after"][key]["@RAI"]
                                impact["before"][userNode][node] += userWeights["before"][key][value] * userWeights["before"][key]["@RAI"]
                            except KeyError:
                                impact["after"][userNode][node] = userWeights["after"][key][value] * userWeights["after"][key]["@RAI"]
                                impact["before"][userNode][node] = userWeights["before"][key][value] * userWeights["before"][key]["@RAI"]

                            if userNode == '260' and node == '274':
                                print "key:", key
                                print "value:", value
                                print "RAI for the key:", userWeights["after"][key]["@RAI"], userWeights["before"][key]["@RAI"]
                                print "weight for the key:", userWeights["after"][key][value], userWeights["before"][key][value]
                                print "product: ", userWeights["after"][key][value] * userWeights["after"][key]["@RAI"], userWeights["before"][key][value] * userWeights["before"][key]["@RAI"]
                                print "accumulated so far:", impact["after"][userNode][node], impact["before"][userNode][node]
                                raw_input("dbg1\n")



    for category in impact:
        for userNode in impact[category]:
            for node in impact[category][userNode]:
                score[category][node].append((float(userSequenceRating[userNode]), userNode, impact[category][userNode][node]))

    for node in nodes:
        if node in testNodes:
            print node
            score["after"][node].sort()
            score["before"][node].sort()

            r = score["after"][node][0][0]
            count = 0
            s = 0
            for entry in score["after"][node]:
                if r != entry[0]:
                    print s / count, relFreqOfRating[str(int(r))], s / count * relFreqOfRating[str(int(r))]
                    r = entry[0]
                    count = 0
                    s = 0
                else:
                    s += entry[2]
                    count += 1
                print entry
            print s / count, relFreqOfRating[str(int(r))], s / count * relFreqOfRating[str(int(r))]
            print ""
            sumOfWeights = sum([weight for rating, userNode, weight in score["after"][node]])
            avrg = sum([weight*rating for rating, userNode, weight in score["after"][node]]) / sumOfWeights
            #print avrg
            #raw_input()

    for node in nodes:
        score["after"][node] = sum([weight*rating for rating, userNode, weight in score["after"][node]]) / sum([weight for rating, userNode, weight in score["after"][node]])
        score["before"][node] = sum([weight*rating for rating, userNode, weight in score["before"][node]]) / sum([weight for rating, userNode, weight in score["before"][node]])

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

    itemRanking["after"] = dict([ (item, itemScore) for itemScore,item in itemRanking["after"] ])
    itemRanking["before"] = dict([ (item, itemScore) for itemScore,item in itemRanking["before"] ])
    itemRanking["equal"] = dict([ (item, itemScore) for itemScore,item in itemRanking["equal"] ])

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

itemRanking = egocentricRecommendation(keyValueNodes, itemSequence, dbFileName, uid, userWeights, [item for item, rating in userSequenceTest[uid]])
#testData = [ itemid for itemid, rating in userSequenceTest[uid]]

#upto = 20
userTestData = dict(userSequenceTest[uid])

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