import csv
import time
import datetime
import collections
from Dijkstra import shortest_path
from build_network import build_graph
import sys, os
origin, dest = '45', '132'
graph = build_graph()
length, route, route_type = shortest_path(graph, origin, dest)
print(length)
print(route)
print(route_type)

#te

import pandas as pd

k=sys.stdout 
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    sys.stdout = k
    
    
result=pd.DataFrame(columns=['origin','destination','length'])
i=132
for j in range(263):
        blockPrint()
        origin, dest = str(i+1), str(j+1)
        length, route, route_type = shortest_path(graph, origin, dest)
        result=result.append({'origin':i,'destination':j,'length':length},ignore_index=True)
        enablePrint()
        print(j)
        