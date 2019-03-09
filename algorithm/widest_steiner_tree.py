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
    """According to the flows and graph, generate Widest Steiner Tree(WST)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    widest_steiner_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Generate the terminal nodes for steiner tree
        # Terminal nodes = destination nodes list + source node
        terminals = list(f['dst'].keys()) + [f['src']]
        # Generate the temp widest steiner tree for terminal nodes
        # Then compute all paths from source to other nodes in temp
        # widest steiner tree
        origin_T = generate_widest_steiner_tree(graph, terminals)
        all_paths = nx.shortest_path(origin_T, f['src'], weight=None)
        # Steiner Tree for current multicast initialization
        allocated_T = nx.Graph()
        # Set the root of widest steiner tree
        allocated_T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from source to destination, not considering weight
            path = all_paths[dst]
            # Check the current path whether valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record path for pair(source, destination)
                f['dst'][dst] = path
                # Add the path into steiner tree
                allocated_T.add_path(path)
        # Update the residual flow entries of nodes in the widest steiner tree
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the widest steiner tree
        update_edge_bandwidth(graph, allocated_T, f['size'])
        # Add multicast tree in forest
        widest_steiner_trees.append(origin_T)

    return graph, allocated_flows, widest_steiner_trees


def generate_widest_steiner_tree(G, terminal_nodes):
    """Generate Widest Steiner Tree
    :param G: The origin graph
    :param terminal_nodes: The list of terminal nodes for which minimum
    steiner trees is to be found
    :return: Widest Steiner Tree
    """
    # Generate the widest metric closure
    M = generate_widest_metric_closure(G)
    # Generate the subgraph of M for terminal nodes
    H = M.subgraph(terminal_nodes)
    # Generate the minimum spanning edges with 'distance' as weight
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # For the minimum spanning edges, add the widest shortest path
    # according to the widest metric closure
    edges = chain.from_iterable(pairwise(d['path']) for v, u, d in mst_edges)
    # Generate the subgraph of G for edges
    T = G.edge_subgraph(edges)

    return T


def generate_widest_metric_closure(G):
    """Generate the Widest Metric Closure according to G
    The widest metric closure of a graph G is the complete graph in which each
    edge is weighted by the widest shortest path distance between the
    nodes in G
    :param G: The origin graph
    :return: Widest Metric Closure
    """
    # Initialize the widest_metric_closure
    M = nx.Graph()
    # Traverse all nodes in G as src_node
    for src in G.nodes:
        # Compute all widest shortest path from src_node to other nodes
        all_paths = generate_widest_shortest_path(G, src)
        # Destination nodes without src_node
        destinations = set(G.nodes)
        destinations.remove(src)
        # Traverse the destination
        for dst in destinations:
            # Get the widest shortest path from src_node to dst_node
            widest_shortest_path = all_paths[dst]
            # Add the edge(src_node, dst_node) into the graph, with two
            # attributes(distance, path)
            M.add_edge(src, dst, distance=len(widest_shortest_path) - 1,
                       path=widest_shortest_path)

    return M

