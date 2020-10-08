import os
import pprint
import typing

from time import perf_counter
from termcolor import colored

pp = pprint.PrettyPrinter(indent=2)
t_start = perf_counter()
script_dir = os.path.dirname(__file__)

# Get a simple adjacency list built from the nodes in the csv file
# The method assumes the lines follow this patter: u (vertice),v (vertice),w (weight)
def get_adj_list(f: typing.TextIO) -> dict:
    graph = {}
    with f as lines:
        for node_str in lines:
            props = node_str.strip().split(',')
            u = props[0]
            v = props[1]
            if graph.get(u) is not None:
                graph[u].add(v)
            else:
                graph[u] = set()
                graph[u].add(v)
    return graph

# Main
nodes_stream = open(os.path.join(script_dir, './data/test2.csv'))
graph = get_adj_list(nodes_stream)

pp.pprint(graph)

t_end = perf_counter()
t_total = (t_end-t_start)*1000
print(colored('Elapsed Time, ', 'green'), '{:.2f} ms'.format(t_total))