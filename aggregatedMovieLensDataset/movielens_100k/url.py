import urllib2
import json
from BeautifulSoup import BeautifulSoup

movieInfo = {}
fin = open("u.item", "r")
fout = open("movielens_100k", "a")

count = 0
for line in fin:
    count += 1
    if count > 1654:
        parts = line.split("|")
        
        baseurl = parts[4]
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
        request = opener.open(baseurl)
        finalurl = request.url
        imdbid = finalurl.split("/")[-2]
        if imdbid == "www.imdb.com":
            try:
                soup = BeautifulSoup(request.read())
                tr = soup.table.findChildren()[0]
                col = tr.findChildren()[0]
                anchor = col.findChildren()[0]
                imdbid = anchor['href'].split("/")[2]
                print "actual IMDB ID", imdbid
            except IndexError:
                print "index error.. invalid search query"
                print finalurl.split("?")
                imdbid = "tt" + finalurl.split("?")[-1].split("-")[-1]
                print imdbid
        
        baseurl = "http://imdbapi.org/?id=" + imdbid + "&type=json&plot=simple&episode=0&lang=en-US&aka=simple&release=simple&business=0&tech=0"
        req = urllib2.Request(baseurl)
        res = urllib2.urlopen(req)
        resString = res.read()

        jsonRes = json.loads(resString)
        out = {}
        out["id"] = [parts[0]]
        for key in jsonRes:
            if key!="rating_count" and key!="poster" and key!="imdb_url" and key!="plot_simple" and key!="runtime" and key!="release_date" and key!="also_known_as" and key!="episodes":
                if key=="rating" or key=="rated" or key=="title" or key=="rating_count" or key=="year" or key=="type" or key=="imdb_id" or key=="filming_locations":
                    out[key] = [jsonRes[key]]
                else:
                    out[key] = jsonRes[key]

        fout.write(json.dumps(out) + "\n")
        print count / 1682.0, imdbid, parts[1]

        if count % 5 == 0:
            print "Check now.. count:", count
            fout.close()
            fout = open("movielens_100k", "a")

fout.close()
fin.close()
