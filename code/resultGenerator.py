import sys
import os
import json
import math
import modules

percent = float(sys.argv[1])

#os.system("mkdir " + str(percent))
userData = open("movielens_1m_userData.json","r")
userData_trainset = open("movielens_1m_userData_trainset.json", "w")
userData_testset = open("movielens_1m_userData_testset.json", "w")

print "reading userData"
userSequence = {}
for line in userData:
    userSequence.update(json.loads(line))  
print "done reading userData"

train = {}
test = {}

for user in userSequence:
    print "processing user ", user
    partition = int(math.ceil(len(userSequence[user])*percent/100.0))
    train[user] = userSequence[user][:partition]
    test[user] = userSequence[user][partition:]


for user in train:
    print user , train[user]
    userData_trainset.write(json.dumps({user:train[user]})+"\n")


for user in test:
    userData_testset.write(json.dumps({user:test[user]})+"\n")

userData_trainset.close()
userData_testset.close()
userData.close()

"""
#os.system("python modules.py --db=movielens --usageData=movielens_userData.json -userProfiles -reduceDimensions -userSimilarity=6040 -formClusters=0.8")
#os.system("python modules.py --db=movielens --usageData=movielens_userData.json -userSimilarity=6040 -formClusters=0.8")
modules.mainImport(db="movielens", usageData="movielens_userData_trainset.json", buildGraph=False, userProfiles=False, generateSequence=None, reduceDimensions=False, userSimilarity=6040, formClusters=None, uid=None)

for user in userSequence:
    print "generating data for user " + user
    modules.mainImport(db="movielens", usageData="movielens_userData_trainset.json", uid=user)
    os.system("mv movielens_" + user + "_contentReco.pickle " + str(percent))
    os.system("mv movielens_" + user + "_collabReco.pickle " + str(percent))
    os.system("mv movielens_" + user + "_combinedReco.pickle " + str(percent))

os.system("mv movielens_userProfiles.pickle " + str(percent))
os.system("mv movielens_attributeRelativeImportance.pickle " + str(percent))
os.system("mv movielens_userSimilarity.pickle " + str(percent))
os.system("mv movielens_clusters.pickle " + str(percent))
os.system("mv movielens_userData_trainset.json " + str(percent))
os.system("mv movielens_userData_testset.json " + str(percent))
"""