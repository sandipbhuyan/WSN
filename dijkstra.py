from collections import defaultdict


class Graph:

    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def printPath(self, parent, j, res):

        if parent[j] == -1:
            res.append(j),
            return res
        self.printPath(parent, parent[j], res)
        res.append(j)
        return res

    def getPath(self, parent, dest):
        res = []
        res = self.printPath(parent, dest, res)
        print(res)
        return res

    def dijkstra(self, graph, src):
        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row
        parent = [-1] * row
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
        while queue:
            u = self.minDistance(dist, queue)
            queue.remove(u)
            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        return {
            'dist': dist,
            'parent': parent,
        }