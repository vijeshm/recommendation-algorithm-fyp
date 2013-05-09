import networkx as nx
import json
import sys
import itertools
import matplotlib.pyplot as plt

dbFileName = sys.argv[1]
userID = sys.argv[2]

def readKeyValueNodes(fileName):
    f = open(fileName, "r")
    keyValueNodes = json.loads(f.read())
    f.close()
    return keyValueNodes

f = open(dbFileName+"_userData_trainset.json","r")
userData = {}
for line in f:
	userData.update(json.loads(line))
f.close()

itemList = [ item for item,rating in userData.values()[0]]
f = open(dbFileName+"_movieWatched.json","w")
for item in itemList :
	f.write(item + ", ")
f.close()

keyValueNodes = readKeyValueNodes(dbFileName + "_keyValueNodes.json")

G = nx.Graph()
for key in keyValueNodes:
	for value in keyValueNodes[key]:
		intersectionSet =  list(set(itemList).intersection(set(keyValueNodes[key][value])))
		intersectionPairList = itertools.combinations(intersectionSet,2)
		for edge in intersectionPairList:
			G.add_edge(*edge)

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos, node_size=10,node_shape='o',node_color='0.75')
nx.draw_networkx_edges(G,pos, width=3,edge_color='b')
plt.axis('off')
plt.savefig(dbFileName+"_Graph.png",dpi=1000)
