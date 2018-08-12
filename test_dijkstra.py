import csv
import time
import datetime
import collections
from Dijkstra import shortest_path
from build_network import build_graph
origin, dest = 'taxi_132', 'taxi_117'
print('building the graph')
graph = build_graph()
print('running dijkstra')
length, route, route_type = shortest_path(graph, origin, dest)
print(length)
print(route)
print(route_type)
