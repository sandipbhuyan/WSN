class Simulation:

    # Constructor
    def __init__(self, env, cluster, size, g):
        self.env = env
        self.size = size
        self.G = g
        self.cluster = cluster
        # Start the simulation process

    #         self.proc =  env.process(self.run())

    def run(self):
        while True:
            # Execution start
            pair = self.startTransmission()
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

                continue
            else:
                print('\t Data is being transmitted from node %d to node %d ' % (pair['src']['id'], pair['dest']['id']))
                if pair['src']['cluster'] == pair['dest']['cluster']:
                    print('\t same Cluster Transmission')
                    dij = Graph()
                    path = dij.dijkstra(self.cluster.weight[pair['src']['cluster']],
                                        self.cluster.final[pair['src']['cluster']].index(pair['src']['id']),
                                        self.cluster.final[pair['src']['cluster']].index(pair['dest']['id']))
                    path = self.getTransmissionPair(path)

                    for i in path:
                        src = self.cluster.final[pair['src']['cluster']][i[0]]
                        dest = self.cluster.final[pair['src']['cluster']][i[1]]
                        print('\t Transmission start from node %d to node %d' % (src, dest))
                        self.G.nodes[src]['dataSent'] = pair['data_size']
                        self.G.nodes[src]['dataSent'] = pair['data_size']

                        self.G.nodes[src]['energy'] = self.G.nodes[src]['energy'] - self.energyConsume(
                            self.cluster.dic[src][dest], pair['data_size'])
                        if i[1] == pair['dest']['id']:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.5 - self.processing(
                                pair['data_size'])
                        else:
                            self.G.nodes[dest]['energy'] = self.G.nodes[dest]['energy'] - 0.1
                        print('\t Transmission end from node %d to node %d' % (src, dest))
                else:
                    print('\t different Cluster Transmission')

                    # Initialize a transmission

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