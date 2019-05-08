"""
@project: RoutingAlgorithm
@author: sam
@file widest_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:36:52
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *
from algorithm.widest_shortest_path_tree import *

__all__ = [
    'WidestSteinerTree'
]


class WidestSteinerTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        super().__init__(G, flows, **kwargs)

        self.deploy()

    def compute(self, source, destinations, **kwargs):
        """WST
        :param source: The source of flow request
        :param destinations: The destinations of flow request
        :return: Widest Steiner Tree
        """
        # Initialize T
        T = nx.Graph()
        T.add_node(source)
        T.root = source
        # Initialize terminals
        terminals = set(destinations)
        # Compute all pair widest shortest paths
        all_pair_paths = self.__all_pair_widest_shortest_paths()
        # While terminals isn't empty
        while terminals:
            # Initialize path
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the widest shortest path from constructed tree to v
                p = self.__widest_shortest_path_from_tree(v, T, all_pair_paths)
                # Update path
                if path is None or (path is not None and len(p) < len(path)) or \
                        (path is not None and len(p) == len(path) and
                         compute_path_minimum_bandwidth(self.graph, p) >
                         compute_path_minimum_bandwidth(self.graph, path)):
                    path = p
            # Add path into T
            nx.add_path(T, path)
            # Remove the terminal node in current path
            terminals.remove(path[-1])

            # Remove the terminals already in T
            v_d = set()
            for v in terminals:
                if v in T.nodes:
                    v_d.add(v)
            terminals = terminals - v_d

        return T

    @classmethod
    def __widest_shortest_path_from_tree(cls, target, tree, all_pair_paths):
        """Compute the widest shortest path from constructed tree to target
        :param target: The target node needs to be added into the tree
        :param tree: The constructed tree
        :param all_pair_paths: All pair widest shortest paths in graph
        :return: path
        """
        # Initialize path
        path = None
        # Traverse all nodes in tree
        for v in tree.nodes:
            # Get the widest shortest path from v to target
            p = all_pair_paths[v][target]
            # Update path
            if path is None or (path is not None and len(p) < len(path)):
                path = p

        return path

    def __all_pair_widest_shortest_paths(self):
        """Compute all pair widest shortest paths
        :return: all_pair_paths
        """
        all_pair_paths = {}

        for v in self.graph.nodes:
            all_pair_paths[v] = widest_shortest_path(self.graph, v)

        return all_pair_paths
