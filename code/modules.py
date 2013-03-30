#!/usr/bin/python
# Program to build a generic recommender
# Time: 
# Date: 
# Todo:

# Python standard libraries
import pickle
import string
import random
import json
import copy
import matplotlib.pyplot as plt
import pylab as pl
import time
import re
import sys
import numpy
import itertools
from multiprocessing import Process, Queue, Pool
import fileinput
import gc
from scipy.cluster.vq import kmeans2

# Third party libraries
import networkx as nx
    
def learnGraph(JSONdb, edgeList=False):
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
        #print uid

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
                    #print attrs
                    #print attribute
                    attributeAndNodes[attrs][attribute] = [uid]


    enumAttr = dict([ (attr, "@"+str(enum)) for enum, attr in list(enumerate(attributeAndNodes.keys())) ])
    enumValues = {}
    for attr in attributeAndNodes:
        if typeInfo[attr] == "string" and attr !="id" : 
            #we enumerate only those attributes which takes string values.
            enumValues[attr] = dict([ (attribute, "#"+str(enum)) for enum, attribute in list(enumerate(attributeAndNodes[attr].keys())) ])

    enum = {}
    enum["attrs"] = enumAttr
    enum["values"] = enumValues

    '''
    print "generating graph.."
    G = nx.Graph()
    for attrs in attributeAndNodes:
        if attrs != "id":
            if typeInfo[attrs] == "string" or typeInfo[attrs] == "bool":            
                for attribute in attributeAndNodes[attrs]:
                    edgeGen =  list(itertools.combinations(attributeAndNodes[attrs][attribute],2))+[(uid,uid) for uid in attributeAndNodes[attrs][attribute]]
                    for edge in edgeGen :
                        G.add_edge(edge[0],edge[1])
                        if G[edge[0]][edge[1]].has_key(enum["attrs"][attrs]):
                            G[edge[0]][edge[1]][enum["attrs"][attrs]].append(enum["values"][attrs][attribute])
                        else :
                            G[edge[0]][edge[1]][enum["attrs"][attrs]]=[enum["values"][attrs][attribute]]
            else:
                for attribute in attributeAndNodes[attrs]:
                    edgeGen =  list(itertools.combinations(attributeAndNodes[attrs][attribute],2))+[(uid,uid) for uid in attributeAndNodes[attrs][attribute]]
                    for edge in edgeGen:
                        G.add_edge(edge[0],edge[1])
                        if G[edge[0]][edge[1]].has_key(attrs):
                           G[edge[0]][edge[1]][attrs].append(attribute)
                        else:
                           G[edge[0]][edge[1]][attrs]=[attribute]
    print "done generating graph.."
    '''

    print "writing " + JSONdb + "_keyValueNodes.json"
    f = open(JSONdb + "_keyValueNodes.json", "w")
    f.write(json.dumps(attributeAndNodes))
    f.close()
    print "done writing " + JSONdb + "_keyValueNodes.json"

    print "writing " + JSONdb + "_enumeration.json"
    f = open(JSONdb + "_enumeration.json", "w")
    f.write(json.dumps(enum))
    f.close()
    print "done writing " + JSONdb + "_enumeration.json"

    if edgeList:
        print "writing " + JSONdb + "_GraphDB.edgelist"
        fout = open(JSONdb + "_GraphDB.edgelist", "w")
        for node in G.nodes():
            for key in G[node]:
                fout.write(node + " " + key + " " + str(G[node][key]) + "\n")
        fout.close()
        print "done writing " + JSONdb + "_GraphDB.edgelist"

    #nx.write_edgelist(G, JSONdb + "_GraphDB.edgelist")
    #write the object onto a pickle file
    #fp = open(JSONdb + "_GraphDB.pickle", "w")
    #print "creating pickle string"
    #pickleStr = pickle.dumps(G)
    #print "writing to file"
    #fp.write(pickleStr)
    #fp.close()

def egocentricRecommendation(graphDb, userSequence, dbFileName, uid):
    '''
    graphDb (networkx Graph object): The database containing the relation between items in a graphical form
    userSequence (list) : the sequence in which the user has been associated with items
    This function applies our content based filtering algorithm to generate a score ranging from 0-1 for every item. This object will be written to contentReco.pickle as a pickle object. This pickle object is a dictionary with uid and score as the key and value respectively.
    '''

    #set the initial score for all the nodes to be zero.
    for node in graphDb.nodes():
        graphDb[node]["score"] = 0

    #for every node in the userSequence, increment the neighbor's score for every common attribute. (The increment can also take place in a weight manner)
    sequenceNames = []
    for node, rating in userSequence:
        sequenceNames.append(graphDb[node]["title"][0])
        neighbors = getRealNeighbors(graphDb.neighbors(node))

        for neighbor in neighbors:
            for assoc in graphDb[node][neighbor]:
                graphDb[neighbor]["score"] += 1 #Note: This is not weighted increment.
    #print "user sequence: ", sequenceNames

    #normalizing the scores - divide by the largest score
    weights = [graphDb[node]["score"] for node in graphDb.nodes()]
    #maxWeight = float(max(weights))
    sumOfWeights = float(sum(weights))

    for node in graphDb.nodes():
        #graphDb[node]["score"] = graphDb[node]["score"] / maxWeight
        graphDb[node]["score"] = graphDb[node]["score"] / sumOfWeights

    #create a dictionary with key and value as node and score respectively
    reco = {}
    for node in graphDb.nodes():
        reco[node] = graphDb[node]["score"]

    #write this object onto a pickle file
    fp = open(dbFileName + "_" + str(uid) + "_contentReco.pickle", "w")
    fp.write(pickle.dumps(reco))
    fp.close()

    #print "written to file", dbFileName + "_" + str(uid) + "_contentReco.pickle"
    #raw_input()

def buildUserSimilarityDict(G, userSequence, userProfiles, dbFileName, upperlim):
    '''
    G (networkx object): The Graph of items
    userSequence (dictionary) : dictionary of users, with their movie watching sequences
    userProfiles (dictionary) : dictionary of users, with their alpha and relative weights for various attributes
    This function builds a user similarity matrix. The matrix is being simulated using a dictionary. Each entry in the matrix is a tuple, a numerator and a denominator. The ratio gives the similarity.
    '''
    userSimilarity = {}

    users = userSequence.keys()
    users.sort()

    #users = users[:upperlim]
    totalUsers = len(users)*(len(users) - 1)/2

    count = 0
    #for i in [str(elem) for elem in range(1, len(users) + 1)]:
    for i in users:
        userSimilarity[i] = {}
        useriItems = set([movie for movie,rating in userSequence[i]])

        for j in users[users.index(i):]:
        #for j in [str(elem) for elem in range(int(i), len(users))]:
            count += 1
            userjItems = set([movie for movie, rating in userSequence[j]])

            #get the intersecting items from both the users and find the induced subgraph
            intersectingItems = list(useriItems.intersection(userjItems))
            intersectingSubgraph = getSubgraph(G, intersectingItems)

            #find all the attributes of all the edges
            attribs = []
            #print getEdges(intersectingSubgraph)
            #raw_input("dbg2")
            for edge in getEdges(intersectingSubgraph):
                #print edge
                #raw_input()
                #print intersectingSubgraph[edge[0]]
                #raw_input()
                #print intersectingSubgraph[edge[0]][edge[1]]
                #raw_input()
                attribs.extend(intersectingSubgraph[edge[0]][edge[1]].keys())
            #print attribs

            #to determine numerator, iterate through all the attributes and add up the relative weights of individual users.
            numerator = 0.0
            #print set(attribs)
            #raw_input("dbg1")

            relFreqOfAttrib = {}
            total = float(len(attribs))
            for attrib in attribs:
                if not relFreqOfAttrib.has_key(attrib):
                    relFreqOfAttrib[attrib] = attribs.count(attrib)

            #print relFreqOfAttrib
            #raw_input("db9")

            for attrib in relFreqOfAttrib:
                useri = 0.0
                #print userProfiles[i]['weights']
                if userProfiles[i]['weights'].has_key(attrib):
                    useri = userProfiles[i]['weights'][attrib]
                #print useri
                #raw_input("dbg2")

                userj = 0.0
                if userProfiles[j]['weights'].has_key(attrib):
                    userj = userProfiles[j]['weights'][attrib]
                #print userj
                #raw_input("dbg3")

                numerator += (useri + userj)*relFreqOfAttrib[attrib]
                #print numerator
                #raw_input("dbg8")

            #get the union of items from both the users and find the induced subgraph
            unionItems = list(useriItems.union(userjItems))
            unionSubgraph = getSubgraph(G, unionItems)

            #find all the attributes of all the edges
            attribs = []
            for edge in getEdges(unionSubgraph):
                attribs.extend(unionSubgraph[edge[0]][edge[1]].keys())

            #to determine denominator, iterate through all the attributes and add up the relative weights of individual users.
            denominator = 0.0

            relFreqOfAttrib = {}
            total = float(len(attribs))
            for attrib in attribs:
                if not relFreqOfAttrib.has_key(attrib):
                    relFreqOfAttrib[attrib] = attribs.count(attrib)

            #print relFreqOfAttrib
            #raw_input("dbg10")


            for attrib in relFreqOfAttrib:
                useri = 0.0
                if userProfiles[i]['weights'].has_key(attrib):
                    useri = userProfiles[i]['weights'][attrib]
                #print useri
                #raw_input("dbg11")

                userj = 0.0
                if userProfiles[j]['weights'].has_key(attrib):
                    userj = userProfiles[j]['weights'][attrib]
                #print userj
                #raw_input("dbg12")

                denominator += (useri + userj)*relFreqOfAttrib[attrib]
                #print denominator
                #raw_input("dbg13")

            userSimilarity[i][j] = [numerator, denominator]

            #print i, useriItems, "\n"
            #rint j, userjItems, "\n"
            #print "\nintersecting Items", intersectingItems
            #print len(intersectingItems)
            #print "\nunion Items", unionItems
            #print len(unionItems)
            print float(count)/totalUsers, i, j, numerator, denominator, numerator/denominator
            #raw_input()

    f = open(dbFileName + "_userSimilarity.pickle", "w")
    f.write(pickle.dumps(userSimilarity))
    f.close()

def getSimilarity(userSimilarity, user1, user2):
    if userSimilarity[user1].has_key(user2):
        return userSimilarity[user1][user2][0] / userSimilarity[user1][user2][1]
    else:
        return userSimilarity[user2][user1][0] / userSimilarity[user2][user1][1]

def formClustersFn(userSimilarity, threshold, dbFileName):
    #clusters = []
    clusters = userSimilarity.keys()
    after_cluster = []
    
    total = float(len(clusters)*( len(clusters) + 1) / 2)
    count = 0

    for x in range(len(clusters)):
        tic = [ [clusters[x]] ]
        for y in clusters[x+1:]:
            count += 1
            i = 0
            print clusters[x], y, count / total, "tic:" + str(len(tic))
            while i<len(tic) and getSimilarity(userSimilarity, clusters[x], y) >= threshold:
                toc = [y]
                for j in tic[i]:
                    if getSimilarity(userSimilarity, j, y) >= threshold :
                        toc.append(j)

                if toc[1:] == tic[i]:
                    tic[i].append(y)
                    i = i+1

                elif toc not in tic:
                    tic.insert(i+1, toc)
                    i = i+2
                    
                else:
                    i = i+1

        for i in tic:
            if len(i) != 1:
                i.sort()
                if i not in after_cluster:
                    after_cluster.append(i)

    after_cluster.sort()
    after_cluster_final = []

    count = 0
    total = len(after_cluster) * (len(after_cluster) + 1) / 2.0
    for i in after_cluster:
        flag = False
        for j in after_cluster:
            count += 1
            print count / total
            if i!=j and set(i).issubset(set(j)):
                flag = True
                break

        if not flag:
            after_cluster_final.append(i)

    f = open(dbFileName + "_clusters.pickle", "w")
    f.write(pickle.dumps(after_cluster_final))
    f.close()

    '''
    users = userSimilarity.keys()

    singletons = []

    clusters = []
    for user in users:
        clusters.append(set([user]))

    print clusters

    for user in users:
        singletonFlag = True
        for i in range(len(clusters)):
            clusterMember = True
            #difference between similarity scores of any two members is less than threshold.
            for member1 in clusters[i]:
                for member2 in clusters[i]:
                    if( abs(getSimilarity(userSimilarity, user, member1) - getSimilarity(userSimilarity, user, member2) ) > threshold ):
                        clusterMember = False
            if(clusterMember):
                clusters[i].add(user)
                singletonFlag = False

        if(singletonFlag):
            singletons.append(set([user]))
        #print clusters
        #raw_input()

    #clean all singletons
    temp = []
    for cluster in clusters:
        if len(cluster) != 1:
            temp.append(cluster)
    clusters = temp

    clusters.extend(singletons)

    temp = []
    for cluster in clusters:
        if clusters.count(cluster) == 1:
            temp.append(cluster)
    clusters = temp
    
    for cluster in clusters:
        print cluster
    '''

    f = open("clusters.pickle", "w")
    f.write(pickle.dumps(clusters))
    f.close()

def collaborativeRecommend(uid, G, clusters, userSequence, userSimilarity, dbFileName):
    for node in G.nodes():
        G[node]["score"] = 0.0

    k = int(0.2 * len(userSimilarity))
    sims = [(sim, user) for (user, sim) in userSimilarity[uid].items()]
    sims.sort(reverse=True)
    for sim, user in sims[:k]:
        for items in userSequence[user]:
            if (uid != user):
                G[items[0]]["score"] += getSimilarity(userSimilarity, uid, user)
                
    #maxWeight = float(max([G[node]["score"] for node in G.nodes()]))
    sumOfWeights = float(sum([G[node]["score"] for node in G.nodes()]))

    reco = {}
    for node in G.nodes():
        reco[node] = G[node]["score"] / sumOfWeights
        '''
        if maxWeight != 0:
            reco[node] = G[node]["score"] / maxWeight
        else:
            reco[node] = 0.0
        '''


    '''
    for cluster in clusters:
        #print cluster
        #raw_input()
        if uid in cluster:
            #print uid
            raw_input("it exists")

            for user in cluster:
                #print userSequence[user]
                for items in userSequence[user]:
                    if (uid != user):
                        G[items[0]]["score"] += getSimilarity(userSimilarity, uid, user)
                        #print node, G[items[0]]["score"]
                        #raw_input()

    maxWeight = float(max([G[node]["score"] for node in G.nodes()]))

    reco = {}
    for node in G.nodes():
        if maxWeight != 0:
            reco[node] = G[node]["score"] / maxWeight
        else:
            reco[node] = 0.0
    '''

    fp = open(dbFileName + "_" + str(uid) + "_collabReco.pickle", "w")
    fp.write(pickle.dumps(reco))
    fp.close()

    #print "written to file ", dbFileName + "_" + str(uid) + "_collabReco.pickle"
    #raw_input()

def combineLists(G, alpha, uid, sequence, dbFileName):
    '''
    G (networkx graph object)
    alpha (float) - a number between 0 and 1.
    This function combines the both the generated lists of items into one composite list.
    '''

    #open both the files that contain the recommendations, combine them using the weighted average method, based in their scores rather than the ranks.
    fp = open(dbFileName + "_" + str(uid) + "_contentReco.pickle", "r")
    contentReco = pickle.loads(fp.read())
    fp.close()
    
    fp = open(dbFileName + "_" + str(uid) + "_collabReco.pickle", "r")
    collabReco = pickle.loads(fp.read())
    fp.close()

    combinedReco = {}
    items = contentReco.keys()

    for item in items:
        if item in sequence:
            combinedReco.pop(item)

    #score based weighted average
    for item in items:
        combinedReco[item] = alpha*contentReco[item] + (1 - alpha)*collabReco[item]

    '''
    ###########################################
    #rank(or index) based weighted average
    contentRecoRank = {}
    valueKey = [(value, key) for (key, value) in contentReco.items()]
    valueKey.sort(reverse = True)
    for i in range(len(valueKey)):
        contentRecoRank[valueKey[1]] = i

    collabRecoRank = {}
    valueKey = [(value, key) for (key, value) in collabReco.items()]
    valueKey.sort(reverse = True)
    for i in range(len(valueKey)):
        collabRecoRank[valueKey[1]] = i

    for uid in uids:
        combinedReco[uid] = alpha*contentReco[uid] + (1 - alpha)*collabReco[uid]    
    ###########################################
    '''

    #recos = [ (rate, item) for item,rate in combinedReco.items()]
    #recos.sort(reverse = True)
    #recos = [(G[item]["title"][0], rate) for rate,item in recos]
    #for reco in recos[:20]:
    #    print reco

    fp = open(dbFileName + "_" + str(uid) + "_combinedReco.pickle", "w")
    fp.write(pickle.dumps(combinedReco))
    fp.close()

    #print "written to file ", dbFileName + "_" + str(uid) + "_combinedReco.pickle"
    #raw_input()

def createUserData(graphDB, alpha, numberOfUsers, threshold, maxItems, dbFileName):
    '''
    graphDb (networkx Graph object) : The networkx graph object
    alpha (float) : the probability with which the user chooses a neighboring item
    numberOfUsers (integer) : self explanatory
    threshold (integer) : the minimum number of items that the user needs to associate with
    maxItems (integer) : the maximum number of items that the user needs to associate with
    This function creates user data set in the form of a pickle object. The object is a dictionary with the user as the key and a list as the value. UID identifies the user.
    '''

    userData = {}
    for i in range(numberOfUsers):
        # raw_input("press any key to continue..")
        userList = []
        userList.append( (random.choice(graphDB.nodes()), 1) ) #pick some random node as the starting point. To indicate that the user is associated with the item, we'll use the tuple (item, rating). To just indicate whether the user is associated or not (binary states), we'll use either (item, 0) or (item, 1).
        availableChoices = getRealNeighbors(graphDB.neighbors(userList[0][0]))
        while availableChoices == []:
            userList.append( ( random.choice( list( set(graphDB.nodes()).difference(set([item for item, rating in userList])) ) ), 1 ) ) #pick an item that the user is not associated with before and append to the user's list of associated items
            availableChoices = getRealNeighbors(graphDB.neighbors(userList[-1][0]))

        numberOfItems = random.choice(range(threshold, maxItems + 1)) #choose a random number between threshold and maxItems
        for j in range(numberOfItems): #throw a random number. if it is less than alpha, choose a random element from availableChoices List. If it is greater than alpha, pick a random node.
            if(random.random() < alpha):
                userList.append( ( random.choice(availableChoices), 1) )
            else:
                randomChoice = random.choice( list( set(graphDB.nodes()).difference(set([item for item, rating in userList])) ) )
                userList.append( (randomChoice, 1) )

            availableChoices = getRealNeighbors(graphDB.neighbors(userList[-1][0]))
            while availableChoices == []:
                userList.append( ( random.choice( list( set(graphDB.nodes()).difference(set([item for item, rating in userList])) ) ), 1 ) ) #pick an item that the user is not associated with before and append to the user's list of associated items
                availableChoices = getRealNeighbors(graphDB.neighbors(userList[-1][0]))
            
            availableChoices = list(set(availableChoices).difference(set(userList)))
            
        userData[i] = userList
        
    #write userData onto the file
    fp = open(dbFileName + "_userSequence.pickle", "w")
    fp.write(pickle.dumps(userData))
    fp.close()

def tweakAlpha(userProfile):
    """
        tweak alpha... [will be extended in future but currenlty NO changes are being made]
    """
    pass

def tweakWeights(keyValueNodes, userProfile, itemSequence):
    """
        G: Item Graph
        userProfile: A dictionary for individual users. It contains two keys, alpha and weights
        itemSequence: A list of tuples of the form (item, rating)
    """

    #get the list of items that the user is associated with
    items = set([item for item, rating in itemSequence])

    for attrib in keyValueNodes:
        for value in keyValueNodes[attrib]:
            numOfNodes = len(items.intersection(set(keyValueNodes[attrib][value])))
            try:
                userProfile["weights"][attrib] += numOfNodes * (numOfNodes - 1) / 2
            except KeyError:
                userProfile["weights"][attrib] = numOfNodes * (numOfNodes - 1) / 2
    
    '''
    #G.subgraph() function removes the attributes of the node. Since we do not want that to happen, I've written a function that does it. I couldnt figure out a networkx alternative which might be more efficient.
    H = G.subgraph(items)
    #get the relative weights of the user towards each attribute
    for node in H.nodes():
        neighbors = H.neighbors(node)
        neighbors.remove(node)
        for neighbor in neighbors: #scores must be updated from each individual neighbor. This would also mean that the weights would be added twice. But that wouldnt be a problem since we're normalizing it later on.
            #the weight for each attribute must be computed. Hence iterate through the edge attributes, find out the number of common attribute-value pairs for each attribute. If the userProfiles have been updated for the first time, initialize it with the formula. If the attribute has already been updated once, then increment the weights correspondingly.
            for attrib in H[node][neighbor]:
                numOfCommonAttribs = len(H[node][neighbor][attrib])
                if userProfile["weights"].has_key(attrib):
                    userProfile["weights"][attrib] += numOfCommonAttribs
                    #userProfile["weights"][attrib] += numOfCommonAttribs*(1.0/len(H[node][attrib]) + 1.0/len(H[neighbor][attrib]))
                else:
                    userProfile["weights"][attrib] = numOfCommonAttribs
                    #userProfile["weights"][attrib] = numOfCommonAttribs*(1.0/len(H[node][attrib]) + 1.0/len(H[neighbor][attrib]))
    '''

    #we still have to normalize the weights, which is done after the function returns

def getEdges(G):
    edges = G.edges()    
    temp = []
    for edge in edges:
        #if type(edge[0]) == int and type(edge[1]) == int:
        if edge[1].isdigit():
            temp.append(edge)
    #print temp
    #raw_input("dbg1")
    return temp

def clustersByKMeans(inp, numOfClusters):
    data = numpy.ndarray( (len(inp),1), buffer=numpy.array(inp), dtype=float)
    centroids, clusters = kmeans2(data, numOfClusters)

    retVal = {}
    for i in range(numOfClusters):
        retVal[i] = []

    for i in range(len(clusters)):
        retVal[clusters[i]].append(inp[i])

    retVal = retVal.values()
    return retVal

def optimumClusters(inp):
    numOfClusters = range(2, len(inp))

    n = len(inp)
    v = []
    for numOfCluster in numOfClusters:
        sys.stdout.write('\b'*10)
        sys.stdout.write(str(numOfCluster))

        mIntra = 0
        clusters = clustersByKMeans(inp, numOfCluster)
        clusters = [cluster for cluster in clusters if cluster != []]
        for cluster in clusters:
            centroid = numpy.average(cluster)
            for member in cluster:
                mIntra += pow(member - centroid, 2)
        mIntra /= n

        centroids = [numpy.average(cluster) for cluster in clusters]
        mInterList = []
        for i in range(len(centroids)):
            for j in range(i+1, len(centroids)):
                mInterList.append( pow(centroids[i] - centroids[j], 2) )
        mInter = min(mInterList)

        v.append((mIntra / mInter, numOfCluster))

    optimumNumber = min(v)[1]
    clusters = clustersByKMeans(inp, optimumNumber)
    clusters = [cluster for cluster in clusters if cluster != []]
    return clusters

def findRange(key, datatype, keyValueNodes, attribRange):
    if datatype[key] == "string" or datatype[key] == "bool":
        attribRange[key] = len(keyValueNodes[key])
        print key, datatype[key], attribRange[key]
    else:
        inp = [float(value) for value in keyValueNodes[key]]
        print key, datatype[key], len(inp)
        attribRange[key] = len(optimumClusters(inp))
        print "", attribRange[key]

def normalizeWeights(userProfiles, keyValueNodes, datatype):
    """
        userProfiles (dictionary) : contains userProfiles each containing 2 keys, alpha and weights
        keyValueNodes 
        Normalize the weights in the weight vector. We'll get the relative importance of each individual attribute is quantified
    """
    attribRange = {}
    pool = Pool(processes=4)
    for key in keyValueNodes:
        #pool.apply_async(findRange, [key, datatype, attribRange])
        findRange(key, datatype, keyValueNodes, attribRange)

    #compute the range of values for categorical and non-categorical attributes

    for profile in userProfiles:
        for attrib in userProfiles[profile]["weights"]:
            userProfiles[profile]["weights"][attrib] *= attribRange[attrib]

    for profile in userProfiles:
        sumOfWeights = float(sum(userProfiles[profile]["weights"].values()))
        for attr in userProfiles[profile]["weights"]:
            userProfiles[profile]["weights"][attr] /= sumOfWeights

def attributeRelativeImportance(dbFileName):
    """
        In order to determine the relative importance of each attribute, we take the average out the attribute's weight from the all the users.
    """
    f = open(dbFileName + "_userProfiles.pickle", "r")
    userProfiles = pickle.loads(f.read())
    f.close()
    
    '''
    pl.ion()
    fig = pl.figure()
    ax = fig.add_subplot(1,1,1)

    '''

    avg = {}
    for userProfile in userProfiles:
        for attr in userProfiles[userProfile]["weights"]:
            if avg.has_key(attr):
                avg[attr] += userProfiles[userProfile]["weights"][attr]
            else:
                avg[attr] = userProfiles[userProfile]["weights"][attr]

        x = []
        y = []
        sumOfWeights = sum(avg.values())
        for attr in avg:
            x.append(attr)
            y.append(avg[attr] / float(sumOfWeights))

        '''
        ax.clear()
        ax.plot(y)
        for i in range(len(y)):
            if y[i] > 0.025:
                ax.text(i, y[i], x[i])

        pl.draw()
        pl.savefig(dbFileName + "_itemDimensionalityReduction.png")
        #time.sleep(0.001)
        '''

    '''
    itemPairs = avg.items()
    x = [x1 for x1,y1 in itemPairs]
    y = [y1 for x1,y1 in itemPairs]
    
    for xcoord in range(len(y)):
        if y[xcoord] > 0.025:
            plt.text(xcoord, y[xcoord], x[xcoord])

    plt.plot(y)
    plt.show()
    '''

    f = open(dbFileName + "_attributeRelativeImportance.pickle", "w")
    f.write(pickle.dumps(avg))
    f.close()

#os.system("python modules.py --db=movielens --usageData=movielens_userData.json -userProfiles -reduceDimensions -userSimilarity=6040 -formClusters=0.8")

def readEdgeList(fileName):
    #This part of the code is NOT functional. It gives a memoryError. (no mem for new parser - who knows what it means?)
    G = nx.Graph()
    for line in fileinput.input(fileName):
        i = line.find(' ')
        j = line.find(' ',i+1)
        try :
          node1 = line[:i]
          node2 = line[i+1:j]
          Weight = eval(line[j+1:])
          G.add_edge(node1,node2,Weight)
        except :
          print line
          print "gone"
        del Weight
        del node1
        del node2
    return G

def constructGraph(keyValueNodes, enum, datatype):
    G = nx.Graph()
    for attrs in keyValueNodes:
        if attrs != "id":
            if datatype[attrs] == "string" or datatype[attrs] == "bool":            
                for attribute in keyValueNodes[attrs]:
                    edgeGen =  list(itertools.combinations(keyValueNodes[attrs][attribute],2))+[(uid,uid) for uid in keyValueNodes[attrs][attribute]]
                    for edge in edgeGen :
                        G.add_edge(edge[0],edge[1])
                        if G[edge[0]][edge[1]].has_key(enum["attrs"][attrs]):
                            G[edge[0]][edge[1]][enum["attrs"][attrs]].append(enum["values"][attrs][attribute])
                        else :
                            G[edge[0]][edge[1]][enum["attrs"][attrs]]=[enum["values"][attrs][attribute]]
            else:
                for attribute in keyValueNodes[attrs]:
                    edgeGen =  list(itertools.combinations(keyValueNodes[attrs][attribute],2))+[(uid,uid) for uid in keyValueNodes[attrs][attribute]]
                    for edge in edgeGen:
                        G.add_edge(edge[0],edge[1])
                        if G[edge[0]][edge[1]].has_key(attrs):
                           G[edge[0]][edge[1]][attrs].append(attribute)
                        else:
                           G[edge[0]][edge[1]][attrs]=[attribute]
    return G

def readTypeInfo(fileName):
    f = open(fileName, "r")
    datatype = json.loads(f.read())
    f.close()
    return datatype

def readKeyValueNodes(fileName):
    f = open(fileName, "r")
    keyValueNodes = json.loads(f.read())
    f.close()
    return keyValueNodes

def forwardMapping(JSONdb):
    f = open(JSONdb + "_enumeration.json", "r")
    enum = json.loads(f.read())
    f.close()
    return enum

def reverseMapping(JSONdb):
    f = open(JSONdb + "_enumeration.json", "r")
    enum = json.loads(f.read())
    reverseEnum = {}
    reverseEnum["attrs"] =  dict([(enum["attrs"][attrs],attrs) for attrs in enum["attrs"]])
    reverseEnum["values"] = {}
    for attr in enum["values"]:
        reverseEnum["values"][attr] = dict([(enum["values"][attr][attributes],attributes) for attributes in enum["values"][attr]])
    f.close()
    return reverseEnum

def mainImport(db=None, usageData=None, buildGraph=False, userProfiles=False, generateSequence=None, reduceDimensions=False, userSimilarity=None, formClusters=None, uid=None):
    dbFileName = ""
    if db:
        dbFileName = db
    else:
        print "please specify the database name"
        exit()

    userSequence = ""
    if usageData:
        userSequence = usageData
    else:
        print "please specify the usagedata file name"
        exit()

    if buildGraph:
        #print "have to build graph"        
        #in case the graph isnt availble, write the learnt graph into a file called GraphDB.pickle
        #comment this out when you already have a learnt graph
        print "building graph from", dbFileName
        learnGraph(dbFileName, edgeList=False)
        print "done with building graph.."
        
    #load the type Info into an object
    datatype = readTypeInfo(dbFileName + "_typeInfo.json")

    #load the key, value and nodes
    keyValueNodes = readKeyValueNodes(dbFileName + "_keyValueNodes.json")

    #load the enumerations
    enum = forwardMapping(dbFileName)

    #load the reverse enumerations
    enumRev = reverseMapping(dbFileName)
    
    '''
    #load the graph onto an object
    print "reading Graph"
    G = constructGraph(keyValueNodes, enum, datatype)
    print "done reading Graph"
    '''

    # load the userSequence onto an object
    print "reading usage data"
    #f = open(usageData, "r")
    userSequence = {}
    for line in fileinput.input(usageData):
        jsonUser = json.loads(line)
        userSequence.update(jsonUser)
    #f.close()
    # userSequence = dict(random.sample(userSequence.items(),500))
    print "done using reading usage data"
    
    if generateSequence:
        print "generating user sequence.."
        numberOfUsers = generateSequence[0]
        threshold = generateSequence[1]
        maxItems = generateSequence[2]
        alpha = generateSequence[3]                                                                                                                                                         
            
        #in case the userSequence is not available, simulate it synthetically using the graph. The sequences are written to a file called userSequence.pickle
        print "\ncreating synthetic user sequences.."
        
        createUserData(G, alpha, numberOfUsers, threshold, maxItems, dbFileName)
        print "done creating synthetic user sequences.."

    if userProfiles:
        # each user is associated with his/her own alpha and the attribute importance list
        print "\ncreating userProfiles.."
        userProfiles = {}
        count = 0
        numOfUsers = float(len(userSequence))

        pool = Pool(processes=4)
        for sequence in userSequence:
            # initializing alpha, weight vector to each user
            print "percentage completion: ", count / numOfUsers, count
            count += 1
            userProfiles[sequence] = {}
            userProfiles[sequence]["alpha"] = 0.5
            userProfiles[sequence]["weights"] = {}  # Key the the attribute and value is the corresponding weight for that attr
            pool.apply_async(tweakWeights, [keyValueNodes, userProfiles[sequence], userSequence[sequence]])
            #tweakWeights(keyValueNodes, userProfiles[sequence], userSequence[sequence])

        f = open(dbFileName + "_userProfiles_beforeNorming.pickle", "w")
        f.write(pickle.dumps(userProfiles))
        f.close()

        normalizeWeights(userProfiles, keyValueNodes, datatype)
        
        f = open(dbFileName + "_userProfiles.pickle", "w")
        f.write(pickle.dumps(userProfiles))
        f.close()
        print "done creating userProfiles.."

    #load the userProfiles onto an object
    f = open(dbFileName + "_userProfiles.pickle", "r")
    userProfiles = pickle.loads(f.read())
    f.close()

    if reduceDimensions:
        #print "have to reduce dimensions"
        
        #Dimensionality Reduction
        #find out the relative importance of the attributes, by considering the attribute's relative importance from all users. write the file to attributeRelativeImportance.pickle
        print "\nreducing dimensions"
        attributeRelativeImportance(dbFileName)
        print "done reducing dimensions"
        
    if userSimilarity:
        #print "have to compute user similarity"
        upperlim = userSimilarity

        print "building user similarity"
        buildUserSimilarityDict(G, userSequence, userProfiles, dbFileName, upperlim)
        print "done building user similarity"

    f = open(dbFileName + "_userSimilarity.pickle", "r")
    userSimilarity = pickle.loads(f.read())
    f.close()

    if formClusters:
        #print "have to form clusters"
        threshold = formClusters
        
        print "forming clusters.."
        formClustersFn(userSimilarity, threshold, dbFileName)
        print "done forming clusters.."

    f = open(dbFileName + "_clusters.pickle", "r")
    clusters = pickle.loads(f.read())
    f.close()

    if uid:
        print "List of movies that the user", uid, "has watched: "
        print [G[itemId]["title"][0] for itemId, rating in userSequence[uid]]

        print "\ngetting egocentric recommendation for user ID", uid
        #get the egocentric recommendation, and write it onto a file called contentReco.pickle
        egocentricRecommendation(G, userSequence[uid], dbFileName, uid)
        print "done with egocentric recommendation for user ID", uid, "\n"

        print "\ngetting collaborative recommendation for user ID", uid
        collaborativeRecommend(uid, G, clusters, userSequence, userSimilarity, dbFileName)
        print "done with collaborative recommendation for user ID", uid, "\n"

        #using contentReco.pickle and collabReco.pickle, generate a combined rank list and write it onto combinedReco.pickle
        combineLists(G, userProfiles[uid]["alpha"], uid, userSequence[uid], dbFileName)

def mae(db=None, testData=None):
    if db:
        dbFileName = db
    else:
        print "please specify the database name"
        exit()

    if testData:
        print "please specify the database name"
        exit()

    G = readEdgeList(dbFileName + "_GraphDB.gpickle")
    
    #load the userSequence onto an object
    f = open(dbFileName + "_userData_trainset.json", "r")
    userSequenceTraining = json.loads(f.read())
    f.close()

    f = open(dbFileName + "_userData_testset.json", "r")
    userSequenceTesting = json.loads(f.read())
    f.close()

    #load the userProfiles onto an object
    f = open(dbFileName + "_userProfiles.pickle", "r")
    userProfiles = pickle.loads(f.read())
    f.close()

    f = open(dbFileName + "_userSimilarity.pickle", "r")
    userSimilarity = pickle.loads(f.read())
    f.close()

    f = open(dbFileName + "_clusters.pickle", "r")
    clusters = pickle.loads(f.read())
    f.close()

    users = userSimilarity.keys()

    count = 0
    errors = 0

    for user in users:
        #print "List of movies that the user", user, "has watched: "
        #print [G[itemId]["title"][0] for itemId, rating in userSequenceTraining[user]]

        #print "\ngetting egocentric recommendation for user ID", user
        #get the egocentric recommendation, and write it onto a file called contentReco.pickle
        egocentricRecommendation(G, userSequenceTesting[user], dbFileName, user)
        #print "done with egocentric recommendation for user ID", user

        #print "\ngetting collaborative recommendation for user ID", user
        collaborativeRecommend(user, G, clusters, userSequenceTraining, userSimilarity, dbFileName)
        #print "done with collaborative recommendation for user ID", user, "\n"

        #using contentReco.pickle and collabReco.pickle, generate a combined rank list and write it onto combinedReco.pickle
        alpha = 1.0
        combineLists(G, alpha, user, userSequenceTraining[user], dbFileName)

        f = open(dbFileName + "_" + str(user) + "_combinedReco.pickle", "r")
        combinedReco = pickle.loads(f.read())
        f.close()

        for movie, rating in userSequenceTesting[user]:
            predictedRating = numpy.round(5*combinedReco[movie])
            errors += numpy.abs(float(rating) - float(predictedRating))

            count += 1
        print float(errors) / count

    mae = float(errors) / count
    return mae

if __name__ == "__main__":
    mainImport(db="movielens_1m", usageData="movielens_1m_userData.json", userProfiles=True)