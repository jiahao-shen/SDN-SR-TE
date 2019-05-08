"""
@project: RoutingAlgorithm
@author: sam
@file steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:36:05
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *

__all__ = [
    'SteinerTree',
    'shortest_path_from_tree'
]


class SteinerTree(MulticastTree):

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
        :return: Steiner Tree
        """
        # Initialize T
        T = nx.DiGraph()
        T.add_node(source)
        T.root = source
        # Initialize terminals
        terminals = set(destinations)
        # While terminals isn't empty
        while terminals:
            # Initialize path
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the shortest path from constructed tree to v
                p = shortest_path_from_tree(v, T, self.all_pair_paths)
                # Update path
                if path is None or (path is not None and len(p) < len(path)):
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


def shortest_path_from_tree(target, tree, all_pair_paths):
    """Compute the shortest path from constructed tree to target
    :param target: The target node needs to be added into the tree
    :param tree: The constructed tree
    :param all_pair_paths: Shortest paths between any two nodes
    :return: path
    """
    # Initialize path
    path = None
    # Traverse all nodes in tree
    for v in tree.nodes:
        # Get the shortest path from v to target
        p = all_pair_paths[v][target]
        # Update the path
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path
