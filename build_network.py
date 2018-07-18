from Dijkstra import Graph
import csv
import time
import datetime
import collections
def build_graph():
    graph = Graph()
    # add nodes and edges of consecutive subway stations
    subway_id = set()
    with open('data/subway_pair_traveltime.csv') as f:
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
            graph.add_edge(start, end, t, 'subway route ' + r_id)

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

    # add edges from each taxi station to its nearest 5 subway stations
    with open('data/closest_subway_stations_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            t_id = row[0]
            graph.add_node(t_id)
            for i in range(5):
                st, t = (row[2*i+1], float(row[2*i+2]))
                graph.add_edge(t_id, st+'N', t, 'walk')
                graph.add_edge(t_id, st+'S', t, 'walk')
                graph.add_edge(st+'N', t_id, t, 'walk')
                graph.add_edge(st+'S', t_id, t, 'walk')

    # add nodes and edges of consecutive bus stations
    with open('data/bus_pair_traveltime.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            r_id = row[0]
            start = row[1]
            end = row[2]
            bus_id.add(start)
            bus_id.add(end)
            x = time.strptime(row[3],'%H:%M:%S')
            t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            graph.add_node(start)
            graph.add_node(end)
            graph.add_edge(start, end, t, 'bus ' + r_id)

    # add edges from each bus stop to its nearest 5 subway stations
    with open('data/closest_subway_to_bus.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = row[0]
            for i in range(5):
                st, t = (row[2*i+1], float(row[2*i+2]))
                graph.add_edge(id, st+'N', t, 'walk')
                graph.add_edge(id, st+'S', t, 'walk')
                graph.add_edge(st+'N', id, t, 'walk')
                graph.add_edge(st+'S', id, t, 'walk')
    return graph

    # add edges from each subway stop to its nearest 5 bus stations
    with open('data/closest_bus_to_subway.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            id = row[0]
            for i in range(5):
                st, t = row[2*i+1], float(row[2*i+2])
                graph.add_edge(st, id+'N', t, 'walk')
                graph.add_edge(st, id+'S', t, 'walk')
                graph.add_edge(id+'N', st, t, 'walk')
                graph.add_edge(id+'S', st, t, 'walk')

    # add edges from each taxi station to its nearest 5 bus stations
    with open('data/closest_bus_stations_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            t_id = row[0]
            for i in range(5):
                st, t = (row[2*i+1], float(row[2*i+2]))
                graph.add_edge(t_id, st, t, 'walk')
                graph.add_edge(st, t_id, t, 'walk')







    # taxi station to subway (bike)
    with open('data/biketime_between_taxi_and_subway_label.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row[1] in id_to_nodes:
                continue
            for node in id_to_nodes[row[1]]:
                try:
                    s = str(int(float(row[4])))
                    e = str(int(float(row[3])))
                    graph.add_edge(row[0],node,float(row[2]), 'bike from '+s+' to '+e)
                    graph.add_edge(node,row[0],float(row[2]), 'bike from '+e+' to '+s)
                except:
                    continue

    # taxi station to taxi station by walk and bike
    with open('data/taxi_to_taxi_label.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                s = str(int(float(row[4])))
                e = str(int(float(row[3])))
                if row[3] == None:
                    graph.add_edge(row[0],row[1],float(row[2]),'walk')
                    graph.add_edge(row[1],row[0],float(row[2]),'walk')
                else:
                    graph.add_edge(row[0],row[1],float(row[2]),'bike from '+e+' to '+s)
                    graph.add_edge(row[1],row[0],float(row[2]),'bike from '+s+' to '+e)
            except:
                continue
