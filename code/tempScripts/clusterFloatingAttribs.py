import random
import numpy
import matplotlib.pyplot as plt

'''
just execute this program. no inputs needed.
'''

def clusterAndPlot(data):
    data.sort()

    dist = [ (data[i+1] - data[i]) for i in range(len(data) - 1)]
    avrg = numpy.average(dist)

    plt.plot(dist, [0]*len(dist), 'bo')
    #plt.show()

    clusters = []
    cluster = []

    for i in range(len(dist)):
        if dist[i] <= avrg:
            cluster.append(data[i])
        elif cluster != []:
            clusters.append(cluster)
            cluster = []

    styles = ['bo', 'ro', 'go']
    for e in enumerate(clusters):
        plt.plot(e[1], [0]*len(e[1]), styles[e[0] % len(styles)])
    plt.show()

if __name__ == "__main__":
    data = [float(random.randint(0, 100)) for i in range(100)]
    clusterAndPlot(data)