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

"""
Old Steiner Tree
"""
# def generate_steiner_trees(G, flows):
#     """According to the flows and graph, generate Steiner Tree(ST)
#     :param G: The origin graph
#     :param flows: The flow request
#     :return: graph, allocated_flows, allocated_graph
#     """
#     graph = deepcopy(G)  # Copy G
#     allocated_flows = deepcopy(flows)  # Copy flows
#
#     steiner_trees = []  # Initialize
#
#     # Traverse the flows
#     for f in allocated_flows:
#         # Generate the terminal nodes for steiner tree
#         # Terminal nodes = destination nodes list + source node
#         terminals = list(f['dst'].keys()) + [f['src']]
#         # Generate temp steiner tree for terminal nodes
#         # Compute all paths from source to other nodes in temp steiner tree
#         origin_T = nx.Graph(nxaa.steiner_tree(graph, terminals, weight=None))
#         all_paths = nx.shortest_path(origin_T, f['src'], weight=None)
#         # Steiner Tree for current multicast initialization
#         allocated_T = nx.Graph()
#         # Set the root of steiner tree
#         allocated_T.root = f['src']
#         # Traverse all destination nodes
#         for dst in f['dst']:
#             # Get the path from source to destination, not considering weight
#             path = all_paths[dst]
#             # Check the current path whether valid
#             if is_path_valid(graph, allocated_T, path, f['size']):
#                 # Record path for pair(source, destination)
#                 f['dst'][dst] = path
#                 # Add the path into steiner tree
#                 allocated_T.add_path(path)
#         # Update the residual flow entries of nodes in the steiner tree
#         update_node_entries(graph, allocated_T)
#         # Update the residual bandwidth of edges in the steiner tree
#         update_edge_bandwidth(graph, allocated_T, f['size'])
#         # Add multicast tree in forest
#         steiner_trees.append(origin_T)
#
#     return graph, allocated_flows, steiner_trees


# New Steiner Tree
def generate_steiner_trees(G, flows):
    """According to the flows and graph, generate Steiner Tree(ST)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)   # Copy flows

    # Generate all pair shortest path
    all_pair_paths = nx.shortest_path(graph)
    # Steiner Trees initialize
    steiner_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Initialize origin_T
        origin_T = nx.Graph()
        origin_T.add_node(f['src'])
        # Initialize terminals
        terminals = set(f['dst'].keys())
        # While terminals not empty
        while terminals:
            # Initialize path
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the shortest path from v to constructed tree
                p = shortest_path_to_tree(v, origin_T, all_pair_paths)
                # Current path length is smaller
                if path is None or (path is not None and len(p) < len(path)):
                    # Update path
                    path = p
            # Add path into origin_T
            origin_T.add_path(path)
            # Remove the terminal node in current path
            terminals.remove(path[-1])

        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        allocated_T.add_node(f['src'])
        # Compute all paths from source to other nodes in origin_T
        all_paths = nx.shortest_path(origin_T, f['src'])
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from src to dst
            path = all_paths[dst]
            # Check whether the path valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record the path
                f['dst'][dst] = path
                # Add the path into steiner tree
                allocated_T.add_path(path)

        # Update the residual flow entries of nodes in the steiner tree
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the steiner tree
        update_edge_bandwidth(graph, allocated_T, f['size'])
        # Add origin_T into steiner_trees
        steiner_trees.append(origin_T)

    return graph, allocated_flows, steiner_trees


def shortest_path_to_tree(target, tree, all_pair_paths):
    """Compute the shortest path from target to constructed tree
    :param target: The target node needs to be added into the tree
    :param tree: The constructed tree
    :param all_pair_paths: All pair shortest path in graph
    :return: path
    """
    # Initialize path
    path = None
    # Traverse all nodes in tree
    for v in tree.nodes():
        # Get the shortest path from v to target
        p = all_pair_paths[v][target]
        # Update the path
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path
