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


# Old Widest Steiner Tree
# def generate_widest_steiner_trees(G, flows):
#     """According to the flows and graph, generate Widest Steiner Tree(WST)
#     :param G: The origin graph
#     :param flows: The flow request
#     :return: graph, allocated_flows, allocated_graph
#     """
#     graph = deepcopy(G)  # Copy G
#     allocated_flows = deepcopy(flows)  # Copy flows
#
#     widest_steiner_trees = []  # Initialize
#
#     # Traverse the flows
#     for f in allocated_flows:
#         # Generate the terminal nodes for steiner tree
#         # Terminal nodes = destination nodes list + source node
#         terminals = list(f['dst'].keys()) + [f['src']]
#         # Generate the temp widest steiner tree for terminal nodes
#         # Then compute all paths from source to other nodes in temp
#         # widest steiner tree
#         origin_T = generate_widest_steiner_tree(graph, terminals)
#         all_paths = nx.shortest_path(origin_T, f['src'], weight=None)
#         # Steiner Tree for current multicast initialization
#         allocated_T = nx.Graph()
#         # Set the root of widest steiner tree
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
#         # Update the residual flow entries of nodes in the widest steiner tree
#         update_node_entries(graph, allocated_T)
#         # Update the residual bandwidth of edges in the widest steiner tree
#         update_edge_bandwidth(graph, allocated_T, f['size'])
#         # Add multicast tree in forest
#         widest_steiner_trees.append(origin_T)
#
#     return graph, allocated_flows, widest_steiner_trees
#
#
# def generate_widest_steiner_tree(G, terminal_nodes):
#     """Generate Widest Steiner Tree
#     :param G: The origin graph
#     :param terminal_nodes: The list of terminal nodes for which minimum
#     steiner trees is to be found
#     :return: Widest Steiner Tree
#     """
#     # Generate the widest metric closure
#     M = generate_widest_metric_closure(G)
#     # Generate the subgraph of M for terminal nodes
#     H = M.subgraph(terminal_nodes)
#     # Generate the minimum spanning edges with 'distance' as weight
#     mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
#     # For the minimum spanning edges, add the widest shortest path
#     # according to the widest metric closure
#     edges = chain.from_iterable(pairwise(d['path']) for v, u, d in mst_edges)
#     # Generate the subgraph of G for edges
#     T = G.edge_subgraph(edges)
#
#     return T
#
#
# def generate_widest_metric_closure(G):
#     """Generate the Widest Metric Closure according to G
#     The widest metric closure of a graph G is the complete graph in which each
#     edge is weighted by the widest shortest path distance between the
#     nodes in G
#     :param G: The origin graph
#     :return: Widest Metric Closure
#     """
#     # Initialize the widest_metric_closure
#     M = nx.Graph()
#     # Traverse all nodes in G as src_node
#     for src in G.nodes:
#         # Compute all widest shortest path from src_node to other nodes
#         all_paths = generate_widest_shortest_path(G, src)
#         # Destination nodes without src_node
#         destinations = set(G.nodes)
#         destinations.remove(src)
#         # Traverse the destination
#         for dst in destinations:
#             # Get the widest shortest path from src_node to dst_node
#             widest_shortest_path = all_paths[dst]
#             # Add the edge(src_node, dst_node) into the graph, with two
#             # attributes(distance, path)
#             M.add_edge(src, dst, distance=len(widest_shortest_path) - 1,
#                        path=widest_shortest_path)
#
#     return M

# New Widest Steiner Tree
def generate_widest_steiner_trees(G, flows):
    """According to the flows and graph, generate Widest Steiner Tree(WSPT)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)   # Copy flows

    # Widest Steiner Trees initialize
    widest_steiner_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        allocated_T.add_node(f['src'])
        # Initialize origin_T
        origin_T = nx.Graph()
        origin_T.add_node(f['src'])
        # Initialize terminals
        terminals = set(f['dst'].keys())
        # Compute all pair widest shortest paths
        all_pair_paths = all_pair_widest_shortest_paths(graph)
        # While terminals not empty
        while terminals:
            # Initialize path, min_dis and max_bandwidth
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the widest shortest path from v to constructed tree
                p = widest_shortest_path_to_tree(v, origin_T, all_pair_paths)
                # If current path length is smaller
                if path is None or (path is not None and len(p) < len(path)):
                    # Update path
                    path = p
            # Add path into origin_T
            origin_T.add_path(path)
            # Remove the terminal node in current path
            terminals.remove(path[-1])

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
                # Add the path into widest steiner tree
                allocated_T.add_path(path)
        # Update the residual flow entries of nodes in the steiner tree
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the steiner tree
        update_edge_bandwidth(graph, allocated_T, f['size'])
        # Add origin_T into widest_steiner_trees
        widest_steiner_trees.append(origin_T)

    return graph, allocated_flows, widest_steiner_trees


def widest_shortest_path_to_tree(target, tree, all_pair_paths):
    """Compute the widest shortest path from target to constructed tree
    :param target: The target node needs to be added into the tree
    :param tree: The constructed tree
    :param all_pair_paths: All pair widest shortest path in graph
    :return: path
    """
    path = None

    for v in tree.nodes():
        p = all_pair_paths[v][target]
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path


def all_pair_widest_shortest_paths(G):
    """According to the graph, compute all pair widest shortest paths
    :param G: The origin graph
    :return: all_pair_paths
    """
    all_pair_paths = {}

    for v in G.nodes():
        all_pair_paths[v] = generate_widest_shortest_path(G, v)

    return all_pair_paths

