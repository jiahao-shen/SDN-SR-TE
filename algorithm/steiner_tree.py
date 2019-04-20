"""
@project: RoutingAlgorithm
@author: sam
@file steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:36:05
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy

__all__ = [
    'generate_steiner_trees',
    'shortest_path_to_tree'
]


def generate_steiner_trees(G, flows):
    """
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)   # Copy flows

    # Generate all pair shortest path
    all_pair_paths = nx.shortest_path(graph)
    # Initialize steiner_trees
    steiner_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Compute the origin_T
        origin_T = generate_steiner_tree(f['src'], f['dst'], all_pair_paths)
        # Add origin_T into steiner_trees
        steiner_trees.append(origin_T)

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

    return graph, allocated_flows, steiner_trees


def generate_steiner_tree(source, destinations, all_pair_paths):
    """Generate Steiner Tree(ST)
    :param source: The source node of flow request
    :param destinations: The destinations of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :return: Steiner Tree
    """
    # Initialize T
    T = nx.Graph()
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
            # Get the shortest path from v to constructed tree
            p = shortest_path_to_tree(v, T, all_pair_paths)
            # Update path
            if path is None or (path is not None and len(p) < len(path)):
                path = p
        # Add path into T
        T.add_path(path)
        # Remove the terminal node in current path
        terminals.remove(path[-1])

        # Remove the terminal already in T
        v_d = set()
        for v in terminals:
            if v in T.nodes:
                v_d.add(v)
        terminals = terminals - v_d

    return T


def shortest_path_to_tree(target, tree, all_pair_paths):
    """Compute the shortest path from target to constructed tree
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
