import json
import pickle
finabase = open("ua.base", "r")
finbbase = open("ub.base", "r")
finatest = open("ua.test", "r")
finbtest = open("ub.test", "r")

foutatrain = open("atrain.json", "w")
foutbtrain = open("btrain.json", "w")
foutatest = open("atest.json", "w")
foutbtest = open("btest.json", "w")

userInfo = {}
for line in finabase:
    parts = line.split()
    try:
        userInfo[parts[0]].append([parts[1], parts[2]])
    except KeyError:
        userInfo[parts[0]] = [[parts[1], parts[2]]]
for user in userInfo:
    foutatrain.write(json.dumps({user: userInfo[user]}) + "\n")

userInfo = {}
for line in finbbase:
    parts = line.split()
    try:
        userInfo[parts[0]].append([parts[1], parts[2]])
    except KeyError:
        userInfo[parts[0]] = [[parts[1], parts[2]]]
for user in userInfo:
    foutbtrain.write(json.dumps({user: userInfo[user]}) + "\n")

userInfo = {}
for line in finatest:
    parts = line.split()
    try:
        userInfo[parts[0]].append([parts[1], parts[2]])
    except KeyError:
        userInfo[parts[0]] = [[parts[1], parts[2]]]
for user in userInfo:
    foutatest.write(json.dumps({user: userInfo[user]}) + "\n")

userInfo = {}
for line in finbtest:
    parts = line.split()
    try:
        userInfo[parts[0]].append([parts[1], parts[2]])
    except KeyError:
        userInfo[parts[0]] = [[parts[1], parts[2]]]
for user in userInfo:
    foutbtest.write(json.dumps({user: userInfo[user]}) + "\n")

finabase.close()
finbbase.close()
finatest.close()
finbtest.close()
foutatrain.close()
foutbtrain.close()
foutatest.close()
foutbtest.close()