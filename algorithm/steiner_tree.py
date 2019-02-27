"""
@project: RoutingAlgorithm
@author: sam
@file steiner_tree.py
@ide: PyCharm
@time: 2019-01-31 15:44:27
@blog: https://jiahaoplus.com
"""
from network.topology import *
from network.utils import *
from figure.utils import *
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
    """According to the flows and graph, generate Steiner Tree(ST)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

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
        # Set the source node of steiner tree
        steiner_tree.source = f['src']
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


def generate_widest_steiner_trees(G, flows):
    """According to the flows and graph, generate Widest Steiner Tree(WST)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    widest_steiner_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Generate the terminal nodes for steiner tree
        # Terminal nodes = destination nodes list + source node
        terminal_nodes = list(f['dst'].keys()) + [f['src']]
        # Generate the temp widest steiner tree for terminal nodes
        # Then compute all paths from source to other nodes in temp
        # widest steiner tree
        all_paths = nx.shortest_path(
            nx.Graph(generate_widest_steiner_tree(graph, terminal_nodes)),
            f['src'],
            weight=None)
        # Steiner Tree for current multicast initialization
        widest_steiner_tree = nx.Graph()
        # Set the source node of widest steiner tree
        widest_steiner_tree.source = f['src']
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Get the path from source to destination, not considering weight
            path = all_paths[dst_node]
            # Check the current path whether valid
            if check_path_valid(graph, widest_steiner_tree, path, f['size']):
                # Record path for pair(source, destination)
                f['dst'][dst_node] = path
                # Add the path into steiner tree
                widest_steiner_tree.add_path(path)
        # Update the residual flow entries of nodes in the widest steiner tree
        update_node_entries(graph, widest_steiner_tree)
        # Update the residual bandwidth of edges in the widest steiner tree
        update_edge_bandwidth(graph, widest_steiner_tree, f['size'])
        # Add multicast tree in forest
        widest_steiner_trees.append(widest_steiner_tree)

    return graph, allocated_flows, widest_steiner_trees


def generate_widest_steiner_tree(G, terminal_nodes):
    """Generate Widest Steiner Tree
    :param G: The origin graph
    :param terminal_nodes: The list of terminal nodes for which minimum
    steiner trees is to be found
    :return: widest_steiner_tree
    """
    # Generate the widest metric closure
    M = generate_widest_metric_closure(G)
    # Generate the subgraph of M for terminal nodes
    H = M.subgraph(terminal_nodes)
    # Generate the minimum spanning edges with 'distance' as weight
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # For the minimum spanning edges, add the widest shortest path
    # according to the widest metric closure
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    # Generate the subgraph of G for edges
    widest_steiner_tree = G.edge_subgraph(edges)

    return widest_steiner_tree


def generate_widest_metric_closure(G):
    """Generate the Widest Metric Closure according to G
    The widest metric closure of a graph G is the complete graph in which each
    edge is weighted by the widest shortest path distance between the
    nodes in G
    :param G: The origin graph
    :return: widest_metric_closure
    """
    # Initialize the widest_metric_closure
    widest_metric_closure = nx.Graph()
    # Traverse all nodes in G as src_node
    for src_node in G.nodes:
        # Compute all widest shortest path from src_node to other nodes
        all_widest_shortest_path = generate_widest_shortest_path(G, src_node)
        # Destination nodes without src_node
        destinations = set(G.nodes)
        destinations.remove(src_node)
        # Traverse the destination
        for dst_node in destinations:
            # Get the widest shortest path from src_node to dst_node
            widest_shortest_path = all_widest_shortest_path[dst_node]
            # Add the edge(src_node, dst_node) into the graph, with two
            # attributes(distance, path)
            widest_metric_closure.add_edge(src_node, dst_node, distance=len(
                widest_shortest_path) - 1, path=widest_shortest_path)

    return widest_metric_closure


def test():
    """Test Steiner Tree and Widest Steiner Tree
    :return:
    """
    G, pos = generate_topology()
    flows = generate_flow_requests(G, flow_groups=3)

    draw_topology(G, pos, title='Topology')

    # ST
    graph, allocated_flows, multicast_trees = generate_steiner_trees(G, flows)

    draw_topology(graph, pos, title='Allocated Graph')
    output_flows(allocated_flows)

    for tree in multicast_trees:
        draw_topology(tree, pos, title='Tree')

    # WST
    graph, allocated_flows, multicast_trees = \
        generate_widest_steiner_trees(G, flows)

    draw_topology(graph, pos, title='Allocated Graph')
    output_flows(allocated_flows)

    for tree in multicast_trees:
        draw_topology(tree, pos, title='Tree')


if __name__ == '__main__':
    test()
