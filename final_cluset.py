#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt


# In[2]:


G = nx.Graph()


# In[3]:


import numpy as np
import random


# In[4]:


ls = []


# In[ ]:





# In[5]:


def get_cordinate():
    x = random.randint(1,20)
    y = random.randint(1,20)
    r = [x,y]
    if r in ls:
        get_cordinate()
    else:
        ls.append(r)
    
    return (x,y)


# In[6]:


for i in range(25):
    cod = get_cordinate()
    G.add_node(i,pos = cod)


# In[7]:


import math as m


# In[8]:


def get_dist(x,y):
    return m.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))


# In[9]:


dic = {}
for i in range(len(ls)):
    dic[i] = []
    for j in range(len(ls)):
        val = get_dist(ls[i],ls[j])
        dic[i].append(round(val))


# In[24]:


dic


# In[11]:


clus = {}
for i in cl.dic:
    clus[i] = []
    for j in range(len(dic[i])):
        if dic[i][j]<4:
            clus[i].append(j)


# In[12]:


clus


# In[14]:


cl = 0
cluster = {}
i=0
lis_clus=[]
while(i<len(clus)):
    temp = cl
    for j in clus[i]:
        if j not in cluster:
            cluster[j]=cl
        else:
            cl = cluster[j]
    i+=1
    cl = temp+1


# In[15]:


cluster


# In[ ]:





# In[17]:


final = {}
for i in cluster:
    if cluster[i] not in final:
        final[cluster[i]]=[]
    final[cluster[i]].append(i)


# In[18]:


final


# In[19]:


color = []
r = lambda: random.randint(0,255)


# In[20]:


def generateColor():
    temp = '#%02X%02X%02X' % (r(),r(),r())
    if temp not in color:
        color.append(temp)
        return temp
    else:
        generateColor()


# In[21]:


for i in range(0,25,1):
    for j in range(i,25,1):
        if(i != j):
            G.add_edge(i,j)


# In[23]:


plt.figure(figsize=(20,20))
for i in final:
    nx.draw_networkx_nodes(G,ls,nodelist=final[i],node_color=generateColor())
nx.draw_networkx_edges(G,ls,edge_color='black')
color = []


# In[17]:


dic[1]


# In[19]:


def macGenerator(macList):
    mac = "%02X:%02X:%02X:%02X:%02X:%02X" % (r(),r(),r(),r(),r(),r())
    if mac not in macList:
        macList.append(mac)
        return mac
    else:    
        return macGenerator(macList)


# In[20]:


def getCluster(node):
    for i in final:
        for j in final[i]:
            if(j == node):
                return i


# In[21]:


def getNode(src=50):
    a = random.randint(1,24)
    if(a == src):
        return getNode(src)
    return a


# In[29]:


def startTransmission():
    src = getNode()
    dest = getNode(src)
    
    return {
        'src': {
            'id': src,
            'cluster' : getCluster(src),
        }, 
        'dest': {
            'id': dest,
            'cluster': getCluster(dest),
        },
        'distance': dic[dest][src],
        'data_size': 100,
        'packet_number': 10,
    }


# In[38]:


def latencyCalculator(distance, speed, packetSize, transmissionRate):
    return (distance/speed) + (packetSize/transmissionRate)


# In[47]:


def throughputCalculator(latency):
    return (524288/latency)/10000


# In[48]:


def setLatency(distance):
    res = []
    for i in distance:
        res.append(latencyCalculator(i * 1000,100000,262144, 65536))
    return res


# In[51]:


def setThroughput(distance):
    lat = setLatency(distance)
    res = []
    for i in lat: 
        res.append(throughputCalculator(i))
    return res


# In[52]:


setThroughput(dic[1])


# In[53]:


macList = []
def setAttributes(node):
    G.nodes[node['id']]['energy'] = 100
    G.nodes[node['id']]['dataRecieved'] = 0
    G.nodes[node['id']]['dataSent'] = 0
    G.nodes[node['id']]['throughput'] = setThroughput(dic[node['id']])
    G.nodes[node['id']]['network_latency'] = setLatency(dic[node['id']])
    G.nodes[node['id']]['duty_cycle'] = random.randint(0,10)
    G.nodes[node['id']]['error_rate'] = 0
    G.nodes[node['id']]['cluster'] = node['cluster']
    G.nodes[node['id']]['cluster_head'] = node['cluster_head']
    G.nodes[node['id']]['routing_table'] = {}
    G.nodes[node['id']]['mac'] = macGenerator(macList)
    G.nodes[node['id']]['distanceList'] = dic[node['id']]
    G.nodes[node['id']]['isCollector'] = 1 if node['cluster_head']==0 else 0
    G.nodes[node['id']]['isTransmitter'] =1 if node['cluster_head']==1 else 0    


# In[54]:


for i in range(25):
    node = {
        'id': i,
        'cluster':  getCluster(i),
        'cluster_head': 0,
    }
    setAttributes(node)
macList = []


# In[58]:


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


# In[ ]:





# In[59]:


showData(25)


# In[60]:


class Node:
    throughput = 0
    latency = []
    duty_cycle = 0
    error_rate = 0
    cluster = 0
    cluster_head = 0
    mac = ""
    routing = {}
    distance = []
    
    def __init__(self, node):
        self.duty_cycle = node['duty_cycle']
        self.cluster = node['cluster']
        self.cluster_head = node['cluster_head']
        self.mac = node['mac']
        self.routing = node['routing_table']
        self.distance = node['distanceList']
    
    def energyConsume(self,distance):
        return distance * 1
    
    def dataPacket(self,dataSize):
        return int((dataSize / 10) + (1 if (dataSize % 10) != 0 else 0))
    
    def run(self):
        data = startTransmission()
        return data
    
    def findNewClusterHead(self):
        return True
    
    def diactivateNode(self):
        return True
    
    def activateNode(self):
        return True
    
    def changePreference(self):
        return True







