import networkx as nx
import string
import json

f = open("movielens_GraphDB.edgelist", "r")
G = nx.Graph()
for line in f:
	data = line.split(' ')
	src = data[0]
	dstn = data[1]
	attribute = string.join(data[2:], ' ')

	G.add_node(src)
	G[src][dstn] = eval(attribute)
f.close()