#usage: python userProfilePlots.py userID

import json
import sys
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects, axis):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        axis.text(rect.get_x()+rect.get_width()/2., height+0.01, height, ha='center', va='bottom')

userID = sys.argv[1]

f = open("../../code/movielens_1m_userProfiles_beforeNorming.json", "r")
beforeNorm = json.loads(f.read())
f.close()

f = open("../../code/movielens_1m_userProfiles_afterNorming.json", "r")
afterNorm = json.loads(f.read())
f.close()

attribs = beforeNorm[userID]["weights"].keys()
weightsBefore = beforeNorm[sys.argv[1]]["weights"].values()
sumOfWeights = float(sum(weightsBefore))
weightsBefore = [weight / sumOfWeights for weight in weightsBefore]

weightsAfter = afterNorm[userID]["weights"].values()
weightsEqual = [1.0/len(attribs)]*len(attribs)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
xPos = np.arange(len(attribs))
width = 0.2

'''
rects0 = ax.bar(xPos, weightsEqual, width, color='#FFCC00')
rects1 = ax.bar(xPos+width, weightsBefore, width, color='#FF3300')
rects2 = ax.bar(xPos+2*width, weightsAfter, width, color='#3333FF')
'''

rects0 = ax1.bar(xPos, weightsEqual, width, color='#FFCC00')
ax1.set_ylabel("weights")
ax1.set_title("Relative attribute importance for the user " + userID)
ax1.set_xticks(xPos + width)
ax1.set_xticklabels(attribs)
ax1.legend( (rects0[0], ), ('equal weights', ) )
#autolabel(rects0, ax1)

rects1 = ax2.bar(xPos+width, weightsBefore, width, color='#FF3300')
ax2.set_ylabel("weights")
ax2.set_title("Relative attribute importance for the user " + userID)
ax2.set_xticks(xPos + width)
ax2.set_xticklabels(attribs)
ax2.legend( (rects1[0], ), ('before range-based normalizing', ) )
#autolabel(rects0, ax2)

rects2 = ax3.bar(xPos+2*width, weightsAfter, width, color='#3333FF')
ax3.set_ylabel("weights")
ax3.set_title("Relative attribute importance for the user " + userID)
ax3.set_xticks(xPos + width)
ax3.set_xticklabels(attribs)
ax3.legend( (rects2[0], ), ('after range-based normalizing', ) )
#autolabel(rects2, ax3)

rects0 = ax4.bar(xPos, weightsEqual, width, color='#FFCC00')
rects1 = ax4.bar(xPos+width, weightsBefore, width, color='#FF3300')
rects2 = ax4.bar(xPos+2*width, weightsAfter, width, color='#3333FF')
ax4.set_ylabel("weights")
ax4.set_title("Relative attribute importance for the user " + userID)
ax4.set_xticks(xPos + width)
ax4.set_xticklabels(attribs)
#ax4.legend( (rects0[0], rects1[0], rects2[0]), ('equal weights', 'before range-based normalizing', 'after range-based normalizing') )
#autolabel(rects0, ax4)
#autolabel(rects1, ax4)
#autolabel(rects2, ax4)
plt.show()

'''
ax.clear()
rects1 = ax.bar(xPos+width, weightsBefore, width, color='#FF3300')
ax.legend( (rects1[0], ), ('before range-based normalizing', ) )
autolabel(rects1)
plt.show()

ax.clear()
rects2 = ax.bar(xPos+2*width, weightsAfter, width, color='#3333FF')
ax.legend( (rects2[0], ), ('after range-based normalizing',) )
autolabel(rects2)
plt.show()

ax.clear()
rects0 = ax.bar(xPos, weightsEqual, width, color='#FFCC00')
rects1 = ax.bar(xPos+width, weightsBefore, width, color='#FF3300')
rects2 = ax.bar(xPos+2*width, weightsAfter, width, color='#3333FF')
ax.legend( (rects0[0], rects1[0], rects2[0]), ('equal weights', 'before range-based normalizing', 'after range-based normalizing') )
autolabel(rects0)
autolabel(rects1)
autolabel(rects2)
plt.show()
'''

'''
fout = open("userProfile.csv", "w")
weightsBefore = [ str(weight) for weight in weightsBefore ]
weightsAfter = [ str(weight) for weight in weightsAfter ]
fout.write(",".join(attribs) + "\n")
fout.write(",".join(weightsBefore) + "\n")
fout.write(",".join(weightsAfter) + "\n")
fout.close()
'''