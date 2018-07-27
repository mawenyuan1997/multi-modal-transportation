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

# return the subway/bus route of an edge
def check_route(label):
    p = label.find(' ')
    if p < 0:
        return label, 'no route'
    return (label[:p], label[p + 1:])

# Dijkstra algorithm
def dijkstra(graph, initial):
    visited = {initial: 0}
    h = [(0, initial)]
    path = {}
    route = {}

    nodes = set(graph.nodes)

    while nodes and h:
        # min_node = None
        # for node in nodes:
        #     if node in visited:
        #         if min_node is None:
        #             min_node = node
        #         elif visited[node] < visited[min_node]:
        #             min_node = node

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
            # add bus/subway transfer time
            if min_node in path:
                pt, pr = check_route(graph.labels[path[min_node], min_node])
                t, r = check_route(graph.labels[min_node, edge])
                weight += waiting_time(pt, pr, t, r)
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
#     print(route_time)
    return length[dest], shortest_path, route_type

def waiting_time(pt, pr, t, r):
    subway_route = ['1','2','3','4','5','5X','6','6X','7','7X','GS','A','B','C','D','E',
                    'F','FS','G','J','L','M','N','Q','R','H','W','Z','SI']
    subway_day = [20,8,8,8,12,12,10,8,5,5,5,8,10,10,10,
                  12,12,10,10,10,5,12,10,10,20,15,10,10,30]
    subway_time = dict(zip(subway_route, subway_day))

    if (pt, t) == ('walk', 'subway') or (pt, t) == ('subway', 'subway') and pr != r:
        return subway_time[r] / 2
    elif (pt, t) == ('walk', 'lirr') or (pt, t) == ('lirr', 'lirr') and pr != r:
        return 600
    elif (pt, t) == ('walk', 'bus') or (pt, t) == ('bus', 'bus') and pr != r:
        return 300
    return 0
