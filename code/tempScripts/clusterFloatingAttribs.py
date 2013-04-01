import random
import numpy
import matplotlib.pyplot as plt

'''
just execute this program. no inputs needed.
'''

data = [float(random.randint(0, 100)) for i in range(100)]

data.sort()

dist = [ (data[i+1] - data[i]) for i in range(len(data) - 1)]
avrg = numpy.average(dist)

plt.plot(dist, [0]*len(dist), 'bo')
#plt.show()

clusters = []
cluster = []
print "data", data
print "dist", dist

for i in range(len(dist)):
    print "\ndist", dist[i]
    print "avrg", avrg
    if dist[i] <= avrg:
        cluster.append(data[i])
    elif cluster != []:
        print cluster
        clusters.append(cluster)
        cluster = []

styles = ['bo', 'ro', 'go']
for e in enumerate(clusters):
    plt.plot(e[1], [0]*len(e[1]), styles[e[0] % len(styles)])
plt.show()
