from Dijkstra import Graph
import csv
import time
import datetime
import collections

def build_graph():
    graph = Graph()
    add_taxi_od(graph)
    add_subway_pair(graph)
    add_bus_pair(graph)
    add_bike_pair(graph)
    add_lirr_pair(graph)
    add_closest_subway_to_taxi(graph)
    add_closest_subway_to_bus(graph)
    add_closest_bus_to_taxi(graph)
    add_closest_bus_to_bus(graph)
    add_closest_bus_to_subway(graph)
    add_closest_bus_to_bike(graph)
    add_closest_bike_to_taxi(graph)
    add_closest_bike_to_bus(graph)
    add_closest_bike_to_subway(graph)
    add_closest_bike_to_lirr(graph)
    add_closest_bus_to_lirr(graph)
    add_closest_subway_to_lirr(graph)
    add_closest_lirr_to_taxi(graph)
    return graph

def add_taxi_od(graph):
    with open('data/taxi_zone_lookup.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[0]) < 264:
                graph.add_node(row[0])

def add_subway_pair(graph):
    # add nodes and edges of consecutive subway stations
    subway_id = set()
    with open('data/edges/subway_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = row[1]
            end = row[2]
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
            id1, id2 = row[0], row[1]
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
        graph.add_edge(id,id1,180,'transfer')

def add_bus_pair(graph):
    # add nodes and edges of consecutive bus stations
    with open('data/edges/bus_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = row[1]
            end = row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
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
            graph.add_edge(start, end, t, 'bike')


def add_lirr_pair(graph):
    # add nodes and edges of consecutive lirr stations
    with open('data/edges/lirr_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = 'lirr_' + row[1]
            end = 'lirr_' + row[2]
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
            graph.add_edge(start, end, t, 'lirr ' + r_id)


def add_closest_subway_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 subway stations
    with open('data/edges/closest_subway_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            t_id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = (row[2*i+1], float(row[2*i+2]))
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
            id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = (row[2*i+1], float(row[2*i+2]))
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
                st, t = (row[2*i+1], float(row[2*i+2]))
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
                st, t = (row[2*i+1], float(row[2*i+2]))
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
            id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = row[2*i+1], float(row[2*i+2])
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
            t_id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = (row[2*i+1], float(row[2*i+2]))
                graph.add_edge(t_id, st, t, 'walk')
                graph.add_edge(st, t_id, t, 'walk')

def add_closest_bus_to_bus(graph):
    # add edges from each bus station to its nearest 5 bus stations
    with open('data/edges/closest_bus_to_bus.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            b_id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = (row[2*i+1], float(row[2*i+2]))
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
                st, t = (row[2*i+1], float(row[2*i+2]))
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
                st, t = (row[2*i+1], float(row[2*i+2]))
                graph.add_edge(id, st, t, 'walk')
                graph.add_edge(st, id, t, 'walk')

def add_closest_bike_to_taxi(graph):
    # add edges from each taxi station to its nearest 5 bike stations
    with open('data/edges/closest_bike_to_taxi.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = row[0]
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
            id = row[0]
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
            id = row[0]
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
    # add edges from each lirr station to its nearest 5 bike stations
    with open('data/edges/closest_lirr_to_taxi.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = row[0]
            for i in range(5):
                if row[2*i+1] == 'null': break
                st, t = 'lirr_' + row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id, t, 'walk')
                graph.add_edge(id, st, t, 'walk')

def modify_edges(graph, bike_id):
    for edge in graph.edges[bike_id]:
        if edge[:4] == 'bike':
            graph.distances[bike_id, edge] *= 0.8
