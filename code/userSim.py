import modules

dbFileName = "movielens_1m"
G = {}
datatype = modules.readTypeInfo(dbFileName + "_typeInfo.json")
print datatype

#load the key, value and nodes
keyValueNodes = modules.readKeyValueNodes(dbFileName + "_keyValueNodes.json")

#load the enumerations
enum = modules.forwardMapping(dbFileName)

#load the reverse enumerations
enumRev = modules.reverseMapping(dbFileName)