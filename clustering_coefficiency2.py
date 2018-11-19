#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import csv

writer = csv.writer(file('cc3.csv', 'wb'))
file = open('news.json', 'r') 
data=json.load(file)['response']['docs']
newsList=list()
linksList=dict()
nodes=set()
for tempdict in data:
    templist=tempdict.get('Entity_Person')#list of entities in the same news
    if templist:
        newsList.append(templist)
        for i in range(len(templist)):
            if templist[i] not in nodes:
                linksList[templist[i]]=set()
                nodes.add(templist[i])
for news in newsList:
    #news is a list of entities in one piece of news
    for entity in news:
        for temp in news:
            #print temp,
            linksList[entity].add(temp)
        linksList[entity].remove(entity)
vectors=dict()
for key,sets in linksList.items():
    neighbors=len(sets)#not include itself
    if neighbors==0 or neighbors==1:
        pass
    else:
        count=0
        for entity in sets:
            count=count+len(sets&linksList[entity])-1
        vectors[key]=count/(neighbors*1.0*(neighbors-1))
result=sorted(vectors.iteritems(), key=lambda d:d[1],reverse=True)
#screen output
#for i in range(10):
#    print result[i][0],result[i][1]
#f = open('clustering.txt', 'w')
#for i in range(10):
#    f.write(result[i][0].encode('utf-8')+"\n")
#f.close()

file.close()

#f = open('clustering.txt', 'w')
cnt = 1
for i in range(0,len(result)):
    #f.write(result[i][0].encode('utf-8')+"\n")
    writer.writerow([cnt,result[i][0].encode('utf-8'),result[i][1]])
    cnt += 1
#f.close()