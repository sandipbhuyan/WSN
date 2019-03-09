import simpy

class Simulation:

    # Constructor
    def __init__(self, env, cluster, size, g, cluster_head):
        self.env = env
        self.size = size
        self.G = g
        self.cluster = cluster
        self.cluster_head = cluster_head
        # Start the simulation process
        self.proc = env.process(self.run())

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
                print('Regenerating Cluster')
                self.G = cluster.regenerate_cluster(self.G)
                print('Sorry transmission is not possible because of low energy \n')
                continue
            else:
                print('Data is being transmitted from node %d to node %d ' % (pair['src']['id'], pair['dest']['id']))
                if pair['src']['cluster'] == pair['dest']['cluster']:
                    print('same Cluster Transmission')
                else:
                    print('different Cluster Transmission')

    # Initialize a transmission
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