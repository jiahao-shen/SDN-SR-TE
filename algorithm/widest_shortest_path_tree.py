"""
@project: RoutingAlgorithm
@author: sam
@file widest_shortest_path_tree.py
@ide: PyCharm
@time: 2019-03-01 14:34:41
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *
import math

__all__ = [
    'WidestShortestPathTree',
    'widest_shortest_path'
]


class WidestShortestPathTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        """
        :param G:
        :param flows:
        :param kwargs:
        """
        super().__init__(G, flows, **kwargs)

        self.deploy(**kwargs)

    def compute(self, source, destinations, **kwargs):
        """
        :param source: The source of flow request
        :param destinations: The destinations of flow request
        :return: Widest Shortest Path Tree
        """
        # Initialize T
        T = nx.DiGraph()
        T.root = source
        # Generate all pair widest shortest paths
        all_pair_paths = widest_shortest_path(self.graph, source)
        # Traverse all destinations
        for dst in destinations:
            # If dst is already in T
            if dst in T.nodes:
                continue
            # Get the widest shortest path from source to dst
            path = all_pair_paths[dst]
            # Add path into T
            nx.add_path(T, path)

        return T


def widest_shortest_path(G, source, widest_attribute='residual_bandwidth'):
    """Compute all widest shortest path from source to other nodes in G
    Using Extension Dijkstra Algorithm
    :param G: The origin graph
    :param source: The source node
    :param widest_attribute: The attribute for widest path
    :return: paths
    """
    # Dict to store the paths
    paths = {source: [source]}
    # The next traverse
    next_level = {source: 1}
    # Dict to store the minimum bandwidth from source to current node
    minimum_bandwidth = {}
    # Initialize minimum bandwidth for all nodes
    for v in G.nodes:
        minimum_bandwidth[v] = math.inf
    # While not empty
    while next_level:
        this_level = next_level
        next_level = {}
        # Traverse current level
        for v in this_level:
            # Traverse all neighbor nodes of v
            for u in G.neighbors(v):
                # if w hasn't been visited
                if u not in paths:
                    # Record the path for w
                    paths[u] = paths[v] + [u]
                    # Record the minimum bandwidth of w
                    minimum_bandwidth[u] = min(minimum_bandwidth[v],
                                               G[v][u][widest_attribute])
                    # Put w into the next traverse
                    next_level[u] = 1
                # If w has been visited, and the current path length equals
                # the shortest path length and the current minimum bandwidth
                # less than the shortest path
                elif u in paths and len(paths[u]) == len(paths[v] + [u]) and \
                        min(minimum_bandwidth[v], G[v][u][widest_attribute]) \
                        > minimum_bandwidth[u]:
                    # Update the shortest path
                    paths[u] = paths[v] + [u]
                    # Update the minimum bandwidth
                    minimum_bandwidth[u] = min(minimum_bandwidth[v],
                                               G[v][u][widest_attribute])

    return paths
