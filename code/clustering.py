import pickle
import random
import copy
import itertools
import numpy
import json 

def getSimilarity(user1, user2):
    global userSimilarity
    try :
        n1 = userSimilarity[user1][user2]["numerator"]
    except :
        n1 = 0
    try :
        n2 = userSimilarity[user2][user1]["numerator"]
    except :
        n2 = 0
    try :
        d1 = userSimilarity[user1][user2]["denominator"]
    except :
        d1 = 0
    try :
        d2 = userSimilarity[user2][user1]["denominator"]
    except :
        d2 = 0
    return (n1+n2)/(d1+d2)

def formClusters(k):
    userList = userSimilarity.keys()
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
        if getSimilarity(pair[0],pair[1]) > k:
            userClusterDict[pair[0]].append(pair[1])
    userClusters = userClusterDict.values()
    for i in range(0,len(userClusters)):
        userClusters[i].sort()
    userClusters.sort()
    userClusters = list(userClusters for userClusters,_ in itertools.groupby(userClusters))
    return userClusters


def main():
    f = open("movielens_1m_userSimilarity.json","r")
    global userSimilarity
    userSimilarity = json.loads(f.read())

    values = []
    userList = userSimilarity.keys()
    userPairs = itertools.combinations(userList,2)
    for user1,user2 in userPairs:
        values.append(getSimilarity(user1,user2))

    k = numpy.average(values)
    k = k + 0.002
    # print k
    clusters = formClusters(k)
    f = open("clusters","w")
    f.write(json.dumps(clusters))
    f.close()
    # print len(clusters)
    # print len(clusters[0])
    # print len(clusters[100])
    # print len(clusters[-2])

    """
        singleNodeCluster = [cluster[0] for cluster in userClusters if len(cluster)==1]
        for cluster in userClusters:
            if len(cluster)!=1:
                for i in range(len(singleNodeCluster)):
                    if singleNodeCluster[i] in cluster:
                        singleNodeCluster[i] = 0
    """

#main()