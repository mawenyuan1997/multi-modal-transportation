import csv
import time
import datetime
import collections
from Dijkstra import shortest_path, dijkstra
from build_network import build_graph, modify_edges
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
taxi_time = {}
with open('data/taxitime.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        s = str(int(float(row[0])))
        e = str(int(float(row[1])))
        if s not in ['264','265'] and e not in ['264','265'] and s!=e:
            taxi_time[s, e]=float(row[2])

# old_multi_time = {}
# with open('data/multimodal_startJFK.csv') as f:
#     reader=csv.reader(f)
#     next(reader)
#     for row in reader:
#         old_multi_time[row[0],row[1]] = float(row[2])
        
bike_ids = set()
with open('data/bikeStation_coordinates.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        bike_ids.add('bike_' + row[0])
        
graph = build_graph()
dest = set()
for (id1, id2), ti in taxi_time.items():
    if id1=='132':
        dest.add(id2)
new_multi_time = {}
original_graph = deepcopy(graph)
import glob
exist = set(glob.glob("data/ebike/*.csv"))
for b_id in bike_ids:
    modify_edges(graph, b_id)
    filename = 'data/ebike/' + b_id + '.csv'
    if filename not in exist:
        with open(filename,'w') as file:
            dist, path, route = dijkstra(graph,'132')
            for id2 in dest:
                print(b_id,'132',id2,dist[id2])
                file.write('132' + ',' + id2 + ',' +
                            str(dist[id2]) + ',' + str(taxi_time['132',id2]) + '\n')
    graph = original_graph