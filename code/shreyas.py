import networkx as nx
import random
import matplotlib.pyplot as plt

G = nx.erdos_renyi_graph(100, 0.3)
cluster1 = random.sample(G.nodes(), 50)
cluster2 = list(set(G.nodes()).difference(set(cluster1)))

color1 = random.random()
color2 = random.random()
valueMap = {}
for node in cluster1:
    valueMap[node] = color1
for node in cluster2:
    valueMap[node] = color2

colors = [valueMap[node] for node in G.nodes()]
nx.draw(G, node_color=colors)
plt.show()