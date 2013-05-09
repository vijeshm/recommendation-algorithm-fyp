import sys
import json
import matplotlib.pyplot as plt
import numpy

dbFileName = sys.argv[1]

def attributeRelativeImportance(dbFileName):
    """
        In order to determine the relative importance of each attribute, we take the average out the attribute's weight from the all the users.
    """
    f = open(dbFileName + "_normalizedUserProfiles.json", "r")
    userProfiles = {}
    for line in f:
	    userProfiles.update(json.loads(line))
    f.close()
    
    weights = {}
    count = 0
    numOfUsers = len(userProfiles)
    for userProfile in userProfiles:
        count += 1
        for attr in userProfiles[userProfile]["weights"]:
            try:
                weights[attr] += userProfiles[userProfile]["weights"][attr]["@RAI"]
            except KeyError:
                weights[attr] = userProfiles[userProfile]["weights"][attr]["@RAI"]

    for attr in weights:
        weights[attr] = weights[attr] / numOfUsers

    f = open(dbFileName + "_attributeRelativeImportance.json", "w")
    f.write(json.dumps(weights))
    f.close()

def valueRelativeImportance(dbFileName):
    """
        In order to determine the relative importance of each attribute, we take the average out the attribute's weight from the all the users.
    """
    f = open(dbFileName + "_normalizedUserProfiles.json", "r")
    userProfiles = {}
    for line in f: 
        userProfiles.update(json.loads(line))
    f.close()
    
    weights = {}
    count = 0
    numOfUsers = len(userProfiles)
    
    for userProfile in userProfiles:
        count += 1
        for attr in userProfiles[userProfile]["weights"]:
            if not weights.has_key(attr):
                weights[attr]={}

            for value in userProfiles[userProfile]["weights"][attr]:
                if value != "@RAI":
                    try:
                        weights[attr][value] += userProfiles[userProfile]["weights"][attr][value]
                    except KeyError:
                        weights[attr][value] = userProfiles[userProfile]["weights"][attr][value]

    for attr in weights:
        for value in weights[attr]:
            if value != "@RAI":
                weights[attr][value][0] = weights[attr][value][0] / numOfUsers

    f = open(dbFileName + "_valueRelativeImportance.json", "w")
    f.write(json.dumps(weights))
    f.close()

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+0.01, height, ha='center', va='bottom')

print "\nreducing dimensions"
attributeRelativeImportance(dbFileName)
valueRelativeImportance(dbFileName)
print "done reducing dimensions"

f = open(dbFileName + "_attributeRelativeImportance.json", "r")
attributeRelativeImportance = json.loads(f.read())
f.close()


fig = plt.figure(figsize = (24, 18))
ax = fig.add_subplot(111)
xPos = numpy.arange(1,len(attributeRelativeImportance.keys())+1)
y = attributeRelativeImportance.values()
width = 0.2

rects2 = ax.bar(xPos, y, width, color='#3333FF')

ax.set_ylabel("weights")
ax.set_title("Plotting of relative attribute weights")
ax.set_xticks(xPos + width)
ax.set_xticklabels(attributeRelativeImportance.keys())

autolabel(rects2)
fig.savefig(dbFileName+"_reducedDimension.png")
