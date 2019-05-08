"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
@ide: PyCharm
@time: 2019-03-01 14:33:05
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *

__all__ = [
    'ShortestPathTree'
]


class ShortestPathTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        """
        :param G:
        :param flows:
        :param kwargs:
        """
        super().__init__(G, flows, **kwargs)

        self.all_pair_paths = nx.shortest_path(self.graph)

        self.deploy(**kwargs)

    def compute(self, source, destinations, **kwargs):
        """
        :param source: The source node of flow request
        :param destinations: The destinations of flow request
        :param kwargs:
        :return: Shortest Path Tree
        """
        # Initialize T
        T = nx.DiGraph()
        T.root = source
        # Traverse all destinations
        for dst in destinations:
            # If dst is already in T
            if dst in T.nodes:
                continue
            # Get the shortest path from source to dst
            path = self.all_pair_paths[source][dst]
            # Add path into T
            nx.add_path(T, path)

        return T

