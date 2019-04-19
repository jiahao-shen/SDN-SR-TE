"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
@ide: PyCharm
@time: 2019-03-01 14:33:05
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy


__all__ = [
    'generate_shortest_path_trees',
]


def generate_shortest_path_trees(G, flows):
    """
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, shortest_path_trees
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    # Generate all pair shortest paths
    all_pair_paths = nx.shortest_path(graph)
    # Initialize shortest_path_trees
    shortest_path_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Compute the origin_T
        origin_T = generate_shortest_path_tree(f['src'], f['dst'].keys(),
                                               all_pair_paths)
        # Add origin_T into shortest_path_trees
        shortest_path_trees.append(origin_T)

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
        # Update the residual flow entries of nodes in the allocated_T
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the allocated_T
        update_edge_bandwidth(graph, allocated_T, f['size'])

    return graph, allocated_flows, shortest_path_trees


def generate_shortest_path_tree(source, destinations, all_pair_paths):
    """Generate Shortest Path Tree(SPT)
    :param source: The source node of flow request
    :param destinations: The destinations of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :return: Shortest Path Tree
    """
    # Initialize T
    T = nx.Graph()
    T.root = source
    # Traverse all destinations
    for dst in destinations:
        # Get the shortest path from source to dst
        path = all_pair_paths[source][dst]
        # Add path into T
        T.add_path(path)

    return T
