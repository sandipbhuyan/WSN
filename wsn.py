import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m
import cluster as c
import libraries_wsn as lw

cl = c.Cluster(25)
G = cl.generate_cluster()

color = []
r = lambda: random.randint(0,255)

def generateColor():
    temp = '#%02X%02X%02X' % (r(),r(),r())
    if temp not in color:
        color.append(temp)
        return temp
    else:
        generateColor()

for i in range(0,25,1):
    for j in range(i,25,1):
        if(i != j):
            G.add_edge(i,j)

plt.figure(figsize=(20,20))
for i in cl.final:
    nx.draw_networkx_nodes(G,cl.ls,nodelist=cl.final[i],node_color=generateColor())
nx.draw_networkx_edges(G,cl.ls,edge_color='black')
color = []

def macGenerator(macList):
    mac = "%02X:%02X:%02X:%02X:%02X:%02X" % (r(), r(), r(), r(), r(), r())
    if mac not in macList:
        macList.append(mac)
        return mac
    else:
        return macGenerator(macList)

def getCluster(node):
    for i in cl.final:
        for j in cl.final[i]:
            if (j == node):
                return i

def getNode(src=50):
    a = random.randint(1, 24)
    if (a == src):
        return getNode(src)
    return a

def startTransmission():
    src = getNode()
    dest = getNode(src)

    return {
        'src': {
            'id': src,
            'cluster': getCluster(src),
        },
        'dest': {
            'id': dest,
            'cluster': getCluster(dest),
        },
        'distance': dic[dest][src],
        'data_size': 100,
        'packet_number': 10,
    }

def latencyCalculator(distance, speed, packetSize, transmissionRate):
    return (distance / speed) + (packetSize / transmissionRate)

def throughputCalculator(latency):
    return (524288 / latency) / 10000

def setLatency(distance):
    res = []
    for i in distance:
        res.append(latencyCalculator(i * 1000, 100000, 262144, 65536))
    return res

def setThroughput(distance):
    lat = setLatency(distance)
    res = []
    for i in lat:
        res.append(throughputCalculator(i))
    return res

macList = []
def setAttributes(node):
    G.nodes[node['id']]['energy'] = 100
    G.nodes[node['id']]['dataRecieved'] = 0
    G.nodes[node['id']]['dataSent'] = 0
    G.nodes[node['id']]['throughput'] = setThroughput(cl.dic[node['id']])
    G.nodes[node['id']]['network_latency'] = setLatency(cl.dic[node['id']])
    G.nodes[node['id']]['duty_cycle'] = random.randint(0,10)
    G.nodes[node['id']]['error_rate'] = 0
    G.nodes[node['id']]['cluster'] = node['cluster']
    G.nodes[node['id']]['cluster_head'] = node['cluster_head']
    G.nodes[node['id']]['routing_table'] = {}
    G.nodes[node['id']]['mac'] = macGenerator(macList)
    G.nodes[node['id']]['distanceList'] = cl.dic[node['id']]
    G.nodes[node['id']]['isCollector'] = 1 if node['cluster_head']==0 else 0
    G.nodes[node['id']]['isTransmitter'] =1 if node['cluster_head']==1 else 0
    G.nodes[node['id']]['mode'] = 'on'

for i in range(25):
    node = {
        'id': i,
        'cluster':  getCluster(i),
        'cluster_head': 0,
    }
    setAttributes(node)
macList = []

def showData(number):
    for i in range(number):
        print("Data for node: " + str(i))
        print("\t id : " + str(i))
        print("\t Data Recieved : "+ str(G.nodes[i]['dataRecieved']))
        print("\t Data Sent : "+ str(G.nodes[i]['dataSent']))
        print("\t Duty Cycle : "+ str(G.nodes[i]['duty_cycle']))
        print("\t Error Rate : "+ str(G.nodes[i]['error_rate']))
        print("\t Cluster : "+ str(G.nodes[i]['cluster']))
        print("\t MAC Address : "+ str(G.nodes[i]['mac']))
        print("\t Latency : "+ str(G.nodes[i]['network_latency']))
        print("\t Throughput : "+ str(G.nodes[i]['throughput']))

showData(25)