import csv
import time
import datetime
import collections
from heapq import *
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = collections.defaultdict(list)
        self.distances = {}
        self.labels = {}
        self.node_set = collections.defaultdict(list)

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance, label):
        if not to_node in self.edges[from_node]:
            self.edges[from_node].append(to_node)
            self.distances[(from_node, to_node)] = distance
            self.labels[(from_node, to_node)] = label
        else:
            if distance < self.distances[(from_node, to_node)]:
                self.distances[(from_node, to_node)] = distance
                self.labels[(from_node, to_node)] = label

# Dijkstra algorithm
def dijkstra(graph, initial):
    visited = {initial: 0}
    h = [(0, initial)]
    path = {}
    route = {}
    nodes = set(graph.nodes)
    while nodes and h:
        dist, min_node = heappop(h)
        if min_node not in nodes:
            while h and min_node not in nodes:
                dist, min_node = heappop(h)
            if not h and min_node not in nodes: 
                break
        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                heappush(h, (weight, edge))
                path[edge] = min_node
                route[edge] = graph.labels[(min_node, edge)]
    return visited, path, route

def shortest_path(graph, origin, dest):
    length, path, route = dijkstra(graph, origin)
    x = dest
    shortest_path = [dest]
    route_time = []
    route_type = []
    while x != origin:
        shortest_path.append(path[x])
        route_time.append(graph.distances[path[x],x])
        if x=='132' and route[x]=='walk':
            route_type.append('airtrain')
        else:
            route_type.append(route[x])
        x = path[x]
    shortest_path.reverse()
    route_time.reverse()
    route_type.reverse()
#     print(shortest_path)
#     print(route_type)
    # print(route_time)
    return length[dest], shortest_path, route_type

