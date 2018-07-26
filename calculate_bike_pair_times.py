import csv
import time
import datetime
import collections
from Dijkstra import shortest_path, dijkstra
from build_network import build_graph
import numpy as np
import matplotlib.pyplot as plt
taxi_time = {}
with open('data/taxitime.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        s = str(int(float(row[0])))
        e = str(int(float(row[1])))
        if s not in ['264','265'] and e not in ['264','265'] and s!=e:
            taxi_time[s, e]=float(row[2])
multi_time = {}
count_bike = {}
graph = build_graph()
print('nodes:'+str(len(graph.nodes)))
print('edges:'+str(len(graph.distances)))
bike_pair = {}
with open('data/bike_pair_times.csv', 'w') as file:
    file.write('origin,destination,number_of_appearance\n')
    for id1 in range(1,264):
        length, path, route = dijkstra(graph, str(id1))
        for id2 in range(1,264):
            if id1 != id2 and (str(id1),str(id2)) in taxi_time:
                print(str(id1) + ',' + str(id2))
                x = str(id2)
                route_type = []
                while x != str(id1):
                    if x[:4]=='bike' and path[x][:4]=='bike':
                        d = x[5:]
                        o = path[x][5:]
                        if (o,d) in bike_pair:
                            bike_pair[o,d] += 1
                        else:
                            bike_pair[o,d] = 1
                    x = path[x]
    for (o,d),t in bike_pair.items():
        file.write(o+','+d+','+str(t)+'\n')