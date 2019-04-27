"""
@project: RoutingAlgorithm
@author: sam
@file widest_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:36:52
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm import *
from itertools import chain
from networkx.utils import pairwise
from copy import deepcopy

__all__ = [
    'generate_widest_steiner_trees',
]


def generate_widest_steiner_trees(G, flows):
    """
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    # Initialize widest_steiner_trees
    widest_steiner_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Compute the origin_T
        origin_T = generate_widest_steiner_tree(graph, f['src'], f['dst'])
        # Add origin_T into widest_steiner_trees
        widest_steiner_trees.append(origin_T)

        # Compute all paths in origin_T
        all_paths = nx.shortest_path(origin_T, f['src'])
        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from src to dst
            path = all_paths[dst]
            # Check whether the path valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record the path
                f['dst'][dst] = path
                # Add path into allocated_T
                allocated_T.add_path(path)
        # Update the information of graph
        update_topo_info(G, allocated_T, f['size'])

    return graph, allocated_flows, widest_steiner_trees


def generate_widest_steiner_tree(G, source, destinations):
    """According to the source and destinations, generate Widest Steiner Tree
    :param G: The origin graph
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
    all_pair_paths = all_pair_widest_shortest_paths(G)
    # While terminals isn't empty
    while terminals:
        # Initialize path
        path = None
        # Traverse all terminals
        for v in terminals:
            # Get the widest shortest path from v to constructed tree
            p = widest_shortest_path_to_tree(G, v, T, all_pair_paths)
            # Update path
            if path is None or (path is not None and len(p) < len(path)) or \
                    (path is not None and len(p) == len(path) and
                     compute_path_minimum_bandwidth(G, p) >
                     compute_path_minimum_bandwidth(G, path)):
                path = p
        # Add path into T
        T.add_path(path)
        # Remove the terminal node in current path
        terminals.remove(path[-1])

        # Remove the terminals already in T
        v_d = set()
        for v in terminals:
            if v in T.nodes:
                v_d.add(v)
        terminals = terminals - v_d

    return T


def widest_shortest_path_to_tree(G, target, tree, all_pair_paths):
    """Compute the widest shortest path from target to constructed tree
    :param G: The origin graph
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
        all_pair_paths[v] = generate_widest_shortest_path(G, v)

    return all_pair_paths
