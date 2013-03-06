import urllib
import urllib2
import json
import string

'''
Read the movies list from movies.dat (this is from the largest dataset. we're gonna reduce the dataset size later on)
get the movie name from each line
issue a request to imdbapi.org
if it fails, issue a request to omdbapi.com
evaluate the response and clean it into json format
write the json onto movieInfo.dat
'''

fin  = open("movies.dat","r")

fout = open("movieInfo.dat", "r")
numOfLines = len(fout.readlines())
fout.close()

fout = open("movieInfo.dat","a")

arr = fin.readlines()

for i in range(numOfLines, len(arr)):
    print i
    fout.close()
    fout = open("movieInfo.dat","a")
    name = arr[i].split("::")[1][:-7]
    print name

    if ":" in name:
        name = string.join(name.split(":"), '')
        print "WITHOUT SEMICOLON", name
    
    if "&" in name:
        name = string.join(name.split("&"), '')


    if "(" in name:
        parts = name.split("(")
        parts[1] = parts[1].split(")")[0]
        if "a.k.a" in parts[1]:
            parts[1] = parts[1][6:]
            print "AKA AKA AKA AKA"

        try:
            request = "http://imdbapi.org/?" + urllib.urlencode({'q': parts[1]})
            print request
            out = urllib2.urlopen(request)
            outstr = out.read()
            print outstr
            jsonObj = eval(outstr)[0]
            fout.write(json.dumps(jsonObj) + "\n")
        except KeyError:
            print "SECOND PART IN BRACKET DIDNT WORK"
            
            try:
                request = "http://imdbapi.org/?" + urllib.urlencode({'q': parts[0]})
                print request
                out = urllib2.urlopen(request)
                outstr = out.read()
                print outstr
                jsonObj = eval(outstr)[0]
                fout.write(json.dumps(jsonObj) + "\n")
            except KeyError:
                imdbID = eval(urllib2.urlopen("http://www.omdbapi.com/?" + urllib.urlencode({"s": parts[0]}) ).read())["Search"][0]["imdbID"]
                request = "http://imdbapi.org/?" + urllib.urlencode({'id': imdbID})
                print request
                out = urllib2.urlopen(request)
                outstr = out.read()
                print outstr
                jsonObj = eval(outstr)
                print jsonObj
                
                fout.write(json.dumps(jsonObj) + "\n")                

    else:
        try:
            request = "http://imdbapi.org/?" + urllib.urlencode({'q': name})
            print request
            out = urllib2.urlopen(request)
            outstr = out.read()
            print outstr
            jsonObj = eval(outstr)[0]
            fout.write(json.dumps(jsonObj) + "\n")
        except KeyError:

            imdbID = eval(urllib2.urlopen("http://www.omdbapi.com/?" + urllib.urlencode({"s": name}) ).read())["Search"][0]["imdbID"]

            request = "http://imdbapi.org/?" + urllib.urlencode({'id': imdbID})
            print request
            out = urllib2.urlopen(request)
            outstr = out.read()
            print outstr
            jsonObj = eval(outstr)
            print jsonObj
            
            fout.write(json.dumps(jsonObj) + "\n")

fout.close()
fin.close()