import json
import sys
import fileinput
import itertools
import operator
import numpy 

dbFileName = sys.argv[1]
userID = sys.argv[2]
alpha = float(sys.argv[3])
def getSimilarity(user1, user2, userSimilarity):
    try :
        n1 = userSimilarity[user1][user2][0]
    except :
        n1 = 0
    try :
        n2 = userSimilarity[user2][user1][0]
    except :
        n2 = 0
    try :
        d1 = userSimilarity[user1][user2][1]
    except :
        d1 = 0
    try :
        d2 = userSimilarity[user2][user1][1]
    except :
        d2 = 0
    return (n1+n2)/(d1+d2)

def egocentricRecommendation(testDataItems, userWeights, keyValueNodes):
    score = {}
    for node in testDataItems:
        score[node] = []

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
                    score[item].append( [ (1 / userWeights[attrib][value][0])**2 * (1 / userWeights[attrib]["@RAI"])**2, numpy.average([float(rating) for rating in userWeights[attrib][value][1]])] )
                except KeyError:
                    pass
    for item in testDataItemDetails:
        score[item] = sum([weight*rating for weight, rating in score[item]]) / sum([weight for weight, rating in score[item]])
    return score
    
def collaborativeRecommend(uid, clusters, userSequenceTrain, testDataItems, userSimilarity):
    '''
    '''
    testDataScore = {}
    score = {}
    for item  in testDataItems:
        testDataScore[item] = {}
        testDataScore[item]["rating"]=[]
        testDataScore[item]["similarity"]=[]
    
    userSequenceTrainDict = {}
    for uid in userSequenceTrain:
        userSequenceTrainDict[uid] =  dict(userSequenceTrain[uid])

    clustersUID = [cluster for cluster in clusters if uid in cluster]
    for cluster in clustersUID :
        cluster.remove(uid)
        for user in cluster :
            intersectSet = set(userSequenceTrainDict.keys()).intersection(set(testDataItems))
            for item in intersectSet:
                try:
                    testDataScore[item]["rating"].append(int(userSequenceTrainDict[user][item]))
                    testDataScore[item]["similarity"].append(getSimilarity(uid,user,userSimilarity))
                except KeyError:
                    pass

    for item  in testDataItems:
        try :
            score[item]= sum(numpy.array(testDataScore[item]["rating"])*numpy.array(testDataScore[item]["similarity"]))/(sum(numpy.array(testDataScore[item]["similarity"])))
        except :
            score[item] = 0
    return score

def combineLists(alpha, itemRankingEgo, itemRankingColl):
    comboList = {}
    for item in itemRankingEgo.keys():
        if itemRankingColl[item] != 0 :
            comboList[item] = itemRankingEgo[item]*(alpha) + itemRankingColl[item]*(1-alpha)
        if itemRankingColl[item] == 0 :
            comboList[item] = itemRankingEgo[item]
    return comboList

f = open(dbFileName +"_keyValueNodes.json","r")
keyValueNodes = json.loads(f.read())
f.close()

f = open(dbFileName +"_userData_trainset.json","r")
userSequenceTrain = {}
for line in f:
    userSequenceTrain.update(json.loads(line))
f.close()

f = open(dbFileName,"r")
items = []
f.readline()
for line in f:
    items.append(str(json.loads(line)["id"][0]))
f.close()

for i in userSequenceTrain[userID]:
    items.remove(str(i[0]))

f = open(dbFileName +"_normalizedUserProfiles.json","r")
userProfile = {}
for line in f:
    userProfile.update(json.loads(line))
f.close()


f = open(dbFileName+"_clusteredUsers.json","r")
clusters = json.loads(f.read())
f.close()

f = open(dbFileName+"_userSimilarity.json","r")
userSimilarity = json.loads(f.read())
f.close()

userWeights = userProfile[userID]["weights"]
scoreEgo = egocentricRecommendation(items, userWeights, keyValueNodes)
scoreCol = collaborativeRecommend(userID, clusters, userSequenceTrain, items, userSimilarity)
scoreCombined = combineLists(alpha, scoreEgo, scoreCol)


scoreEgo = sorted(scoreEgo.iteritems(), key=operator.itemgetter(1), reverse=True)
f = open(dbFileName +"_egocentricReco.json","w")
for movie,rating in scoreEgo:
    f.write(str(movie) + " " + str(rating) + "\n")
f.close()

scoreCol = sorted(scoreCol.iteritems(), key=operator.itemgetter(1), reverse=True)
f = open(dbFileName +"_collaborativeReco.json","w")
for movie,rating in scoreCol:
    f.write(str(movie) + " " + str(rating) + "\n")
f.close()

scoreCombined = sorted(scoreCombined.iteritems(), key=operator.itemgetter(1), reverse=True)
f = open(dbFileName +"_combinedReco.json","w")
for movie,rating in scoreCombined:
    f.write(str(movie) + " " + str(rating) + "\n")
f.close()
