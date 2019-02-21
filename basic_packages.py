import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m

ls = []
G = nx.Graph()


def get_cordinate():
    x = random.randint(1, 20)
    y = random.randint(1, 20)
    r = [x, y]
    if r in ls:
        get_cordinate()
    else:
        ls.append(r)

    return (x, y)

for i in range(25):
    cod = get_cordinate()
    G.add_node(i,pos = cod)

def get_dist(x,y):
    return m.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

dic = {}
for i in range(len(ls)):
    dic[i] = []
    for j in range(len(ls)):
        val = get_dist(ls[i],ls[j])
        dic[i].append(round(val))

clus = {}
for i in dic:
    clus[i] = []
    for j in range(len(dic[i])):
        if dic[i][j]<4:
            clus[i].append(j)

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

final = {}
for i in cluster:
    if cluster[i] not in final:
        final[cluster[i]]=[]
    final[cluster[i]].append(i)

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
for i in final:
    nx.draw_networkx_nodes(G,ls,nodelist=final[i],node_color=generateColor())
nx.draw_networkx_edges(G,ls)
color = []

plt.show()
