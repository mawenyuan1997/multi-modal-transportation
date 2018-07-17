from Dijkstra import Graph
import csv
import time
import datetime
import collections
def build_graph():
    graph = Graph()
    # add nodes and edges of consecutive subway stations
    with open('data/subway_pair_traveltime.csv') as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
        r_id = row[0][0]
        start = r_id + '_' + row[1]
        end = r_id + '_' + row[2]
        x = time.strptime(row[3],'%H:%M:%S')
        t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        graph.add_node(start)
        graph.add_node(end)
        graph.add_edge(start, end, t, 'subway')

    # add edges for transfers between different routes
    with open('data/subway_gtfs/transfers.txt') as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
        id1, id2 = row[0][0]+'_'+row[0], row[1][0]+'_'+row[1]
        t = int(row[3])
        if id1 != id2:
            graph.add_edge(id1+'N',id2+'N',t,'transfer')
            graph.add_edge(id2+'N',id1+'S',t,'transfer')
            graph.add_edge(id2+'S',id1+'N',t,'transfer')
            graph.add_edge(id2+'S',id1+'S',t,'transfer')

    # add transfers between north and south directions
    for id1 in graph.nodes:
        for id2 in graph.nodes:
            x = id1.find('_') + 1
            if id1 != id2 and (id1[x:-1] == id2[x:-1]):
                graph.add_edge(id1,id2,180,'transfer')

    taxi_time = {}
    with open('data/taxitime.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            s = str(int(float(row[0])))
            e = str(int(float(row[1])))
            if s not in ['264','265'] and e not in ['264','265'] and s!=e:
                taxi_time[s, e]=float(row[2])

# add edges from each taxi station to its nearest 5 subway stations
    closest_st = {}
    with open('data/closest_subway_stations_to_taxi.csv') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            closest_st[row[0]] = []
            for i in range(5):
                closest_st[row[0]].append((row[2*i+1], float(row[2*i+2])))
    id_to_nodes = {}
    for i in graph.nodes:
        x = i.find('_') + 1
        if i[x:-1] in id_to_nodes:
            id_to_nodes[i[x:-1]].append(i)
        else:
            id_to_nodes[i[x:-1]] = [i]
    # taxi station to subway (walk)
    multi_time = {}
    for (id1, id2), ti in taxi_time.items():
        graph.add_node(id1)
        graph.add_node(id2)
        for st, t in closest_st[id1]:
            if not st in id_to_nodes:
                continue
            for near in id_to_nodes[st]:
                graph.add_edge(id1, near, t, 'walk')

        for st, t in closest_st[id2]:
            if not st in id_to_nodes:
                continue
            for near in id_to_nodes[st]:
                graph.add_edge(near, id2, t, 'walk')

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
    return graph
