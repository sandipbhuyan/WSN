import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m
from sklearn.cluster import DBSCAN, k_means


class Cluster:
    dic = {}
    final = {}
    G = nx.Graph()
    cluster = []
    ls = []
    centroid = []
    cluster_head = []
    weight = {}
    chw = []

    def __init__(self, size):
        self.size = size

    def getWeight(self, src, dest):
        return G.get_edge_data(src, dest)['weight']

    def weightMartix(self):
        weight = {}
        for i in self.final:
            weight[i] = []
            for j in range(len(self.final[i])):
                res = []
                for k in range(len(self.final[i])):
                    if k == j:
                        res.append(0)
                    else:
                        res.append(self.getWeight(j, k))
                weight[i].append(res)
        self.weight = weight
        return

    def clusterHeadWeightMatrix(self):
        chw = []
        for i in range(len(self.cluster_head)):
            res = []
            for k in range(len(self.cluster_head)):
                if i == k:
                    res.append(0)
                else:
                    res.append(self.getWeight(self.cluster_head[i], self.cluster_head[k]))
            chw.append(res)
        self.chw = chw

    def calculateWeight(self, dis, lat, e1, e2):
        return m.ceil((10 ** 6) * ((dis * lat) / (e1 * e2)))

    def setWeightOfEdges(self):
        for i in range(0, self.size, 1):
            for j in range(i, self.size, 1):
                if (i != j):
                    distance = self.dic[i][j]
                    latency = self.G.nodes[i]['network_latency'][j]
                    E1 = self.G.nodes[i]['energy']
                    E2 = self.G.nodes[j]['energy']
                    self.G.get_edge_data(i, j)['weight'] = self.calculateWeight(distance, latency, E1, E2)
        return self.G

    def get_coordinate(self):
        x = random.randint(1, 40)
        y = random.randint(1, 40)
        r = [x, y]
        if r in self.ls:
            self.get_coordinate()
        else:
            self.ls.append(r)
        return (x, y)

    def get_dist(self, x, y):
        return m.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def getClusterHead(self, cls, cent):
        distance = []
        for i in cls:
            distance.append(self.get_dist(self.ls[i], cent))
        return distance.index(min(distance))

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
        n_clus = max(self.cluster) + 1
        temp = k_means(np.array(self.ls), n_clusters=n_clus)

        self.centroid = temp[0]
        self.cluster = temp[1]

        for i in range(len(self.centroid)):
            for j in range(2):
                self.centroid[i][j] = int(round(self.centroid[i][j]))

        for i in range(max(self.cluster) + 1):
            self.final[i] = []
            for j in range(len(self.cluster)):
                if (i == self.cluster[j]):
                    self.final[i].append(j)

        for i in range(len(self.final)):
            self.cluster_head.append(self.final[i][self.getClusterHead(self.final[i], self.centroid[i])])

        return self.G

    def regenerate_cluster(self, g):
        self.G = g
        temp_ls = []
        ass_ls = []

        for i in range(self.size):
            if self.G.nodes[i]['mode'] == 'on':
                temp_ls.append(self.ls[i])
                ass_ls.append(i)

        if len(temp_ls) == 0:
            print('All nodes are off')
            print('can\'t regenerate cluster')
            return self.G

        self.cluster = DBSCAN(eps=4, min_samples=1).fit_predict(np.array(temp_ls))
        n_clus = max(self.cluster) + 1
        temp = k_means(np.array(temp_ls), n_clusters=n_clus)
        self.cluster = temp[1]

        self.centroid = temp[0]
        self.final = {}
        for i in range(len(self.centroid)):
            for j in range(2):
                self.centroid[i][j] = int(round(self.centroid[i][j]))

        for i in range(max(self.cluster) + 1):
            self.final[i] = []
            for j in range(len(ass_ls)):
                if (i == self.cluster[j]):
                    self.final[i].append(ass_ls[j])

        self.cluster_head = []
        for i in range(len(self.final)):
            self.cluster_head.append(self.final[i][self.getClusterHead(self.final[i], self.centroid[i])])

        return self.G