import json
import string

predefinedTypes = ["float", "integer", "date", "bool", "string"]
validAttribChars = string.letters + '1234567890_'

f = open("../movielens_100k", "r")
typeInfo = json.loads(f.readline())
for attrib in typeInfo:
    if typeInfo[attrib] not in predefinedTypes:
        print "invalid type definition for", attrib

itemJson = [json.loads(line) for line in f]
f.close()

attribs = []
ids = []
for e in enumerate(itemJson):
    if not e[1].has_key("id"):
        print "item at line number",e[0] + 1, " doesnt have an id"

    for attrib in e[1]:
        for char in attrib:
            if char not in validAttribChars:
                print "     the attibute '", attrib, "' contains invalid characters."
                break
    
    for attrib in e[1]:
        if attrib not in typeInfo:
            print "     the type of '" + attrib + "' for the item at line " + str(e[0] + 2) + " is not defined."

    for attrib in e[1]:
        if type(e[1][attrib]) != list:
            print "     " + attrib + " for the item at line " + str(e[0] + 2) + " should be a list."