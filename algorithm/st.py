"""
@project: RoutingAlgorithm
@author: sam
@file st.py
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
        terminal_nodes = list(f['dst'].keys()) + [f['src']]
        # Generate temp steiner tree for terminal nodes
        # Compute all paths from source to other nodes in temp steiner tree
        all_paths = nx.shortest_path(nx.Graph(nxaa.steiner_tree(graph,
                                                                terminal_nodes,
                                                                weight=None)),
                                     f['src'], weight=None)
        # Steiner Tree for current multicast initialization
        steiner_tree = nx.Graph()
        # Set the root of steiner tree
        steiner_tree.root = f['src']
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Get the path from source to destination, not considering weight
            path = all_paths[dst_node]
            # Check the current path whether valid
            if check_path_valid(graph, steiner_tree, path, f['size']):
                # Record path for pair(source, destination)
                f['dst'][dst_node] = path
                # Add the path into steiner tree
                steiner_tree.add_path(path)
        # Update the residual flow entries of nodes in the steiner tree
        update_node_entries(graph, steiner_tree)
        # Update the residual bandwidth of edges in the steiner tree
        update_edge_bandwidth(graph, steiner_tree, f['size'])
        # Add multicast tree in forest
        steiner_trees.append(steiner_tree)

    return graph, allocated_flows, steiner_trees
