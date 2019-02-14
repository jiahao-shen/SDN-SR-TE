"""
@project: RoutingAlgorithm
@author: sam
@file steiner_tree.py
@ide: PyCharm
@time: 2019-01-31 15:44:27
@blog: https://jiahaoplus.com
"""
from network.topology import *
from itertools import chain
from networkx.utils import pairwise
from algorithm.shortest_path_tree import generate_widest_shortest_path
import networkx.algorithms.approximation as nxaa

__all__ = [
    'generate_steiner_trees',
    'generate_widest_steiner_trees',
    'generate_widest_steiner_tree',
    'generate_widest_metric_closure'
]


def generate_steiner_trees(G, flows):
    """According to the flows and graph, generate Steiner Tree(ST) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    steiner_trees = nx.Graph()  # Steiner Trees initialization
    steiner_trees.add_nodes_from(G)  # Add nodes from G to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Generate the steiner tree(src_node, dst_nodes), not considering weight
        steiner_tree = nx.Graph(nxaa.steiner_tree(graph, list(flows[src_node].keys()) + [src_node], weight=None))

        # Traverse the destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Find the path for current flow in steiner tree
            path = nx.shortest_path(steiner_tree, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = path
                # Add the path into the allocated_graph
                nx.add_path(steiner_trees, path)

    return graph, allocated_flows, steiner_trees


def generate_widest_steiner_trees(G, flows):
    """According to the flows and graph, generate Widest Steiner Tree(WST) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    widest_steiner_trees = nx.Graph()  # Steiner Trees initialization
    widest_steiner_trees.add_nodes_from(G)  # Add nodes from G to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Generate the steiner tree(src_node, dst_nodes), not considering weight
        steiner_tree = generate_widest_steiner_tree(graph, list(flows[src_node].keys()) + [src_node])
        # Traverse the destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Find the path for current flow in steiner tree
            path = nx.shortest_path(steiner_tree, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = path
                # Add the path into the allocated_graph
                nx.add_path(widest_steiner_trees, path)

    return graph, allocated_flows, widest_steiner_trees


def generate_widest_steiner_tree(G, terminal_nodes):
    """Generate Widest Steiner Tree
    :param G: The origin graph
    :param terminal_nodes: The list of terminal nodes for which minimum steiner trees is to be found
    :return: widest_steiner_tree
    """
    # Generate the widest metric closure
    M = generate_widest_metric_closure(G)
    # Generate the subgraph of M for terminal nodes
    H = M.subgraph(terminal_nodes)
    # Generate the minimum spanning edges with 'distance' as weight
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # For the minimum spanning edges, add the widest shortest path according to the widest metric closure
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    # Generate the subgraph of G for edges
    widest_steiner_tree = G.edge_subgraph(edges)

    return nx.Graph(widest_steiner_tree)  # Transform to the nx.Graph


def generate_widest_metric_closure(G):
    """Generate the Widest Metric Closure according to G
    The widest metric closure of a graph G is the complete graph in which each edge
    is weighted by the widest shortest path distance between the nodes in G
    :param G: The origin graph
    :return: widest_metric_closure
    """
    # Initialize the widest_metric_closure
    widest_metric_closure = nx.Graph()
    # Traverse all nodes in G as src_node
    for src_node in range(len(G)):
        # Compute all widest shortest path from src_node to other nodes
        all_widest_shortest_path = generate_widest_shortest_path(G, src_node)
        # Destination nodes without src_node
        destinations = set(range(len(G)))
        destinations.remove(src_node)
        # Traverse the destination
        for dst_node in destinations:
            # Get the widest shortest path from src_node to dst_node
            widest_shortest_path = all_widest_shortest_path[dst_node]
            # Add the edge(src_node, dst_node) into the graph, with two attributes(distance, path)
            widest_metric_closure.add_edge(src_node, dst_node, distance=len(widest_shortest_path) - 1,
                                           path=widest_shortest_path)

    return widest_metric_closure


def test():
    # g, pos = generate_topology(100)
    # draw_topology(g, pos, 'Network Topology')
    # flows = generate_flow_requests(g, 50, 10)
    # allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
    # draw_topology(allocated_graph, pos, 'Steiner Tree')
    pass


if __name__ == '__main__':
    test()
