import json
import sys
import fileinput
import itertools
import numpy
import random

dbFileName = sys.argv[1]

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

def clusterUsers(JSONdb):
    f = open(JSONdb+"_userSimilarity.json","r")
    userSimilarity = json.loads(f.read())
    f.close()

    values = []
    userList = userSimilarity.keys()
    userPairs = itertools.combinations(userList,2)
    for user1,user2 in userPairs:
        values.append(getSimilarity(user1,user2,userSimilarity))

    k = numpy.average(values)
    k = k + 0.002
    # print k
    
    userList = random.sample(userList,len(userList))
    userClusterDict = {}
    for user in userList:
        userClusterDict[user] = [user]
    userPairs = itertools.permutations(userList,2)
    total = len(userList) * (len(userList)-1)
    count = 0
    for pair in userPairs:
        count += 1
        #print count*1.0/total
        if getSimilarity(pair[0],pair[1],userSimilarity) > k:
            userClusterDict[pair[0]].append(pair[1])
    userClusters = userClusterDict.values()
    for i in range(0,len(userClusters)):
        userClusters[i].sort()
    userClusters.sort()
    userClusters = list(userClusters for userClusters,_ in itertools.groupby(userClusters))

    f = open(JSONdb+"_clusteredUsers.json","w")
    f.write(json.dumps(userClusters))
    f.close()

clusterUsers(dbFileName)