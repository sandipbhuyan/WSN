import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math as m
import dijkstra as dijkstra
from sklearn.cluster import DBSCAN, k_means

class Simulation:

    # Constructor
    def __init__(self, env, cluster, size, g):
        self.env = env
        self.size = size
        self.G = g
        self.cluster = cluster
        # Start the simulation process
        self.action = env.process(self.run(env))

    def run(self, env):
        while True:
            # Execution start
            pair = self.startTransmission()
            yield env.timeout(1)
            print('Transmission will start from %d to node %d ' % (pair['src']['id'], pair['dest']['id']))
            if self.G.nodes[pair['src']['id']]['energy'] < 20 or self.G.nodes[pair['dest']['id']]['energy'] < 20:
                # Low Power Condition
                if self.G.nodes[pair['src']['id']]['energy'] < 20:
                    self.turnNodeOff(pair['src']['id'])
                elif self.G.nodes[pair['dest']['id']]['energy'] < 20:
                    self.turnNodeOff(pair['dest']['id'])
                print('\t Sorry transmission is not possible because of low energy')
                print('\t Regenerating Cluster')
                self.G = self.cluster.regenerate_cluster(self.G)
                self.cluster.weight = {}
                self.cluster.chw = []
                self.cluster.weightMartix()
                self.cluster.clusterHeadWeightMatrix()
                yield env.timeout(2)
                continue
            else:
                print('\t Data is being transmitted from node %d to node %d ' % (pair['src']['id'], pair['dest']['id']))
                if pair['src']['cluster'] == pair['dest']['cluster']:
                    dij = Graph()
                    print('\t same Cluster Transmission')
                    yield env.timeout(1)
                    path = dij.dijkstra(self.cluster.weight[pair['src']['cluster']],
                                        self.cluster.final[pair['src']['cluster']].index(pair['src']['id']),
                                        self.cluster.final[pair['src']['cluster']].index(pair['dest']['id']))
                    path = self.getTransmissionPair(path)

                    for i in path:
                        src = self.cluster.final[pair['src']['cluster']][i[0]]
                        dest = self.cluster.final[pair['src']['cluster']][i[1]]
                        print('\t changing weight from %d to %d' % (src, dest))
                        print('\t Transmission start from node %d to node %d' % (src, dest))
                        self.G.nodes[src]['dataSent'] = pair['data_size']
                        self.G.nodes[dest]['dataReceived'] = pair['data_size']

                        self.G.nodes[src]['energy'] = self.G.nodes[src]['energy'] - self.energyConsume(
                            self.cluster.dic[src][dest], pair['data_size'])
                        if i[1] == pair['dest']['id']:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.5 - self.processing(
                                pair['data_size'])
                        else:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.1
                        print('\t Transmission end from node %d to node %d' % (src, dest))
                        yield env.timeout(1)
                else:
                    dij = Graph()
                    print('\t different Cluster Transmission')
                    sch = self.cluster.cluster_head[pair['src']['cluster']]
                    dch = self.cluster.cluster_head[pair['dest']['cluster']]
                    path = dij.dijkstra(self.cluster.weight[pair['src']['cluster']],
                                        self.cluster.final[pair['src']['cluster']].index(pair['src']['id']),
                                        self.cluster.final[pair['src']['cluster']].index(sch))
                    path = self.getTransmissionPair(path)
                    print('\t -----')
                    yield env.timeout(1)

                    for i in path:
                        src = self.cluster.final[pair['src']['cluster']][i[0]]
                        dest = self.cluster.final[pair['src']['cluster']][i[1]]
                        print('\t Transmission start from node %d to node %d' % (src, dest))
                        self.G.nodes[src]['dataSent'] = pair['data_size']
                        self.G.nodes[dest]['dataReceived'] = pair['data_size']
                        print('\t changing weight from %d to %d' % (src, dest))
                        self.G.nodes[src]['energy'] = self.G.nodes[src]['energy'] - self.energyConsume(
                            self.cluster.dic[src][dest], pair['data_size'])
                        if i[1] == pair['dest']['id']:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.5 - self.processing(
                                pair['data_size'])
                        else:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.1
                        print('\t Transmission end from node %d to node %d' % (src, dest))
                        yield env.timeout(1)
                    # Initialize a transmission
                    print('\t Clusterhead transmisssion')
                    path = dij.dijkstra(self.cluster.chw, self.cluster.cluster_head.index(sch),
                                        self.cluster.cluster_head.index(dch))
                    path = self.getTransmissionPair(path)
                    yield env.timeout(1)

                    for i in path:
                        src = self.cluster.cluster_head[i[0]]
                        dest = self.cluster.cluster_head[i[1]]
                        print('\t Transmission start from node %d to node %d' % (src, dest))
                        self.G.nodes[src]['dataSent'] = pair['data_size']
                        self.G.nodes[dest]['dataReceived'] = pair['data_size']
                        print('\t changing weight from %d to %d' % (src, dest))
                        self.G.nodes[src]['energy'] = self.G.nodes[src]['energy'] - self.energyConsume(
                            self.cluster.dic[src][dest], pair['data_size'])
                        if i[1] == pair['dest']['id']:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.5 - self.processing(
                                pair['data_size'])
                        else:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.1
                        print('\t Transmission end from node %d to node %d' % (src, dest))
                        yield env.timeout(1)
                    print('\t Different cluster transmission')
                    path = dij.dijkstra(self.cluster.weight[pair['dest']['cluster']],
                                        self.cluster.final[pair['dest']['cluster']].index(dch),
                                        self.cluster.final[pair['dest']['cluster']].index(pair['dest']['id']))
                    path = self.getTransmissionPair(path)
                    yield env.timeout(1)

                    for i in path:
                        src = self.cluster.final[pair['dest']['cluster']][i[0]]
                        dest = self.cluster.final[pair['dest']['cluster']][i[1]]
                        print('\t Transmission start from node %d to node %d' % (src, dest))
                        self.G.nodes[src]['dataSent'] = pair['data_size']
                        self.G.nodes[dest]['dataReceived'] = pair['data_size']
                        print('\t changing weight from %d to %d' % (src, dest))
                        self.G.nodes[src]['energy'] = self.G.nodes[src]['energy'] - self.energyConsume(
                            self.cluster.dic[src][dest], pair['data_size'])
                        if i[1] == pair['dest']['id']:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.5 - self.processing(
                                pair['data_size'])
                        else:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.1
                        print('\t Transmission end from node %d to node %d' % (src, dest))
                        yield env.timeout(1)

    def getTransmissionPair(self, path):
        k = []
        for j in range(len(path) - 1):
            k.append([path[j], path[j + 1]])

        return k

    def processing(self, size):
        return size * 0.001

    def startTransmission(self):
        src = self.getNode()
        dest = self.getNode(src)

        return {
            'src': {
                'id': src,
                'cluster': self.getCluster(src),
            },
            'dest': {
                'id': dest,
                'cluster': self.getCluster(dest),
            },
            'distance': self.cluster.dic[src][dest],
            'data_size': random.randint(1, 50),
            'packet_number': 10,
        }

    # Turn off node
    def turnNodeOff(self, id):
        self.G.nodes[id]['mode'] = 'off'

    # Get the cluster of the node
    def getCluster(self, node):
        for i in self.cluster.final:
            for j in self.cluster.final[i]:
                if (j == node):
                    return i

    # Get Random node
    def getNode(self, src=200):
        a = random.randint(1, self.size)
        if (a == src):
            return self.getNode(src)
        return a

    # Calculate energy consumption value
    def energyConsume(self, distance, size):
        return distance * size * .01