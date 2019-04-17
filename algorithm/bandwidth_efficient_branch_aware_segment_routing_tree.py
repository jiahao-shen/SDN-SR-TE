""""
@project: RoutingAlgorithm
@author: sam
@file bandwidth_efficient_branch_aware_segment_routing_tree.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
from network import *
from networkx.utils import pairwise
from copy import deepcopy
from collections import OrderedDict
import math

__all__ = [
    'generate_bandwidth_efficient_branch_aware_segment_routing_trees',
    'compute_intersection_node'
]


def generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows,
                                                                    k=5,
                                                                    alpha=0.5,
                                                                    beta=0.5,
                                                                    w1=1,
                                                                    w2=1):
    """According to the flows and graph, generate Bandwidth-efficient
    Branch-aware Segment Routing Tree(BBSRT)
    Sheu, J.-P., & Chen, Y.-C. (2017).
    A scalable and bandwidth-efficient multicast algorithm based on segment
    routing in software-defined networking.
    In 2017 IEEE International Conference on Communications (ICC) (pp. 1–6).
    https://doi.org/10.1109/ICC.2017.7997197
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
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    # Add node weight and edge weight
    nx.set_edge_attributes(graph, 0, 'weight')
    nx.set_node_attributes(graph, 0, 'weight')

    band_efficient_branch_aware_segment_routing_trees = []  # Initialize

    # The node betweenness centrality
    nodes_betweenness_centrality = nx.betweenness_centrality(graph)

    # The edge betweenness centrality
    edges_betweenness_centrality = nx.edge_betweenness_centrality(graph)

    # Traverse the flows
    for f in allocated_flows:
        # Add weight for nodes and edges
        graph = generate_weighted_graph(graph, nodes_betweenness_centrality,
                                        edges_betweenness_centrality, alpha,
                                        beta)
        # Dict to store k shortest paths for (source, destinations)
        d = {}
        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        # Initialize origin_T
        origin_T = nx.Graph()
        origin_T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Compute the k shortest path from source to dst_node
            d[dst] = generate_k_shortest_paths(graph, f['src'], dst,
                                               k, weight='weight')
        # Sort the dict by value
        d = OrderedDict(sorted(d.items(),
                               key=lambda x:
                               compute_path_cost(graph, x[1][0],
                                                 weight='weight')))

        # Traverse the destination nodes in d_sorted
        for dst in d:
            # Path initialize
            path = d[dst][0]
            # If the multicast tree isn't empty
            if len(origin_T) != 0:
                # Initialize the minimum cost
                minimum_cost = math.inf
                # Traverse the k shortest path for dst_node
                for p in d[dst]:
                    # If exists cycle after adding p into multicast tree
                    # Then continue
                    if has_cycle(origin_T, p):
                        continue
                    # Compute the extra cost according to the paper
                    extra_cost = compute_extra_cost(graph, origin_T,
                                                    p, w1, w2)
                    # If extra cost less than minimum cost
                    if extra_cost < minimum_cost:
                        # Update minimum cost and path
                        minimum_cost = extra_cost
                        path = p
            # Add path into origin_T
            origin_T.add_path(path)
            # Check the current path whether valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record the path for pair(source, destination)
                f['dst'][dst] = path
                # Add the path into the multicast tree
                allocated_T.add_path(path)
        # Update the residual entries of nodes in graph
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the multicast tree
        update_edge_bandwidth(graph, allocated_T, f['size'])
        # Add origin_T into band_efficient_branch_aware_segment_routing_trees
        band_efficient_branch_aware_segment_routing_trees.append(origin_T)

    return graph, allocated_flows, \
        band_efficient_branch_aware_segment_routing_trees


def compute_extra_cost(G, multicast_tree, path, w1, w2):
    """Compute the extra cost for path
    :param G: The origin graph
    :param multicast_tree: The multicast tree
    :param path: The path needs to add into the graph
    :param w1: The first parameter of extra cost
    :param w2: The second parameter of extra cost
    :return: extra_cost
    """
    # Compute the branch node and flag(whether new branch node)
    intersection, flag = compute_intersection_node(multicast_tree, path)
    # The final result
    extra_cost = 0
    # If exists intersection node
    if intersection is not None:
        # Compute sub path start from intersection
        sub_path = path[path.index(intersection):]
        # Extra cost add path cost
        extra_cost += w1 * compute_path_cost(G, sub_path, weight='weight')
        # If the intersection node is new branch node
        if flag:
            # Extra cost add cost of new branch node
            extra_cost += w2 * G.nodes[intersection]['weight']

    return extra_cost


def generate_weighted_graph(G, nodes_betweenness_centrality,
                            edges_betweenness_centrality, alpha, beta):
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
        # Set the congestion to inf
        congestion_index = math.inf
        # If the residual bandwidth not equals 0, then compute the congestion
        if e[2]['residual_bandwidth'] != 0:
            congestion_index = e[2]['link_capacity'] / e[2][
                'residual_bandwidth'] - 1
        # Compute the weight according to the equation 3
        # Set the edge weight
        e[2]['weight'] = alpha * congestion_index + (
                1 - alpha) * edges_betweenness_centrality[(e[0], e[1])]
    # Traverse the nodes
    for v in G.nodes(data=True):
        # Set the congestion to inf
        congestion_index = math.inf
        # If the residual bandwidth not equals 0, then compute the congestion
        if v[1]['residual_flow_entries'] != 0:
            congestion_index = v[1]['flow_limit'] / v[1][
                'residual_flow_entries'] - 1
        # Set the node weight
        v[1]['weight'] = beta * congestion_index + (
                1 - beta) * nodes_betweenness_centrality[v[0]]

    return G


def compute_intersection_node(multicast_tree, path):
    """According to the multicast tree, to compute the intersection node
    :param multicast_tree: The allocated multicast tree
    :param path: The path need to be added
    :return: node, flag
    """
    # Intersection node initialize
    intersection = None
    # Traverse all nodes during path
    for v, u in pairwise(path):
        if v in multicast_tree.nodes and u not in multicast_tree.nodes:
            intersection = v
            break
    # If no intersection, return False
    if intersection is None:
        return None, False
    # If the intersection isn't root but new branch node, return True
    if intersection != multicast_tree.root and \
            multicast_tree.degree(intersection) == 2:
        return intersection, True
    # Else return False
    return intersection, False
