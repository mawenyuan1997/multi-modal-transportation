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
multi_time = {}
for (id1, id2), ti in taxi_time.items():
    # multi_time[id1,id2], path, route_type = shortest_path(id1,id2)
    multi_time[id1,id2] = 5000+int(id1)

for (id1, id2), t1 in multi_time.items():
    t2 = taxi_time[(id1, id2)]
    if t2 < 12000 and t1 < 12000:
        plt.scatter(t2, t1, color='b', s=0.7, alpha=0.7)
t = np.arange(0., 6000, 1)
plt.plot(t, t, 'r--')
plt.xlabel('taxi time')
plt.ylabel('subway+bike time')
plt.show()
