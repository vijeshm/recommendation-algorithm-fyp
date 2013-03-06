import pickle
import numpy
import math

errors = 0

userData_testset = open("movielens_userData_testset.json", "r")
print "reading userData"
userSequence = json.loads(userData_testset.read())
print "done reading userData"

for user in userSequence:
    userReco = open("movielens_" + user + "_combinedReco.pickle", "r")
    jsonObj = pickle.loads(userReco.read())
    userReco.close()

    for movie,rating in userSequence[user]:
        predictedRating = numpy.round(5*jsonObj[movie])
        errors += numpy.abs(float(rating) - float(predictedRating))

    count += 1

userData_testset.close()