import modules1 as m
import pickle 
import json 

fp = open("movielens_1m_userProfiles_beforeNorming.pickle", "r")
userProfiles = pickle.loads(fp.read())
fp.close()

f = open("movielens_1m_keyValueNodes.json", "r")
keyValueNodes = json.loads(f.read())
f.close()
  
f = open("movielens_1m_typeInfo.json", "r")
datatype = json.loads(f.read())
f.close()

m.normalizeWeights(userProfiles, keyValueNodes, datatype)