""""
@project: RoutingAlgorithm
@author: sam
@file segment_routing.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.shortest_path_tree import *
from copy import deepcopy
from itertools import islice
from collections import OrderedDict

__all__ = [
    'generate_bandwidth_efficient_branch_aware_segment_routing_trees'
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
    :param flows: The flow request
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
    nodes_betweenness_centrality = nx.betweenness_centrality(graph,
                                                             weight=None)
    # The edge betweenness centrality
    edges_betweenness_centrality = nx.edge_betweenness_centrality(graph,
                                                                  weight=None)

    # Traverse the flows
    for f in allocated_flows:
        # Add weight for nodes and edges
        graph = generate_weighted_graph(graph, nodes_betweenness_centrality,
                                        edges_betweenness_centrality, alpha,
                                        beta)
        # Dict to store k shortest paths for (source, destinations)
        d = {}
        # Sorted Dict to store cost of the shortest path
        d_sorted = {}
        # The multicast tree for current source node
        multicast_tree = nx.Graph()
        # Set the source node of multicast tree
        multicast_tree.source = f['src']
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Compute the k shortest path from source to dst_node
            d[dst_node] = generate_k_shortest_paths(graph, f['src'], dst_node,
                                                    k, weight='weight')
            # Store the shortest path cost in d_sorted
            d_sorted[dst_node] = compute_path_cost(graph, d[dst_node][0],
                                                   weight='weight')
        # Sort the dict by value
        d_sorted = OrderedDict(sorted(d_sorted.items(), key=lambda x: x[1]))
        # Traverse the destination nodes in d_sorted
        for dst_node in d_sorted:
            # Path initialize
            path = d[dst_node][0]
            # If the multicast tree isn't empty
            if len(multicast_tree) != 0:
                # Initialize the minimum cost
                minimum_cost = math.inf
                # Traverse the k shortest path for dst_node
                for p in d[dst_node]:
                    # If exists cycle after adding p into multicast tree
                    # Then continue
                    if has_cycle(multicast_tree, p):
                        continue
                    # Compute the extra cost according to the paper
                    extra_cost = compute_extra_cost(graph, multicast_tree, p,
                                                    w1, w2)
                    # If extra cost less than minimum cost
                    if extra_cost < minimum_cost:
                        # Update minimum cost and path
                        minimum_cost = extra_cost
                        path = p
            # Check the current path whether valid
            if check_path_valid(graph, multicast_tree, path, f['size']):
                # Record the path for pair(source, destination)
                f['dst'][dst_node] = path
                # Add the path into the multicast tree
                multicast_tree.add_path(path)
        # Update the residual entries of nodes in graph
        update_node_entries(graph, multicast_tree)
        # Update the residual bandwidth of edges in the multicast tree
        update_edge_bandwidth(graph, multicast_tree, f['size'])
        # Add multicast tree in forest
        band_efficient_branch_aware_segment_routing_trees.append(
            multicast_tree)

    return graph, allocated_flows, \
        band_efficient_branch_aware_segment_routing_trees


def has_cycle(multicast_tree, path):
    """Check whether exists cycle if path is added into the multicast tree
    :param multicast_tree: The multicast tree for current multicast
    :param path: The current path
    :return:
    """
    # Copy multicast tree as temp graph
    tmp_graph = deepcopy(multicast_tree)
    # Add path into the temp graph
    tmp_graph.add_path(path)
    # If temp graph exists cycle
    if len(nx.cycle_basis(tmp_graph)) != 0:
        return True
    # Else return False
    return False


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
    intersection_node, flag = compute_intersection_node(multicast_tree, path)
    # The final result
    extra_cost = 0
    # If exists intersection node
    if intersection_node is not None:
        # Compute sub path start from intersection
        sub_path = path[path.index(intersection_node):]
        # Extra cost add path cost
        extra_cost += w1 * compute_path_cost(G, sub_path, weight='weight')
        # If the intersection node is new branch node
        if flag:
            # Extra cost add cost of new branch node
            extra_cost += w2 * G.nodes[intersection_node]['weight']

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
    for edge in G.edges(data=True):
        # Set the congestion to inf
        congestion_index = math.inf
        # If the residual bandwidth not equals 0, then compute the congestion
        if edge[2]['residual_bandwidth'] != 0:
            congestion_index = edge[2]['link_capacity'] / edge[2][
                'residual_bandwidth'] - 1
        # Get the current edge betweenness centrality
        betweenness_centrality = edges_betweenness_centrality[
            (edge[0], edge[1])]
        # Compute the weight according to the equation 3
        # Set the edge weight
        edge[2]['weight'] = alpha * congestion_index + (
                1 - alpha) * betweenness_centrality
    # Traverse the nodes
    for node in G.nodes(data=True):
        # Set the congestion to inf
        congestion_index = math.inf
        # If the residual bandwidth not equals 0, then compute the congestion
        if node[1]['residual_flow_entries'] != 0:
            congestion_index = node[1]['flow_limit'] / node[1][
                'residual_flow_entries'] - 1
        # Get the current node betweenness centrality
        betweenness_centrality = nodes_betweenness_centrality[node[0]]
        # Set the node weight
        node[1]['weight'] = beta * congestion_index + (
                1 - beta) * betweenness_centrality

    return G


def generate_k_shortest_paths(G, source, destination, k=2, weight=None):
    """Generate the k shortest paths from source to destination in G
    :param G: The origin graph
    :param source: The source node
    :param destination: The destination node
    :param k: The parameter in k shortest path, default 2
    :param weight: The weight value in shortest path algorithm, default None
    :return: The list of k shortest paths
    """
    return list(
        islice(nx.shortest_simple_paths(G, source, destination, weight), k))


def compute_intersection_node(multicast_tree, path):
    """According to the multicast tree, to compute the intersection node
    :param multicast_tree: The allocated multicast tree
    :param path: The path need to be added
    :return: node, flag
    """
    # Intersection node initialize
    intersection_node = None
    # Traverse all nodes during path
    for i in range(len(path)):
        # Find the first node not in the multicast tree
        if path[i] not in multicast_tree.nodes:
            # Set the previous node as intersection and then break
            intersection_node = path[i - 1]
            break
    # If no intersection, return False
    if intersection_node is None:
        return None, False
    # If the intersection is new branch node, return True
    if (intersection_node == multicast_tree.source and
            multicast_tree.degree(intersection_node) == 1) or (
            intersection_node != multicast_tree.source and
            multicast_tree.degree(intersection_node) == 2):
        return intersection_node, True
    # Else return False
    return intersection_node, False


def compute_path_cost(G, path, weight=None):
    """Compute the cost of path according to the parameter weight
    :param G: The origin graph
    :param path: The path need to compute
    :param weight: The edge value
    :return: cost
    """
    cost = 0
    # Traverse nodes during the path
    for i in range(len(path) - 1):
        # If weight==None, cost plus 1
        if weight is None:
            cost += 1
        # Else cost plus the edge weight
        else:
            cost += G[path[i]][path[i + 1]][weight]

    return cost


def test_1():
    G, pos = generate_topology()
    flows = generate_flow_requests(G, flow_entries=10)

    output_flows(flows)

    draw_topology(G, pos, title='Topology')

    graph, allocated_flows, multicast_trees = \
        generate_shortest_path_trees(G, flows)

    for index, tree in enumerate(multicast_trees):
        draw_topology(tree, pos, title='SPT' + str(index))

    graph, allocated_flows, multicast_trees = \
        generate_bandwidth_efficient_branch_aware_segment_routing_trees(G,
                                                                        flows)

    for index, tree in enumerate(multicast_trees):
        draw_topology(tree, pos, title='BBSRT' + str(index))


def test_2():
    G = nx.Graph()
    G.source = 0
    G.add_path([0, 1, 2, 3])

    print(compute_intersection_node(G, [0, 5]))
    print(compute_intersection_node(G, [0, 1]))
    print(compute_intersection_node(G, [0, 1, 4]))
    print(compute_intersection_node(G, [0, 1, 2, 3, 4]))
    print('-----------------------')

    G.add_path([0, 1, 2, 4])
    print(compute_intersection_node(G, [0, 5]))
    print(compute_intersection_node(G, [0, 1, 2, 5]))
    print(compute_intersection_node(G, [0, 1, 2]))
    print(compute_intersection_node(G, [0, 1, 2, 4, 6]))
    print(compute_intersection_node(G, [0, 1, 5]))


if __name__ == '__main__':
    test_1()
    test_2()
