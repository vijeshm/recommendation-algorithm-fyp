import sys
import json
import numpy
import math
import random

numOfUsers = int(sys.argv[1])

def egocentricRecommendation(keyValueNodes, dbFileName, uid, userWeights, testDataItems):
    '''
    graphDb (networkx Graph object): The database containing the relation between items in a graphical form
    userSequence (list) : the sequence in which the user has been associated with items
    This function applies our content based filtering algorithm to generate a score ranging from 0-1 for every item. This object will be written to contentReco.pickle as a pickle object. This pickle object is a dictionary with uid and score as the key and value respectively.
    '''

    score = {}
    score["after"] = {}
    score["before"] = {}
    score["equal"] = {}
    equalWeight = 1.0 / len(userWeights["after"])

    for node in testDataItems:
        score["after"][node] = []
        score["before"][node] = []
        score["equal"][node] = []

    testDataItemDetails = {}
    for item in testDataItems:
        testDataItemDetails[item] = {}

    for key in keyValueNodes:
        for value in keyValueNodes[key]:
            for item in keyValueNodes[key][value]:
                if item in testDataItems:
                    try:
                        testDataItemDetails[item][key].append(value)
                    except KeyError:
                        testDataItemDetails[item][key] = [value]

    for item in testDataItemDetails:
        for attrib in testDataItemDetails[item]:
            for value in testDataItemDetails[item][attrib]:
                try:
                    score["after"][item].append( [ (1 / userWeights["after"][attrib][value][0])**2 * (1 / userWeights["after"][attrib]["@RAI"])**2, numpy.average([float(rating) for rating in userWeights["after"][attrib][value][1]])] )
                    score["before"][item].append( [ (1 / userWeights["before"][attrib][value][0])**2 * (1 / userWeights["before"][attrib]["@RAI"])**2, numpy.average([float(rating) for rating in userWeights["after"][attrib][value][1]])] )

                    score["equal"][item].append([1, numpy.median([float(rating) for rating in userWeights["after"][attrib][value][1]])])
                except KeyError:
                    pass

    for item in testDataItemDetails:
        score["after"][item] = sum([weight*rating for weight, rating in score["after"][item]]) / sum([weight for weight, rating in score["after"][item]])
        score["before"][item] = sum([weight*rating for weight ,rating in score["before"][item]]) / sum([weight for weight, rating in score["before"][item]])
        score["equal"][item] = sum([weight*rating for weight ,rating in score["equal"][item]]) / sum([weight for weight, rating in score["equal"][item]])
    return score

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

print userProfileAfter.keys()
print numOfUsers
users = random.sample(userProfileAfter.keys(), numOfUsers)
error = []

count = 0
for uid in users:
    print count, uid
    count += 1
    userWeights = {}
    userWeights["before"] = userProfileBefore[uid]["weights"]
    userWeights["after"] = userProfileAfter[uid]["weights"]

    itemSequence = [ itemid for itemid,rating in userSequenceTrain[uid]]
    dbFileName = "movielens_1m"

    itemRanking = egocentricRecommendation(keyValueNodes, dbFileName, uid, userWeights, [item for item, rating in userSequenceTest[uid]])
    #testData = [ itemid for itemid, rating in userSequenceTest[uid]]

    userTestData = dict(userSequenceTest[uid])
    results = [ (float(userTestData[itemid]), itemid, numpy.round(itemRanking["after"][itemid]), itemRanking["before"][itemid], itemRanking["equal"][itemid]) for itemid, rating in userSequenceTest[uid]]
    results.sort()
    for result in results:
        #print result[0], result[2]
        error.append((result[0] - result[2])**2)

error = math.sqrt(sum(error) / len(error))
print error