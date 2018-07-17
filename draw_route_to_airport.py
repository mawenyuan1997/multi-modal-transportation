import csv
import time
import datetime
import collections
from Dijkstra import shortest_path
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
subway_loc = {}
with open('data/subway_gtfs.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
multi_time = {}
for (id1, id2), ti in taxi_time.items():
    if id2 in ['132','1','138']:
        multi_time[id1,id2], path, route_type = shortest_path(id1,id2)
        if multi_time[id1,id2] < taxi_time[id1,id2]:
