from Dijkstra import Graph
import csv
import time
import datetime
import collections

def build_graph():
    graph = Graph()
    add_subway_pair(graph)
    add_bus_pair(graph)
    add_taxi_od(graph)
    add_bike_pair(graph)
    add_lirr_pair(graph)
    add_closest_subway_to_taxi(graph)
    add_closest_subway_to_bus(graph)
    add_closest_subway_to_bike(graph)
    add_closest_subway_to_lirr(graph)
    add_closest_bus_to_taxi(graph)
    # add_closest_bus_to_bus(graph)
    add_closest_bus_to_subway(graph)
    add_closest_bus_to_bike(graph)
    add_closest_bus_to_lirr(graph)
    add_closest_bike_to_taxi(graph)
    add_closest_bike_to_bus(graph)
    add_closest_bike_to_subway(graph)
    add_closest_bike_to_lirr(graph)
    add_closest_lirr_to_taxi(graph)
    add_closest_lirr_to_bus(graph)
    add_airport_express(graph)
    return graph

def add_taxi_od(graph):
    with open('data/taxi_zone_lookup.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[0]) < 264:
                graph.add_node('taxi_' + row[0])

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
            start = 'subway_' + row[1]
            end = 'subway_' + row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            subway_id.add(start)
            subway_id.add(end)
            graph.add_node(start)
            graph.add_node(end)
            graph.add_edge(start, end, t, 'subway ' + r_id)

    # add edges for transfers between different subway routes
    with open('data/subway_gtfs/transfers.txt') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id1, id2 = 'subway_' + row[0], 'subway_' + row[1]
            t = int(row[3])
            if id1 != id2:
                graph.add_edge(id1+'N',id2+'N',t,'transfer')
                graph.add_edge(id2+'N',id1+'S',t,'transfer')
                graph.add_edge(id2+'S',id1+'N',t,'transfer')
                graph.add_edge(id2+'S',id1+'S',t,'transfer')

    # add transfers between north and south directions
    for id in subway_id:
        if id[-1] == 'N':
            id1 = id[:-1] + 'S'
        else:
            id1 = id[:-1] + 'N'
        graph.add_edge(id, id1, 180, 'transfer')

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
            graph.node_set['bus_'+row[1]].append(start)
            graph.node_set['bus_'+row[2]].append(end)
            graph.add_edge(start, end, t, 'bus ' + r_id)
            graph.add_edge(end, start, t, 'bus ' + r_id)

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
            graph.add_edge(start, end, t*0.8, 'bike')

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
            graph.node_set['lirr_'+row[1]].append(start)
            graph.node_set['lirr_'+row[2]].append(end)
            graph.add_edge(start, end, t, 'lirr ' + r_id)


def add_closest_subway_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 subway stations
    with open('data/edges/closest_subway_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            t_id = 'taxi_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('subway_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(t_id, st+'N', t, 'walk')
                graph.add_edge(t_id, st+'S', t, 'walk')
                graph.add_edge(st+'N', t_id, t, 'walk')
                graph.add_edge(st+'S', t_id, t, 'walk')

def add_closest_subway_to_bus(graph):
    # add edges from each bus stop to its nearest 5 subway stations
    with open('data/edges/closest_subway_to_bus.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            for id in graph.node_set['bus_' + row[0]]:
                for i in range(5):
                    if row[2*i+1] == 'null': break
                    st, t = ('subway_' + row[2*i+1], float(row[2*i+2]))
                    graph.add_edge(id, st+'N', t, 'walk')
                    graph.add_edge(id, st+'S', t, 'walk')
                    graph.add_edge(st+'N', id, t, 'walk')
                    graph.add_edge(st+'S', id, t, 'walk')

def add_closest_subway_to_bike(graph):
    # add edges from each bike stop to its nearest 5 subway stations
    with open('data/edges/closest_subway_to_bike.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = 'bike_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('subway_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(id, st+'N', t, 'walk')
                graph.add_edge(id, st+'S', t, 'walk')
                graph.add_edge(st+'N', id, t, 'walk')
                graph.add_edge(st+'S', id, t, 'walk')

def add_closest_subway_to_lirr(graph):
    # add edges from each lirr stop to its nearest 5 subway stations
    with open('data/edges/closest_subway_to_lirr.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = 'lirr_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('subway_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(id, st+'N', t, 'walk')
                graph.add_edge(id, st+'S', t, 'walk')
                graph.add_edge(st+'N', id, t, 'walk')
                graph.add_edge(st+'S', id, t, 'walk')

def add_closest_bus_to_subway(graph):
    # add edges from each subway stop to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_subway.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = 'subway_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'bus_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id+'N', t, 'walk')
                graph.add_edge(st, id+'S', t, 'walk')
                graph.add_edge(id+'N', st, t, 'walk')
                graph.add_edge(id+'S', st, t, 'walk')

def add_closest_bus_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            t_id = 'taxi_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('bus_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(t_id, st, t, 'walk')
                graph.add_edge(st, t_id, t, 'walk')

def add_closest_bus_to_bus(graph):
    # add edges from each bus station to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_bus.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            b_id = 'bus_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('bus_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(b_id, st, t, 'walk')
                graph.add_edge(st, b_id, t, 'walk')

def add_closest_bus_to_bike(graph):
    # add edges from each bike station to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_bike.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            b_id = 'bike_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('bus_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(b_id, st, t, 'walk')
                graph.add_edge(st, b_id, t, 'walk')

def add_closest_bus_to_lirr(graph):
    # add edges from each lirr station to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_lirr.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = 'lirr_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = ('bus_' + row[2*i+1], float(row[2*i+2]))
                graph.add_edge(id, st, t, 'walk')
                graph.add_edge(st, id, t, 'walk')

def add_closest_bike_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 bike stations
    with open('data/edges/closest_bike_to_taxi.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = 'taxi_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'bike_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

def add_closest_bike_to_bus(graph):
    # add edges from each bus station to its nearest 5 bike stations
    with open('data/edges/closest_bike_to_bus.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = 'bus_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'bike_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

def add_closest_bike_to_subway(graph):
    # add edges from each subway stop to its nearest 5 bike stations
    with open('data/edges/closest_bike_to_subway.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = 'subway_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'bike_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id+'N', t, 'walk')
                graph.add_edge(st, id+'S', t, 'walk')
                graph.add_edge(id+'N', st, t, 'walk')
                graph.add_edge(id+'S', st, t, 'walk')

def add_closest_bike_to_lirr(graph):
    # add edges from each lirr station to its nearest 5 bike stations
    with open('data/edges/closest_bike_to_lirr.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = 'lirr_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'bike_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

def add_closest_lirr_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 lirr stations
    with open('data/edges/closest_lirr_to_taxi.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = 'taxi_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'lirr_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

def add_closest_lirr_to_bus(graph):
    # add edges from each bus station to its nearest 5 lirr stations
    with open('data/edges/closest_lirr_to_bus.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = 'bus_' + row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'lirr_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

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
                s, e = row[0], 'subway_' + row[1]
            else:
                s, e = row[0], row[1]
            graph.add_edge(s, e, 300, 'walk')
            graph.add_edge(e, s, 300, 'walk')

def modify_edges(graph, bike_id):
    for edge in graph.edges[bike_id]:
        if edge[:4] == 'bike':
            graph.distances[bike_id, edge] *= 0.8
