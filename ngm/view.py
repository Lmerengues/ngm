# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse

from py2neo import Graph,Node,Relationship,database

from django.db import connections

from django.core   import serializers

import json

import numpy as np

import requests

test_graph = Graph(
    "http://118.89.233.180:7474",
    username="neo4j",
    password="77777"
)
def f2(a,b):
    return b['val']-a['val']

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def near(request):
    return render(request,'near.html')
def path(request):
    return render(request,'path.html')
def totalview(request):
    return render(request,'index.html')
def gettotalview(request):
    cursor = connections['default'].cursor()
    cursor.execute("select * from influence order by sval desc limit 50 ")
    influence = dictfetchall(cursor)
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select * from center order by sval desc limit 50 ")
    center = dictfetchall(cursor)
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select * from claster order by sval desc limit 50 ")
    claster = dictfetchall(cursor)
    cursor.close()

    response = HttpResponse(json.dumps([influence,center,claster]), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def find_near(request):
    a = request.GET['pname']

    maxn = request.GET['maxnear']

    cursor = connections['default'].cursor()
    cursor.execute("select sval from influence where sname = %s ",(a,))
    raw = dictfetchall(cursor)
    influence = -1
    if len(raw)>=1:
        influence = raw[0]['sval']
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select sval from center where sname = %s ", (a,))
    raw = dictfetchall(cursor)
    center = -1
    if len(raw) >= 1:
        center = raw[0]['sval']
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select sval from claster where sname = %s ", (a,))
    raw = dictfetchall(cursor)
    claster = -1
    if len(raw) >= 1:
        claster = raw[0]['sval']
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select sval from num where sname = %s ", (a,))
    raw = dictfetchall(cursor)
    num = -1
    if len(raw) >= 1:
        num = raw[0]['sval']
    cursor.close()

    data = test_graph.data("Match (n:Person{name: {str}})-[r:know]-(end:Person) return r.val,n.name,end.name order by r.val desc limit " +maxn ,str=a)
    #
    '''
    for dataitem in data:
        for dataitem2 in data:
            if (dataitem['n.name'] == dataitem2['end.name'] and dataitem['end.name']==dataitem2['n.name']) or \
                    (dataitem['n.name'] == dataitem2['n.name'] and dataitem['end.name']==dataitem2['end.name']):
                dataitem['r.value'] += dataitem2['r.value']
                data.remove(dataitem2)
                break
    '''
    for i in range(0,len(data)):
        for j in range(i+1,len(data)):
            if (data[i]['n.name'] == data[j]['end.name'] and data[i]['end.name'] == data[j]['n.name']) or \
                    (data[i]['n.name'] == data[j]['n.name'] and data[i]['end.name'] == data[j]['end.name']):
                data[i]['r.val'] += data[j]['r.val']
                data.remove(data[j])
                break
    #
    if(request.GET['mr'] == "1"):
        response = HttpResponse(json.dumps([data,influence,claster,center,num]), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    #tdata = []
    #for i in range(0,maxn):
    #    tdata[i] = data[i]

    #data = tdata
    '''
    for i in data:
        iname = i['end.name']
        #inode = test_graph.node(i['end.id'])
        for j in data:
            jname = j['end.name']
            if iname==jname:
                continue
            #jnode = test_graph.node(j['end.id'])
            #find_r = test_graph.match_one(start_node=inode,end_node=jnode,bidirectional=True);
            find_r = test_graph.data("Match (n:Person{name: {i}})-[r:CALL]-(end:Person{name:{j}}) return r.value",i=iname
                                     ,j=jname)
            if find_r:
                data.append({"r.value":find_r[0]['r.value'],"n.name":iname,"end.name":jname})
    '''
    '''
    for i in range(0, len(data)):
        hisdata = test_graph.data(
            "Match (n:Person{name: {str}})-[r:CALL]-(end:Person) where r.value > 10 return r.value, "
            "n.name,end.name order by r.value desc limit 25", str=data[i]['end.name'])
        for j in range(0, len(hisdata)):
            if hisdata[j]['end.name'] == data[i]['end.name']:
                data.append(hisdata[j])
    '''
    hisdatas = []
    for i in range(0, len(data)):
        hisdata = test_graph.data(
            "Match (n:Person{name: {str}})-[r:know]->(end:Person) return r.val, n.name,end.name order by r.val desc limit 20", str=data[i]['end.name'])
        hisdatas.append(hisdata)

    cnt = 0
    for i in range(0, len(data)):
        for j in range(0, len(hisdatas)):
            for k in range(0, len(hisdatas[j])):
                if (data[i]['end.name'] == hisdatas[j][k]['end.name']):
                    if (hisdatas[j][k] in data):
                        continue
                    else:
                        data.append({'r.val': hisdatas[j][k]['r.val'], 'n.name': hisdatas[j][k]['end.name'],
                                     'end.name': hisdatas[j][k]['n.name']})
                        # cnt += 1
    # print cnt

    response = HttpResponse(json.dumps([data,num,influence,center,claster]),content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def getEdgeinfo(request):
    name1 = request.GET['sname']
    name2 = request.GET['tname']

    url = "http://websensor.playbigdata.com/fss3/service.svc/GetSearchResults"

    querystring = {"query": name1+" "+ name2, "num": "5", "start": "1"}

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'upgrade-insecure-requests': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'cache-control': "no-cache",
        'postman-token': "5549dc28-2253-f247-d5f9-1f8e87bd830f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    response = HttpResponse(json.dumps(res), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def find_path(request):
    #return render(request,'path.html')
    fperson = request.GET['fname']
    tperson = request.GET['tname']
    data = test_graph.run("Match(p1:Person{name:{fp}}),(p2:Person{name:{tp}}),p=allshortestpaths((p1)-[*..10]-(p2)) return p limit 30",fp=fperson,tp=tperson)
    cnt = 0
    datap = []
    for datai in data:
        cnt+= 1
        #datap.append(datai['p'])

    if len(datap)==0:
        response = HttpResponse(json.dumps(datap), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    sdis = datap[0].relationships()
    if(len(datap) < 10):
        step = 3
        result_len = 0
        while result_len < 10:
            path_store = []
            mydata = test_graph.run(
                "MATCH (fromNodes:Person) where fromNodes.name='" + fperson + "' MATCH (toNodes:Person) where toNodes.name='" + tperson + "' CALL apoc.algo.allSimplePaths(fromNodes, toNodes, 'know'," + str(
                    step) + ") yield path RETURN path,reduce(a=1, r in rels(path) | a+r.val) as orders ORDER BY length(path),orders desc limit 10")
            result_len = 0
            for item in mydata:
                result_len += 1
                path_store.append(item['path'])
            step += 1
        for p in path_store:
            datap.append(p)
    nodes_total = []
    rels_total = []
    #all_nodes_total = []
    paths = []
    cnt = 0
    for p in datap:
        nodes = p.nodes()
        rels = p.relationships()
        # print rel
        # print nodes
        # print rels
        this_path = []
        this_path_val = 0
        this_path_values = []
        for i in range(0, len(nodes)):
            #all_nodes_total.append(nodes[i]['name'])
            if nodes[i]['name'] not in nodes_total:
                nodes_total.append(nodes[i]['name'])
            if i < len(nodes) - 1:
                rels_total.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i+1]['name'], "val": rels[i]['val']})
                this_path.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rels[i]['val']})
                this_path_val += rels[i]['val']
                this_path_values.append(rels[i]['val'])
        paths.append({'path': this_path, 'val': np.sum(this_path_values)})
    paths.sort(cmp=f2)

    #双保险
    response = HttpResponse(json.dumps([nodes_total,rels_total,paths]), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

