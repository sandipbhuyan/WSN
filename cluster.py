import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m
from sklearn.cluster import DBSCAN

class Cluster:
    dic = {}
    final = {}
    G = nx.Graph()
    cluster = []
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
        return (x, y)

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

        self.cluster = DBSCAN(eps=4, min_samples=1).fit_predict(np.array(self.ls))

        for i in range(max(self.cluster)+1):
            self.final[i] = []
            for j in range(len(self.cluster)):
                if (i == self.cluster[j]):
                    self.final[i].append(j)

        return self.G

    def regenerate_cluster(self, g):
        self.G = g
        temp_ls = []
        ass_ls = []

        for i in range(self.size):
            if self.G.nodes[i]['mode'] == 'on':
                temp_ls.append(self.ls[i])
                ass_ls.append(i)

        self.cluster = DBSCAN(eps=4, min_samples=1).fit_predict(np.array(temp_ls))

        self.final = {}
        print(self.cluster)
        print(ass_ls)
        for i in range(max(self.cluster) + 1):
            self.final[i] = []
            for j in range(len(ass_ls)):
                if (i == self.cluster[j]):
                    self.final[i].append(ass_ls[j])

        return self.G