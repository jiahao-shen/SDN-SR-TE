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
import networkx.algorithms.approximation as nxaa

__all__ = [
    'generate_steiner_trees',
]


def generate_steiner_trees(G, flows):
    """According to the flows and graph, generate Steiner Tree(ST)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    steiner_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Generate the terminal nodes for steiner tree
        # Terminal nodes = destination nodes list + source node
        terminals = list(f['dst'].keys()) + [f['src']]
        # Generate temp steiner tree for terminal nodes
        # Compute all paths from source to other nodes in temp steiner tree
        all_paths = nx.shortest_path(nx.Graph(nxaa.steiner_tree(graph,
                                                                terminals,
                                                                weight=None)),
                                     f['src'], weight=None)
        # Steiner Tree for current multicast initialization
        T = nx.Graph()
        # Set the root of steiner tree
        T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from source to destination, not considering weight
            path = all_paths[dst]
            # Check the current path whether valid
            if is_path_valid(graph, T, path, f['size']):
                # Record path for pair(source, destination)
                f['dst'][dst] = path
                # Add the path into steiner tree
                T.add_path(path)
        # Update the residual flow entries of nodes in the steiner tree
        update_node_entries(graph, T)
        # Update the residual bandwidth of edges in the steiner tree
        update_edge_bandwidth(graph, T, f['size'])
        # Add multicast tree in forest
        steiner_trees.append(T)

    return graph, allocated_flows, steiner_trees
