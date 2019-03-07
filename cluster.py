import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m

class Cluster:
    cluster = {}
    dic = {}
    clus = {}
    final = {}
    G = nx.Graph()
    ls = []
    
    def __init__(self, size):
        self.size = size

    def get_coordinate(self):
        x = random.randint(1, 20)
        y = random.randint(1, 20)
        r = [x, y]
        if r in self.ls:
            self.get_coordinate()
        else:
            self.ls.append(r)
        return (x,y)

    def get_dist(self, x, y):
        return m.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def generate_cluster(self):
        for i in range(self.size):
            cod = self.get_coordinate()
            self.G.add_node(i, pos=cod)

        for i in range(len(self.ls)):
            self.dic[i] = []
            for j in range(len(self.ls)):
                val = self.get_dist(self.ls[i], self.ls[j])
                self.dic[i].append(round(val))

        for i in self.dic:
            self.clus[i] = []
            for j in range(len(self.dic[i])):
                if self.dic[i][j] < 4:
                    self.clus[i].append(j)

        cl = 0
        i = 0
        while(i<len(self.clus)):
            temp = cl
            for j in self.clus[i]:
                if j not in self.cluster:
                    self.cluster[j] = cl
                else:
                    cl = self.cluster[j]
            i += 1
            cl = temp + 1

        for i in self.cluster:
            if self.cluster[i] not in self.final:
                self.final[self.cluster[i]] = []
            self.final[self.cluster[i]].append(i)

        return self.G

    def regenerate_cluster(self, g):
        self.G = g
        for i in self.dic:
            self.clus[i] = []
            for j in range(len(self.dic[i])):
                if self.dic[i][j] < 4 and G.nodes(i)['mode'] == 'on' :
                    self.clus[i].append(j)

        cl = 0
        i = 0
        while(i<len(self.clus)):
            temp = cl
            for j in self.clus[i]:
                if j not in self.cluster:
                    self.cluster[j] = cl
                else:
                    cl = self.cluster[j]
            i += 1
            cl = temp + 1

        for i in self.cluster:
            if self.cluster[i] not in self.final:
                self.final[self.cluster[i]] = []
            self.final[self.cluster[i]].append(i)
        print(self.final)

        return self.G
