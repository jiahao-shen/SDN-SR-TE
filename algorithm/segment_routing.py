"""
@project: RoutingAlgorithm
@author: sam
@file segment_routing.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
from network.topology import *
from itertools import islice
from collections import OrderedDict

"""
Sheu, J.-P., & Chen, Y.-C. (2017). 
A scalable and bandwidth-efficient multicast algorithm based on segment routing in software-defined networking. 
In 2017 IEEE International Conference on Communications (ICC) (pp. 1–6). IEEE. https://doi.org/10.1109/ICC.2017.7997197
"""


def generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows, k=2):
    """According to the flows and graph, generate Bandwidth-efficient Branch-aware Segment Routing Tree(BBSRT)
    :param G: The origin graph
    :param flows: The flow request
    :param k:
    :return:
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    band_efficient_branch_aware_segment_routing_trees = []  # Initialize

    # The node betweenness centrality
    nodes_betweenness_centrality = nx.betweenness_centrality(graph, weight=None)
    # The edge betweenness centrality
    edges_betweenness_centrality = nx.edge_betweenness_centrality(graph, weight=None)

    # Traverse the flows
    for f in allocated_flows:
        # Add weight for nodes and edges
        graph = generate_weighted_graph(graph, nodes_betweenness_centrality, edges_betweenness_centrality)
        # Dict to store k shortest paths for (source, destinations)
        d = {}
        # Sorted Dict to store cost of the shortest path
        d_sorted = {}
        # The multicast tree for current source node
        multicast_tree = nx.Graph()
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Compute the k shortest path from source to dst_node
            d[dst_node] = generate_k_shortest_path(graph, f['src'], dst_node, weight='weight')
            # Store the shortest path cost in d_sorted
            d_sorted[dst_node] = compute_path_cost(graph, d[dst_node][0], weight='weight')
        # Sort the dict by value
        d_sorted = OrderedDict(sorted(d_sorted.items(), key=lambda x: x[1]))
        # Traverse the destination nodes in d_sorted
        for dst_node in d_sorted:
            # Path initialize
            path = None
            # If the graph is empty
            if len(G) == 0:
                # Path equals the shortest path
                path = d[dst_node][0]
            # If the graph is not empty
            else:
                # Initialize the minimum cost
                minimum_cost = math.inf
                # Traverse the k shortest paths for dst_node
                for p in d[dst_node]:
                    # Compute the extra cost
                    extra_cost = compute_extra_cost(graph, p)
                    # If extra cost is smaller than minimum cost
                    if extra_cost < minimum_cost:
                        # Update minimum cost
                        minimum_cost = extra_cost
                        # Record current path
                        path = p
            # Check the current path whether valid
            if check_path_valid(graph, path, f['size']):
                # Record the path for pair(source, destination)
                f['dst'][dst_node] = path
                # Add the path into the multicast tree
                nx.add_path(multicast_tree, path)
                # Update the residual entries of nodes in graph
                update_node_entries(graph, path)

        # Update the residual bandwidth of edges in the multicast tree
        update_edge_bandwidth(graph, multicast_tree, f['size'])

        band_efficient_branch_aware_segment_routing_trees.append(multicast_tree)

    return graph, allocated_flows, band_efficient_branch_aware_segment_routing_trees


def compute_extra_cost(G, path, w1=1, w2=1):
    """Compute the extra cost for path
    :param G: The origin graph
    :param path: The path needs to add into the graph
    :param w1: The first parameter of extra cost, default 1
    :param w2: The second parameter of extra cost, default 2
    :return: extra_cost
    """
    tmp_graph = G.copy()  # The temp graph
    old_degree = dict(tmp_graph.degree)  # The old degree before path added
    nx.add_path(tmp_graph, path)  # Add path into temp graph
    new_degree = dict(tmp_graph.degree)  # The new degree after path added

    # Compute the branch node and flag(whether new branch node)
    branch_node, flag = compute_branch_node(old_degree, new_degree)
    # The final result
    extra_cost = 0
    # If there is no branch node
    if branch_node is None:
        # The extra cost equals to the whole path cost
        extra_cost += w1 * compute_path_cost(G, path, weight='weight')
    # If there exists branch node
    else:
        # Compute sub path from branch node to destination node
        sub_path = path[path.index(branch_node):]
        # The extra cost equals to the sub path cost
        extra_cost += w1 * compute_path_cost(G, sub_path, weight='weight')
        # If it's new branch node
        if flag:
            # Add the cost of branch node
            extra_cost += w2 * G.nodes[branch_node]['weight']

    return extra_cost


def compute_branch_node(old_degrees, new_degrees):
    """According to the degrees, check whether generate new branch node
    :param old_degrees: The degree of graph before path added into
    :param new_degrees: The degree of graph after path added into
    :return: node, Boolean
    """
    for node in old_degrees:
        # Is new branch node
        if new_degrees[node] > old_degrees[node] == 2:
            return node, True
        # Not new branch node
        elif new_degrees[node] > old_degrees[node] > 2:
            return node, False
    # No branch node
    return None, False


def generate_weighted_graph(G, nodes_betweenness_centrality, edges_betweenness_centrality, alpha=0.5, beta=0.5):
    """Generate the weighted graph according to the paper
    :param G: The origin graph
    :param nodes_betweenness_centrality:
    :param edges_betweenness_centrality:
    :param alpha: The parameter of edges for weight
    :param beta: The parameter of nodes for weight
    :return: weighted G
    """
    nx.set_edge_attributes(G, 0, 'weight')
    nx.set_node_attributes(G, 0, 'weight')

    for edge in G.edges(data=True):
        congestion_index = edge[2]['link_capacity'] / edge[2]['residual_bandwidth'] - 1
        betweenness_centrality = edges_betweenness_centrality[(edge[0], edge[1])]
        weight = alpha * congestion_index + (1 - alpha) * betweenness_centrality
        edge[2]['weight'] = weight

    for node in G.nodes(data=True):
        congestion_index = node[1]['flow_limit'] / node[1]['residual_flow_entries'] - 1
        betweenness_centrality = nodes_betweenness_centrality[node[0]]
        weight = beta * congestion_index + (1 - beta) * betweenness_centrality
        node[1]['weight'] = weight

    return G


def generate_k_shortest_path(G, source, destination, k=2, weight=None):
    """Generate the k shortest path from source to destination in G
    :param G: The origin graph
    :param source: The source node
    :param destination: The destination node
    :param k: The parameter in k shortest path, default 2
    :param weight: The weight value in shortest path algorithm, default None
    :return: The list of k shortest path
    """
    return list(islice(nx.shortest_simple_paths(G, source, destination, weight), k))


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
        else:
            # Else cost plus the edge weight
            cost += G[path[i]][path[i + 1]][weight]

    return cost


def test():
    G, pos = generate_topology()
    flows = generate_flow_requests(G)
    generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows)


if __name__ == '__main__':
    test()
