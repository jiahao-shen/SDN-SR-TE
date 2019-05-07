""""
@project: RoutingAlgorithm
@author: sam
@file bandwidth_efficient_branch_aware_segment_routing_tree.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy
from collections import OrderedDict
import math

__all__ = [
    'generate_bandwidth_efficient_branch_aware_segment_routing_trees',
]


def generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows,
                                                                    k=5,
                                                                    alpha=0.5,
                                                                    beta=0.5,
                                                                    w1=1,
                                                                    w2=1):
    """According to the flows and graph, generate Bandwidth-efficient
    Branch-aware Segment Routing Tree(BBSRT)
    :param G: The origin graph
    :param flows: The current flow request
    :param k: The k-shortest paths in algorithm, default 5
    :param alpha: The parameter in equation 3 in paper, default 0.5
    :param beta: The parameter in equation 4 in paper, default 0.5
    :param w1: The parameter in equation for extra cost, default 1
    :param w2: The parameter in equation for extra cost, default 1
    :return: graph, allocated_flows,
    band_efficient_branch_aware_segment_routing_trees
    """
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    # Add node weight and edge weight
    nx.set_edge_attributes(graph, 0, 'weight')
    nx.set_node_attributes(graph, 0, 'weight')

    # The node betweenness centrality
    nodes_betweenness_centrality = nx.betweenness_centrality(graph)
    # The edge betweenness centrality
    edges_betweenness_centrality = nx.edge_betweenness_centrality(graph)
    # Initialize bandwidth_efficient_branch_node_aware_segment_routing_trees
    bandwidth_efficient_branch_aware_segment_routing_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Compute the origin_T
        origin_T = generate_bandwidth_efficient_branch_aware_segment_routing_tree(graph, f['src'], f['dst'],
                                                                                  nodes_betweenness_centrality,
                                                                                  edges_betweenness_centrality,
                                                                                  k, alpha, beta, w1, w2)
        # Add origin_T into band_efficient_branch_aware_segment_routing_trees
        bandwidth_efficient_branch_aware_segment_routing_trees.append(origin_T)

        # Compute all paths in origin_T
        all_paths = nx.shortest_path(origin_T, f['src'])
        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from src to dst
            path = all_paths[dst]
            # Check whether path valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record the path
                f['dst'][dst] = path
                # Add path into allocated_T
                nx.add_path(allocated_T, path)
        # Update the information of graph
        update_topo_info(graph, allocated_T, f['size'])

    return graph, allocated_flows, \
        bandwidth_efficient_branch_aware_segment_routing_trees


def generate_bandwidth_efficient_branch_aware_segment_routing_tree(G, source, destinations,
                                                                   nodes_betweenness_centrality,
                                                                   edges_betweenness_centrality,
                                                                   k, alpha, beta,
                                                                   w1, w2):
    """Generate Bandwidth-efficient Branch-aware Segment Routing Tree(BBSRT)
    Sheu, J.-P., & Chen, Y.-C. (2017).
    A scalable and bandwidth-efficient multicast algorithm based on segment
    routing in software-defined networking.
    In 2017 IEEE International Conference on Communications (ICC) (pp. 1–6).
    https://doi.org/10.1109/ICC.2017.7997197
    :param G: The origin graph
    :param source: The source of flow request
    :param destinations: The destinations of request
    :param nodes_betweenness_centrality:
    :param edges_betweenness_centrality:
    :param k: The k-shortest paths in algorithm
    :param alpha: The parameter in equation 3 in paper
    :param beta: The parameter in equation 4 in paper
    :param w1: The parameter in extra cost equation
    :param w2: The parameter in extra cost equation
    :return: Branch-efficient Branch-aware Segment Routing Tree
    """
    # Add weight for nodes and edges
    G = generate_weighted_graph(G,
                                nodes_betweenness_centrality,
                                edges_betweenness_centrality,
                                alpha, beta)
    # Initialize T
    T = nx.Graph()
    T.root = source
    # Dict to store k shortest paths for (source, destinations)
    d_sorted = {}
    # Traverse all destination nodes
    for dst in destinations:
        # Compute the k shortest path from source to dst
        d_sorted[dst] = generate_k_shortest_paths(G, source, dst, k,
                                                  weight='weight')
    # Sort the dict by value
    d_sorted = OrderedDict(sorted(d_sorted.items(), key=lambda x:
                                  compute_path_cost(G, x[1][0], weight='weight')))

    # Traverse the destination nodes in d_sorted
    for dst in d_sorted:
        # If dst already in T, then continue
        if dst in T.nodes:
            continue
        # Initialize path
        path = d_sorted[dst][0]
        # If T isn't empty
        if len(T) != 0:
            # Initialize the minimum cost
            minimum_cost = math.inf
            # Traverse the k shortest path for dst_node
            for p in d_sorted[dst]:
                # Get the sub_path
                sub_path = compute_acyclic_sub_path(T, p)
                # Compute the extra cost according to the paper
                extra_cost = compute_extra_cost(G, T, sub_path, w1, w2)
                # If extra cost less than minimum cost
                if extra_cost < minimum_cost:
                    # Update minimum cost and path
                    minimum_cost = extra_cost
                    path = sub_path
        # Add path into T
        nx.add_path(T, path)

    return T


def compute_extra_cost(G, tree, path, w1, w2):
    """Compute the extra cost for path
    :param G: The origin graph
    :param tree: The multicast tree
    :param path: The current path
    :param w1: The first parameter of extra cost
    :param w2: The second parameter of extra cost
    :return: extra_cost
    """
    # Compute the path cost
    extra_cost = w1 * compute_path_cost(G, path, weight='weight')
    # Get the intersection
    intersection = path[0]
    # If intersection is new branch node
    if intersection != tree.root and tree.degree(intersection) == 2:
        # Extra cost add cost of new branch node
        extra_cost += w2 * G.nodes[intersection]['weight']

    return extra_cost


def generate_weighted_graph(G,
                            nodes_betweenness_centrality,
                            edges_betweenness_centrality,
                            alpha, beta):
    """Generate the weighted graph according to the paper
    :param G: The origin graph
    :param nodes_betweenness_centrality:
    :param edges_betweenness_centrality:
    :param alpha: The parameter of edges for weight
    :param beta: The parameter of nodes for weight
    :return: weighted G
    """
    # Traverse the edges
    for e in G.edges(data=True):
        # Compute the congestion for links
        congestion_index = e[2]['link_capacity'] / e[2][
            'residual_bandwidth'] - 1
        # Compute the weight according to the equation 3
        e[2]['weight'] = alpha * congestion_index + (
            1 - alpha) * edges_betweenness_centrality[(e[0], e[1])]
    # Traverse the nodes
    for v in G.nodes(data=True):
        # Compute the congestion for nodes
        congestion_index = v[1]['flow_limit'] / v[1][
            'residual_flow_entries'] - 1
        # Compute the weight according to the equation 4
        v[1]['weight'] = beta * congestion_index + (
            1 - beta) * nodes_betweenness_centrality[v[0]]

    return G
