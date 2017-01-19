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
    ENTITIES.append(line)

    line=f.readline().rstrip()





f.close()
print queries
#print "\n\n\n"
print ENTITIES