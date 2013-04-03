#usage: python userProfilePlots.py userID

import json
import sys
import matplotlib.pyplot as plt
import numpy as np

def roundoff(lst, place):
    factor = float(pow(10, place))
    for e in enumerate(lst):
        lst[e[0]] = int(e[1] * factor) / factor


f = open("../movielens_1m_attributeRelativeImportance.json", "r")
attribRelImp = json.loads(f.read())
f.close()

attribs = attribRelImp.keys()
weights = attribRelImp.values()
roundoff(weights, 3)

fig = plt.figure()
ax = fig.add_subplot(111)
xPos = np.arange(len(attribs))
width = 0.2

rects0 = ax.bar(xPos, weights, width, color='#3333FF')

ax.set_ylabel("weights")
ax.set_title("Relative attribute importance for the dataset")
ax.set_xticks(xPos + width)
ax.set_xticklabels(attribs)

ax.legend( (rects0[0],), ('Relative Attribute Importance',) )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+0.01, height, ha='center', va='bottom')

#autolabel(rects0)
autolabel(rects0)

plt.show()