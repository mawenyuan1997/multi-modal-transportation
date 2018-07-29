from Dijkstra import *
from build_network import *
import collections
class Edge_graph(Graph):
    def __init__(self, graph):
        Graph.__init__(self)
        self.node_set = collections.defaultdict(list)
        for (u, v), dist in graph.distances.items():
            self.add_node(u + '->' + v)
            self.node_set[v].append(u + '->' + v)
        for v in graph.nodes:
            for uv in self.node_set[v]:
                for w in graph.edges[v]:
                    print(uv,w)
                    from_node = uv
                    to_node = v + '->' + w
                    time = graph.distances[v, w]
                    # add bus/subway transfer time
                    x = uv.find('-')
                    pt, pr = self.check_route(graph.labels[uv[:x], v])
                    t, r = self.check_route(graph.labels[v, w])
                    time += self.waiting_time(pt, pr, t, r)
                    self.add_edge(from_node, to_node, time, graph.labels[v, w])

    # return the subway/bus route of an edge
    def check_route(self, label):
        p = label.find(' ')
        if p < 0:
            return label, 'no route'
        return (label[:p], label[p + 1:])

    def waiting_time(self, pt, pr, t, r):
        subway_route = ['1','2','3','4','5','5X','6','6X','7','7X','GS','A','B','C','D','E',
                        'F','FS','G','J','L','M','N','Q','R','H','W','Z','SI']
        subway_day = [20,8,8,8,12,12,10,8,5,5,5,8,10,10,10,
                    12,12,10,10,10,5,12,10,10,20,15,10,10,30]
        subway_time = dict(zip(subway_route, subway_day))

        if (pt, t) == ('walk', 'subway') or (pt, t) == ('subway', 'subway') and pr != r:
            return subway_time[r] / 2 * 60
        elif (pt, t) == ('walk', 'lirr') or (pt, t) == ('lirr', 'lirr') and pr != r:
            return 600
        elif (pt, t) == ('walk', 'bus') or (pt, t) == ('bus', 'bus') and pr != r:
            return 300
        return 0
