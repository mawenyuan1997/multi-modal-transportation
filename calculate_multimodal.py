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
print('original graph nodes:'+str(len(graph.nodes)))
print('original graph edges:'+str(len(graph.distances)))
with open('data/multimodal.csv', 'w') as file:
    file.write('origin,destination,time\n')
    for id1 in range(1,264):
        origin = 'taxi_' + str(id1)
        length, path, route = dijkstra(graph, origin)
        for id2 in range(1,264):
            if id1 != id2 and (str(id1),str(id2)) in taxi_time:
                dest = 'taxi_' + str(id2)
                time = length[dest]
                file.write(str(id1) + ',' + str(id2) + ',' + str(time) + '\n')
                print(str(id1) + ',' + str(id2) + ',' + str(time))
                # x = str(id2)
                # shortest_path = [x]
                # route_time = []
                # route_type = []
                # while x != str(id1):
                #     shortest_path.append(path[x])
                #     route_time.append(graph.distances[path[x],x])
                #     if x=='132' and route[x]=='walk':
                #         route_type.append('airtrain')
                #     else:
                #         route_type.append(route[x])
                #     x = path[x]
                # shortest_path.reverse()
                # route_time.reverse()
                # route_type.reverse()
                # print(shortest_path)
                # print(route_time)
                # file.write(str(shortest_path) + '\n')
                # file.write(str(route_time) + '\n')

        
# for (id1, id2), t1 in multi_time.items():
#     t2 = taxi_time[(id1, id2)]
#     if t2 < 12000 and t1 < 12000:
#         plt.scatter(t2, t1, color='b', s=0.7, alpha=0.7)
# t = np.arange(0., 6000, 1)
# plt.plot(t, t, 'r--')
# plt.xlabel('taxi time')
# plt.ylabel('multimodal time')
# plt.show()
