import urllib
import requests
import json
import csv
import numpy


RESULTENTITIES = []  #list of list of tuples of result entities # ENTITIES AND RESULTENTITIES will be finally compared in integrated file # ADDED IN PHASE 2

queries = []

#NEXT 10 LINES OF CODE WERE REPLACED IN PHASE 2 TO SKIP EVERY ALTERNATE LINE

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

    line=f.readline().rstrip()



print queries

###############################################################################


queriesencoded = []

for query in queries:
    queriesencoded.append(urllib.quote(query, safe=''))
    #dot will appear as in encoded string but it's no problem
    #because even wit's encoder does the same

print ("brock")

print queriesencoded


###############################################################################

matrix = []
row = ["QUERY","RESPONSE STATUS" , "QUERY'S MEAN 'CONFIDENCE" , "QUERY'S 'STANDARD DEVIATION" , "RECOGNIZED ENTITIES"]
matrix.append(row)
row=[]
matrix.append(row)

netmeanset = []
netstdset = []


for queryencoded in queriesencoded:
    row = []
    r=requests.get("https://api.wit.ai/message?v=20170111&q="+queryencoded, headers={"Authorization":"Bearer QWRFP44Y7XSF3LNVOARB4RGLVCGHZSWH"})
    print r.text

    #dump r.text to dump.txt
    with open("dump.txt", "a") as myfile:
        myfile.write(r.text+",")

    #parse r.text json object
    jsn = json.loads(r.text) #jsn is a dictionary haivng 2 keys - _text and entities. Ideally we should now loop over it, but since only 2 keys, no need to loop
    message = jsn['_text']  #handling the first key
    row.append(message)

    print r.status_code
    row.append(r.status_code)


    if 'entities' in jsn: #handling the second key
        ents = jsn['entities'] #now ents is just a json object which means that it is also a dictionary'. But this time, we don't know in advance how many key value pairs are there. So we will loop over this dictionary''
        en=''
        con=''
        val=''
        conarray = [] #list of confidences of all entities predicted in this query. Will help us measure overall confidene for THIS QUERY
        rowofentities = []

        qRESULTENTITIES=[] #for a single query, it stores all the (result entity, result value) tuples # added in PHASE 2

        for key, value in ents.iteritems(): #that's how you loop over a dictionary'
            #now value is an array. for example in the response, (value=)intent is an array OF 1 JSON OBJECT (WHICH IS A DICTIONARY )HAVING 2 or 3 KEY VALUE PAIRS (confidence, type  a third key - value might also be present)
            print key
            en=key
            for key1, value1 in value[0].iteritems(): #why value[0]? because value was an array of 1 json object
                print (key1+':'+str(value1))
                if key1=='confidence':
                    con=value1
                    conarray.append(con)
                elif key1=='value':
                    val=value1

            #here we have the opportunity of finding mean confidence and standard deviation for THIS QUERY using conarray


            #append all these values to rowofentities list which will be appended to row list later on

            rowofentities.append("("+en+", "+str(val)+") : "+str(con))
            qRESULTENTITIES.append((en,str(val)))

        #our conarray hs now been built. Calculate mean confidence and standard deviation
        mean = numpy.mean(conarray)
        print mean
        netmeanset.append(mean)
        std = numpy.std(conarray)
        print std
        netstdset.append(std)
        row.append(mean)
        row.append(std)

        for item in rowofentities:
            row.append(item)



        RESULTENTITIES.append(qRESULTENTITIES) #ADDED IN PHASE 2, building RESULTENTITIES superlist


	
    matrix.append(row)



#execution finished. make an extra row for netmean and netstd
row = []
row.append("QUERYSET'S MEAN CONFIDENCE = " + str(numpy.mean(netmeanset)))
matrix.append([])
matrix.append(row)
row=[]
row.append("QUERYSET'S MEAN' STDEV = " + str(numpy.mean(netstdset)))
matrix.append(row)

##############################################################################
#write matrix into the csv


with open('results.csv', 'wb') as outfile:

	writer = csv.writer(outfile)
	for row in matrix:
		writer.writerow(row)



print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
print RESULTENTITIES