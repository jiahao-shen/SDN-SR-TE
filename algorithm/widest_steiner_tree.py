"""
@project: RoutingAlgorithm
@author: sam
@file widest_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:36:52
@blog: https://jiahaoplus.com
"""
import math
from networkx.utils import pairwise
from network import *
from algorithm.multicast_tree import *
from algorithm.widest_shortest_path_tree import *

__all__ = [
    'WidestSteinerTree',
    'widest_shortest_path_from_tree',
    'all_pair_widest_shortest_paths',
    'compute_path_minimum_bandwidth'
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
        all_pair_paths = all_pair_widest_shortest_paths(self.graph)
        # While terminals isn't empty
        while terminals:
            # Initialize path
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the widest shortest path from constructed tree to v
                p = widest_shortest_path_from_tree(v, T, all_pair_paths)
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


def widest_shortest_path_from_tree(target, tree, all_pair_paths):
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


def all_pair_widest_shortest_paths(G):
    """Compute all pair widest shortest paths
    :param G: The origin graph
    :return: all_pair_paths
    """
    all_pair_paths = {}

    for v in G.nodes:
        all_pair_paths[v] = widest_shortest_path(G, v)

    return all_pair_paths


def compute_path_minimum_bandwidth(G, path):
    """Compute the minimum bandwidth during the path
    :param G: The origin path
    :param path: The path in G
    :return: minimum_bandwidth
    """
    minimum_bandwidth = math.inf
    for v, u in pairwise(path):
        minimum_bandwidth = min(minimum_bandwidth,
                                G[v][u]['residual_bandwidth'])

    return minimum_bandwidth
