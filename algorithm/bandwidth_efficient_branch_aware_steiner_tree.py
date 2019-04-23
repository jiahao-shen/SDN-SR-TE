"""
@project: SDN-SR-TE
@author: sam
@file bandwidth_efficient_branch_aware_steiner_tree.py
@ide: PyCharm
@time: 2019-04-20 13:54:55
@blog: https://jiahaoplus.com
"""
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

__all__ = [
    'generate_bandwidth_efficient_branch_aware_steiner_trees',
]


def generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows,
                                                            alpha=0.5,
                                                            beta=0.5,
                                                            w1=1,
                                                            w2=1):
    """According to the flows and graph, generate Bandwidth-efficient
    Branch-aware Segment Routing Tree(BBSRT)
    :param G: The origin graph
    :param flows: The current flow request
    :param alpha: The weight parameter for edges, default 0.5
    :param beta: The weight parameter for nodes, default 0.5
    :param w1: The weight parameter for extra path, default 1
    :param w2: The weight parameter for branch node, default 1
    :return: graph, allocated_flows,
    band_efficient_branch_aware_segment_routing_trees
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    # Add node weight and edge weight
    nx.set_edge_attributes(graph, 0, 'weight')
    nx.set_node_attributes(graph, 0, 'weight')

    # The node betweenness centrality
    nodes_betweenness_centrality = nx.betweenness_centrality(graph)
    # The edge betweenness centrality
    edges_betweenness_centrality = nx.edge_betweenness_centrality(graph)
    # Initialize band_efficient_branch_aware_steiner_trees
    band_efficient_branch_aware_steiner_trees = []

    # Traverse all flows
    for f in allocated_flows:
        # Compute the origin_T
        origin_T = generate_bandwidth_efficient_branch_aware_steiner_tree(
            graph, f['src'], f['dst'],
            nodes_betweenness_centrality,
            edges_betweenness_centrality,
            alpha, beta, w1, w2)
        # Add origin_T into band_efficient_branch_aware_segment_routing_trees
        band_efficient_branch_aware_steiner_trees.append(origin_T)

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
                allocated_T.add_path(path)
        # Update the residual entries of nodes in the allocated_T
        update_node_entries(graph, allocated_T)
        # Update the residual bandwidth of edges in the allocated_T
        update_edge_bandwidth(graph, allocated_T, f['size'])

    return graph, allocated_flows, \
           band_efficient_branch_aware_steiner_trees


def generate_bandwidth_efficient_branch_aware_steiner_tree(G, source,
                                                           destinations,
                                                           nodes_betweenness_centrality,
                                                           edges_betweenness_centrality,
                                                           alpha, beta,
                                                           w1, w2):
    """
    :param G: The origin graph
    :param source: The source of flow request
    :param destinations: The destinations of request
    :param nodes_betweenness_centrality:
    :param edges_betweenness_centrality:
    :param alpha: The weight parameter for edges
    :param beta: The weight parameter for nodes
    :param w1: The weight parameter for extra path
    :param w2: The weight parameter for branch node
    :return: Branch-efficient Branch-aware Segment Routing Tree
    """
    # Add weight for nodes and edges
    G = generate_weighted_graph(G,
                                nodes_betweenness_centrality,
                                edges_betweenness_centrality,
                                alpha, beta)
    # Initialize T
    T = nx.Graph()
    T.add_node(source)
    T.root = source
    # Initialize terminals
    terminals = set(destinations)
    # Compute all pair weighted shortest paths
    all_pair_paths = all_pair_weighted_shortest_paths(G)

    # While terminals isn't empty
    while terminals:
        # Initialize path
        path = None
        # Traverse all terminals
        for v in terminals:
            # Get the weighted shortest path from v to constructed tree
            p = weighted_shortest_path_to_tree(G, v, T, all_pair_paths)
            # Update path
            if path is None or \
                    (path is not None and compute_extra_cost(G, T, p, w1, w2) <
                     compute_extra_cost(G, T, path, w1, w2)):
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


def compute_extra_cost(G, tree, path, w1, w2):
    """Compute the extra cost for path
    :param G: The origin graph
    :param tree: The multicast tree
    :param path: The path needs to add into the graph
    :param w1: The weight parameter for extra path
    :param w2: The weight parameter for branch node
    :return: extra_cost
    """
    # Compute the path cost
    extra_cost = w1 * compute_path_cost(G, path, weight='weight')
    # Get the intersection node
    intersection = path[0]
    # If the intersection node of path is new branch node
    if intersection != tree.root and tree.degree(intersection) == 2:
        # Add the branch node cost
        extra_cost += w2 * G.nodes[intersection]['weight']

    return extra_cost


def generate_weighted_graph(G, nodes_betweenness_centrality,
                            edges_betweenness_centrality, alpha, beta):
    """Generate the weighted graph according to the paper
    :param G: The origin graph
    :param nodes_betweenness_centrality:
    :param edges_betweenness_centrality:
    :param alpha: The weight parameter for edges
    :param beta: The weight parameter for nodes
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


def weighted_shortest_path_to_tree(G, target, tree, all_pair_paths):
    """Compute the weighted shortest path from target to constructed tree
    :param G: The origin graph
    :param target: The target node needs to be added into the tree
    :param tree: The constructed tree
    :param all_pair_paths: All pair minimum weighted paths in graph
    :return: path
    """
    # Initialize path
    path = None
    # Traverse all nodes in tree
    for v in tree.nodes:
        # Get the weighted shortest path from v to target
        p = all_pair_paths[v][target]
        # Update path
        if path is None or (path is not None and
                            compute_path_cost(G, p, 'weight') <
                            compute_path_cost(G, path, 'weight')):
            path = p

    return path


def all_pair_weighted_shortest_paths(G):
    """Compute all pair weighted shortest paths
    :param G: The origin graph
    :return: all_pair_paths
    """
    all_pair_paths = {}

    for v in G.nodes:
        all_pair_paths[v] = nx.shortest_path(G, v, weight='weight')

    return all_pair_paths
