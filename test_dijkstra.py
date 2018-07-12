import csv
import time
import datetime
import collections
from Dijkstra import shortest_path
from build_network import build_graph
origin, dest = '1_120S', 'A_H02S'
graph = build_graph()
length, route, route_type = shortest_path(graph, origin, dest)
print(length)
print(route)
print(route_type)
