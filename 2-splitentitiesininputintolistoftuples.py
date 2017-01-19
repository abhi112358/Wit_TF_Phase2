# we will have -
#queries which is a list of all queries
#ENTITIES  -  each query has multiple entities, convert them in tuples, make a list of those tuples , and finally make a list of all such lists over the entire query set


import urllib
import requests
import json
import csv
import numpy




queries = []
ENTITIES = []


f = open('queries.txt', 'r')
## Read the first line
line = f.readline().rstrip()




## If the file is not empty keep reading line one at a time
## till the file is empty
while line:

#    print line
    queries.append(line)

    line=f.readline().rstrip()
#    print line
    qENTITIES=[]
    jsn = json.loads(line)
    for key, value in jsn.iteritems():#key is a string and entity is a list of strings
        for bro in value:
            tup = (key,bro)
            qENTITIES.append(tup)
    ENTITIES.append(qENTITIES)


    line=f.readline().rstrip()





f.close()
print queries
#print "\n\n\n"
print ENTITIES