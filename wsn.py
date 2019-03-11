import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m
import cluster as c
import simulation as sim
import dijkstra as dij
import warnings
import simpy

cl = c.Cluster(25)
G = cl.generate_cluster()

color = []
r = lambda: random.randint(0, 255)

warnings.filterwarnings('ignore')

def generateColor():
    temp = '#%02X%02X%02X' % (r(), r(), r())
    if temp not in color:
        color.append(temp)
        return temp
    else:
        generateColor()


for i in range(0, 25, 1):
    for j in range(i, 25, 1):
        if (i != j):
            G.add_edge(i, j, weight=j)

plt.figure(figsize=(15, 15))
for i in cl.final:
    nx.draw_networkx_nodes(G, cl.ls, nodelist=cl.final[i], node_color=generateColor())
nx.draw_networkx_edges(G, cl.ls, edge_color='white')
color = []

def macGenerator(macList):
    mac = "%02X:%02X:%02X:%02X:%02X:%02X" % (r(), r(), r(), r(), r(), r())
    if mac not in macList:
        macList.append(mac)
        return mac
    else:
        return macGenerator(macList)

def latencyCalculator(distance):
    return (distance * 10 / 200000) + (10240 / 15 * (2 ** 20))

def setLatency(distance):
    res = []
    for i in distance:
        res.append(latencyCalculator(i))
    return res

macList = []

def setAttributes(node):
    G.nodes[node['id']]['energy'] = 100
    G.nodes[node['id']]['dataRecieved'] = 0
    G.nodes[node['id']]['dataSent'] = 0
    G.nodes[node['id']]['network_latency'] = setLatency(cl.dic[node['id']])
    G.nodes[node['id']]['duty_cycle'] = random.randint(0, 10)
    G.nodes[node['id']]['error_rate'] = 0
    G.nodes[node['id']]['cluster'] = node['cluster']
    G.nodes[node['id']]['cluster_head'] = node['cluster_head']
    G.nodes[node['id']]['routing_table'] = {}
    G.nodes[node['id']]['mac'] = macGenerator(macList)
    G.nodes[node['id']]['distanceList'] = cl.dic[node['id']]
    G.nodes[node['id']]['isCollector'] = 1 if node['cluster_head'] == 0 else 0
    G.nodes[node['id']]['isTransmitter'] = 1 if node['cluster_head'] == 1 else 0
    G.nodes[node['id']]['mode'] = 'on'

    # Get the cluster of the node

def getCluster(node):
    for i in cl.final:
        for j in cl.final[i]:
            if (j == node):
                return i

for i in range(25):
    node = {
        'id': i,
        'cluster': getCluster(i),
        'cluster_head': 0,
    }
    setAttributes(node)
macList = []

def getWeight(src,dest):
    return G.get_edge_data(src,dest)['weight']

weight = {}

for i in cl.final:
    weight[i] = []
    for j in range(len(cl.final[i])):
        res = []
        for k in range(len(cl.final[i])):
            if k == j:
                res.append(0)
            else:
                res.append(getWeight(j,k))
        weight[i].append(res)

cl.weight = weight

env = simpy.Environment()
e = sim.Simulation(env,cl,24,G)
e.run()