# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 20:34:19 2018

@author: liumo
"""


import csv
import time
import datetime
import collections
from Dijkstra import shortest_path, dijkstra
from build_network import build_graph,modify_edges
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy

#station=pd.read_csv('data/bikeStation_coordinates.csv')
#change the times of iteration and top here
iteration=5
top=10
result= {}
bikeid = {}


biketime=pd.read_csv('data/edges/bike_pair_traveltime.csv')
biketime=biketime.set_index(['startid','endid'])

taxi_time = {}
with open('data/taxitime.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        s = str(int(float(row[0])))
        e = str(int(float(row[1])))
        if s not in ['264','265'] and e not in ['264','265'] and s!=e:
            taxi_time[s, e]=float(row[2])
            
# exclude the too long trips whose travel time is bigger than 1.2 times taxitime
multimodal = {}
with open('data/multimodal.csv') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        s = str(int(float(row[0])))
        e = str(int(float(row[1])))
        if s not in ['264','265'] and e not in ['264','265'] and s!=e:
            multimodal[s, e]=float(row[2]) 
            
multi_time = {}
count_bike = {}
graph = build_graph()
original_graph = deepcopy(graph)

for itera in range(iteration):
    for bi in bikeid:
        modify_edges(graph, bi)
    print(itera,'nodes:'+str(len(graph.nodes)))
    print(itera,'edges:'+str(len(graph.distances)))
    
    bike_pair = {}
    multitime=pd.DataFrame(columns=['origin','destination','time'])
    
    with open('data/bike_pair_times_'+str(top)+'_'+str(itera+1)+'.csv', 'w') as file:
        file.write('origin,destination,number_of_appearance\n')
        for id1 in range(1,264):
            length, path, route = dijkstra(graph, str('taxi_'+str(id1)))
            for id2 in range(1,264):
                if (id1 != id2) and ((str(id1),str(id2)) in taxi_time):
                    if multimodal[str(id1),str(id2)] < 1.2 * taxi_time[str(id1),str(id2)]:
                        print(itera,str(id1) + ',' + str(id2))
                        x = str('taxi_'+str(id2))
                        route_type = []
                        while x != str('taxi_'+str(id1)):
                            if x[:4]=='bike' and path[x][:4]=='bike':
                                d = x[5:]
                                o = path[x][5:]
                                if (o,d) in bike_pair:
                                    bike_pair[o,d] += 1
                                else:
                                    bike_pair[o,d] = 1
                            x = path[x]
                        multitime=multitime.append({'origin':id1,'destination':id2,'time':length[str('taxi_'+str(id2))]},ignore_index = True)
        for (o,d),t in bike_pair.items():
            file.write(o+','+d+','+str(t)+'\n')
    
    multitime.to_csv('data/iteration_times_'+str(top)+'_'+str(itera+1)+'.csv')    
    measure=pd.DataFrame(columns=['startid','endid','totaltime'])

    times=pd.read_csv('data/bike_pair_times_'+str(top)+'_'+str(itera+1)+'.csv')
    times=times.set_index(['origin','destination'])

    for (i,j) in times.index:
        measure=measure.append({'startid':i,'endid':j,'totaltime':(float(times.loc[(i,j),'number_of_appearance']) * float(biketime.loc[(i,j),'bikingtime'][:1]))},ignore_index=True)

    measurement=measure.groupby('startid').sum()
    measurement=measurement.sort_values('totaltime',ascending=False)
    result=measurement.head(top)
    del measurement['endid']
    measurement.to_csv('data/iteration_result_'+str(top)+'_'+str(itera+1)+'.csv')
    bikeid=list(result.index)
    
    bikeid = list(map(lambda x: str('bike_'+str(int(x))), bikeid))
    #measure=measure.set_index(['startid','endid'])
    graph = deepcopy(original_graph)
    print(itera,'result:',bikeid)




'''        
dist=pd.read_csv('data/bike_pair_dist.csv')
dist=dist.set_index(['origin','destination'])
longdist=dist[dist.distance>7750]

times=pd.read_csv('data/bike_pair_times_0.csv')
times=times.set_index(['origin','destination'])
'''