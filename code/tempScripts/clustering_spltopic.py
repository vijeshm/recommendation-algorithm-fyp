import pickle
import random
import copy

def getSimilarity(user1, user2):
    userSimilarity = X
    if userSimilarity[user1].has_key(user2):
        return userSimilarity[user1][user2][0] / userSimilarity[user1][user2][1]
    else:
        return userSimilarity[user2][user1][0] / userSimilarity[user2][user1][1]

def formClusters(user, threshold, dbFileName=None):
    clusters = random.sample(user,len(user))
    clusters = user
    after_cluster = []
    
    total = float(len(user)*( len(user) + 1) / 2)
    count = 0

    for x in range(len(clusters)):
        tic = [ [clusters[x]] ]
        for y in clusters[x+1:]:
            count += 1
            i = 0
            print clusters[x], y, count / total, "tic:" + str(len(tic))
            while i<len(tic) and getSimilarity(clusters[x],y) >= threshold:
                toc = [y]
                for j in tic[i] :
                    if getSimilarity(j,y) >= threshold :
                        toc.append(j)

                if toc[1:] == tic[i]:
                    tic[i].append(y)
                    i = i+1

                elif toc not in tic:
                    tic.insert(i+1, toc)
                    i = i+2
                    
                else :
                    i = i+1

        for i in tic :
            if len(i) != 1:
                i.sort()
                if i not in after_cluster:
                    after_cluster.append(i)

    after_cluster.sort()
    after_cluster_final = []
    for i in after_cluster:
        flag = False
        for j in after_cluster:
            if i!=j and set(i).issubset(set(j)):
                flag = True
                break

        if not flag:
            after_cluster_final.append(i)

    return after_cluster_final

k = 4
f = open("movielens_userSimilarity.pickle")
#f = open("JSONGomoloText_userSimilarity.pickle")
str1 =f.read()
X = pickle.loads(str1)
f.close()
cluster = formClusters(X.keys(), k*0.0623890960069)

for i in cluster:
    print i
print "threshold = ", k*0.0623890960069
print len(cluster)


string = pickle.dumps(cluster)
fout = open('clusters123', 'w')
fout.write(string)
fout.close()