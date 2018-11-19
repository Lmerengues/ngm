#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import csv
import io
import networkx as nx
import json

#filename = 'news.txt'
G=nx.Graph()
#with open(filename, encoding='UTF-8') as file:

writer = csv.writer(file('pr.csv', 'wb'))

#file = io.open(filename, encoding='UTF-8')

with open('news.json', 'r') as f:
    data = json.load(f)

cnt = 0
for line in file:
    blank = " "
    perNum = line.count(blank)
    list1 = list(line.split())
    for a in list1:
        for b in list1:
            if a != b:
                G.add_edge(a,  b) #若两个人a和b出现在同一新闻中，则加入边（a，b）
    print cnt
    cnt += 1



print nx.number_connected_components(G) #统计连通分量个数
sg = max(nx.connected_component_subgraphs(G), key=len)
print nx.diameter(sg)
print sg.number_of_nodes() #统计最大连通分量节点数
print nx.average_shortest_path_length(sg)




pr=nx.pagerank(G)
dict = sorted(pr.items(), key = lambda d:d[1], reverse = True) #按pagerank值降序排序
#f = os.open("result.txt",os.O_RDWR|os.O_CREAT)

file.close()

#f = open("result.txt", "w")
cnt = 1
for node, value in dict:
    #thisline = str(node) + " " + str(value) + "\n"
    #os.write(fd, thisline)
    #print(node,value)
    #print("%s %0.6f" % (node, value), file = f)
    writer.writerow([cnt,node.encode('utf-8'),value])
    cnt += 1