#usage: python 3_show.py dbfilename userID

import json
import sys
import matplotlib.pyplot as plt
import numpy as np

dbFileName = sys.argv[1]
userID = sys.argv[2]

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+0.01, height, ha='center', va='bottom')

#f = open(dbFileName + "_normalizedUserProfiles.json", "r")
f = open(dbFileName + "_normalizedUserProfiles.json", "r")
for line in f:
	profile = json.loads(line)
	if profile.keys()[0] == userID:
		attribs = profile[userID]["weights"].keys()
		weights = [profile[userID]["weights"][attrib]["@RAI"] for attrib in attribs]
		fig = plt.figure(figsize = (24, 18))
		ax = fig.add_subplot(111)
		xPos = np.arange(1,len(attribs)+1)
		width = 0.2
		rects2 = ax.bar(xPos, weights, width, color='#3333FF')

		ax.set_ylabel("weights")
		ax.set_title("Relative attribute importance for the user " + userID)
		ax.set_xticks(xPos + width)
		ax.set_xticklabels(attribs)

		autolabel(rects2)
		fp = open(dbFileName+"_attributes.txt","w")
		for att in attribs:
			fp.write(str(att)+"\n")
		fp.close()
		fig.savefig(dbFileName+"_userAttribImportance.png")
		break
f.close()



