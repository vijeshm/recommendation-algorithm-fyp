#usage: python userProfilePlots.py userID

import json
import sys
import matplotlib.pyplot as plt
import numpy as np

userID = sys.argv[1]

f = open("../movielens_1m_userProfiles_beforeNorming.json", "r")
beforeNorm = json.loads(f.read())
f.close()

f = open("../movielens_1m_userProfiles_afterNorming.json", "r")
afterNorm = json.loads(f.read())
f.close()

attribs = beforeNorm[userID]["weights"].keys()
weightsBefore = [beforeNorm[sys.argv[1]]["weights"][attrib]["@RAI"] for attrib in attribs]
sumOfWeights = float(sum(weightsBefore))
weightsBefore = [weight / sumOfWeights for weight in weightsBefore]

weightsAfter = [afterNorm[userID]["weights"][attrib]["@RAI"] for attrib in attribs]
weightsEqual = [1.0/len(attribs)]*len(attribs)

fig = plt.figure()
ax = fig.add_subplot(111)
xPos = np.arange(len(attribs))
width = 0.2

rects0 = ax.bar(xPos, weightsEqual, width, color='#FFCC00')
rects1 = ax.bar(xPos+width, weightsBefore, width, color='#FF3300')
rects2 = ax.bar(xPos+2*width, weightsAfter, width, color='#3333FF')

ax.set_ylabel("weights")
ax.set_title("Relative attribute importance for the user " + userID)
ax.set_xticks(xPos + width)
ax.set_xticklabels(attribs)

ax.legend( (rects0[0], rects1[0], rects2[0]), ('equal weights', 'before range-based normalizing', 'after range-based normalizing') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+0.01, height, ha='center', va='bottom')

#autolabel(rects0)
autolabel(rects1)
autolabel(rects2)


plt.show()

'''
fout = open("userProfile.csv", "w")
weightsBefore = [ str(weight) for weight in weightsBefore ]
weightsAfter = [ str(weight) for weight in weightsAfter ]
fout.write(",".join(attribs) + "\n")
fout.write(",".join(weightsBefore) + "\n")
fout.write(",".join(weightsAfter) + "\n")
fout.close()
'''