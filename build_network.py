from Dijkstra import Graph
import csv
import time
import datetime
import collections
import os.path

def build_graph():
    graph = Graph()
    add_subway_pair(graph)
    add_bus_pair(graph)
    add_taxi_od(graph)
    add_bike_pair(graph)
    add_lirr_pair(graph)
    add_edges_of_closest_stations(graph)
    add_airport_express(graph)
    add_waiting_time(graph)
    return graph

def add_taxi_od(graph):
    with open('data/taxi_zone_lookup.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[0]) < 264:
                graph.add_node('taxi_' + row[0])
                graph.node_set['taxi_' + row[0]].add('taxi_' + row[0])

    with open('data/edges/taxi_bike_walking.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            start = 'taxi_' + row[0]
            end = 'taxi_' + row[1]
            try:
                t = float(row[4])
            except:
                continue
            if start == end or row[4]=='': continue
            graph.add_edge(start, end, t, 'walk')

def add_subway_pair(graph):
    # add nodes and edges of consecutive subway stations
    subway_id = set()
    with open('data/edges/subway_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = 'subway_' + r_id + '_' + row[1]
            end = 'subway_' + r_id + '_' + row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
            graph.node_set['subway_' + row[1][:-1]].add(start)
            graph.node_set['subway_' + row[2][:-1]].add(end)
            graph.add_edge(start, end, t, 'subway ' + r_id)

    # add edges for transfers between different subway routes
    with open('data/subway_gtfs/transfers.txt') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id1, id2 = 'subway_' + row[0], 'subway_' + row[1]
            t = int(row[3])
            if id1 != id2:
                for from_id in graph.node_set[id1]:
                    for to_id in graph.node_set[id2]:
                        graph.add_edge(from_id, to_id, t, 'transfer')
                        graph.add_edge(to_id, from_id, t, 'transfer')

def add_bus_pair(graph):
    # add nodes and edges of consecutive bus stations
    with open('data/edges/bus_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = 'bus_' + r_id + '_' + row[1]
            end = 'bus_' + r_id + '_' + row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
            graph.node_set['bus_'+row[1]].add(start)
            graph.node_set['bus_'+row[2]].add(end)
            graph.add_edge(start, end, t, 'bus ' + r_id)

def add_bike_pair(graph):
    # add nodes and edges of common pair of bike stations
    with open('data/edges/bike_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            start = 'bike_' + row[1]
            end = 'bike_' + row[2]
            if start == end or row[3]=='': continue
            t = float(row[3])
            graph.add_node(start)
            graph.add_node(end)
            graph.node_set[start].add(start)
            graph.node_set[end].add(end)
            graph.add_edge(start, end, t, 'bike')

def add_lirr_pair(graph):
    # add nodes and edges of consecutive lirr stations
    with open('data/edges/lirr_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = 'lirr_' + r_id + '_' + row[1]
            end = 'lirr_' + r_id + '_' + row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
            graph.node_set['lirr_'+row[1]].add(start)
            graph.node_set['lirr_'+row[2]].add(end)
            graph.add_edge(start, end, t, 'lirr ' + r_id)


def add_edges_of_closest_stations(graph):
    # add edges from each taxi station to its nearest 5 subway stations
    transport = ['subway','bus','lirr','taxi','bike']
    for tr1 in transport:
        for tr2 in transport:
            filename = 'data/edges/closest_' + tr1 + '_to_' + tr2 + '.csv'
            if not os.path.isfile(filename) or tr1 == tr2: continue
            #print(tr1,tr2)
            with open(filename) as f:
                reader=csv.reader(f)
                next(reader)
                for row in reader:
                    for from_id in graph.node_set[tr2 + '_' + row[0]]:
                        for i in range(5):
                            if row[2*i+1] == 'null': break
                            st_id, t = (tr1 + '_' + row[2*i+1], float(row[2*i+2]))
                            for to_id in graph.node_set[st_id]:
                                t1 = t + waiting_time(to_id) if tr1 in ['subway', 'bus', 'lirr'] else t
                                t2 = t + waiting_time(from_id) if tr2 in ['subway', 'bus', 'lirr'] else t
                                graph.add_edge(from_id, to_id, t1, 'walk')
                                graph.add_edge(to_id, from_id, t2, 'walk')
    transport1 = ['subway','bus','lirr','bike']
    for tr1 in transport1:
            tr2 = 'taxi'
            filename = 'data/edges/closest_' + tr1 + '_to_' + tr2 + '1.csv'
            if not os.path.isfile(filename) or tr1 == tr2: continue
            #print(tr1,tr2)
            with open(filename) as f:
                reader=csv.reader(f)
                next(reader)
                for row in reader:
                    #print(row[0])
                    for from_id in graph.node_set[tr2 + '_' + row[0]]:
                        for i in range(500):
                            if row[2*i+1] == 'null': break
                            #print(i,row[2*i+1],row[2*i+2])
                            st_id, t = (tr1 + '_' + row[2*i+1], float(row[2*i+2]))
                            for to_id in graph.node_set[st_id]:
                                t1 = t + waiting_time(to_id) if tr1 in ['subway', 'bus', 'lirr'] else t
                                t2 = t + waiting_time(from_id) if tr2 in ['subway', 'bus', 'lirr'] else t
                                graph.add_edge(from_id, to_id, t1, 'walk')
                                graph.add_edge(to_id, from_id, t2, 'walk')
                                
                                
                                


def add_airport_express(graph):
    graph.add_node('port_authority')
    graph.add_node('byrant_park')
    graph.add_node('grand_central')
    graph.add_edge('port_authority', 'taxi_1', 3000, 'airport express')
    graph.add_edge('taxi_1', 'port_authority', 3000, 'airport express')
    graph.add_edge('byrant_park', 'taxi_1', 3600, 'airport express')
    graph.add_edge('taxi_1', 'byrant_park', 3600, 'airport express')
    graph.add_edge('grand_central', 'taxi_1', 4200, 'airport express')
    graph.add_edge('taxi_1', 'grand_central', 4200, 'airport express')
    graph.add_edge('grand_central', 'taxi_138', 1800, 'airport express')
    graph.add_edge('taxi_138', 'grand_central', 1800, 'airport express')
    graph.add_edge('taxi_1','taxi_138', 3000, 'airport express')
    graph.add_edge('taxi_138', 'taxi_1', 3000, 'airport express')
    graph.add_edge('taxi_132','taxi_138', 2400, 'airport express')
    graph.add_edge('taxi_138', 'taxi_132',2400, 'airport express')
    with open('data/edges/Newark_express_stations.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row[1]) == 6:
                s, e = row[0], 'bus_' + row[1]
            elif len(row[1]) == 4:
                s, e = row[0], 'subway_' + row[1][:-1]
            else:
                s, e = row[0], row[1]
            for to_node in graph.node_set[e]:
                graph.add_edge(s, to_node, 300, 'walk')
                graph.add_edge(to_node, s, 300, 'walk')

def modify_edges(graph, bike_id):
    for edge in graph.edges[bike_id]:
        if edge[:4] == 'bike':
            graph.distances[bike_id, edge] *= 2/3

def add_waiting_time(graph):
    for node, nodeset in graph.node_set.items():
        if len(nodeset) > 1:
            for id1 in nodeset:
                for id2 in nodeset:
                    if id1 != id2:
                        graph.add_edge(id1, id2, waiting_time(id2), 'transfer')

def waiting_time(st_id):
    subway_route = ['1','2','3','4','5','5X','6','6X','7','7X','GS','A','B','C','D','E',
                        'F','FS','G','J','L','M','N','Q','R','H','W','Z','SI']
    subway_day = [20,8,8,8,12,12,10,8,5,5,5,8,10,10,10,
                    12,12,10,10,10,5,12,10,10,20,15,10,10,30]
    subway_time = dict(zip(subway_route, subway_day))
    p = st_id.split('_')
    if p[0] == 'subway':
        return subway_time[p[1]] / 2 * 60
    elif p[0] == 'bus':
        return (10/2 * 60 if p[1][0] == 'M' else 20/2 * 60)
    else:
        return 600
