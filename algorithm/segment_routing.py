"""
@project: RoutingAlgorithm
@author: sam
@file segment_routing.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
from network.topology import *


def generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows):
    """According to the flows and graph, generate Bandwidth-efficient Branch-aware Segment Routing Tree(BBSRT)
    :param G: The origin graph
    :param flows: The flow request
    :return:
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    allocated_graph = nx.Graph()  # Allocated Graph(Only including path, without link capacity)
    allocated_graph.add_nodes_from(G)  # Add nodes from G to allocated_graph

    for src_node in flows:

        for dst_node in flows[src_node].keys():
            pass


def generate_weight_graph(G, alpha=0.5, beta=0.5):
    """
    :param G:
    :param alpha:
    :param beta:
    :return:
    """
    nx.set_edge_attributes(G, 0, 'weight')
    nx.set_node_attributes(G, 0, 'weight')

    node_betweenness_centrality = nx.betweenness_centrality(G, weight=None)
    edge_betweenness_centrality = nx.edge_betweenness_centrality(G, weight=None)

    for edge in G.edges(data=True):
        congestion_index = edge[2]['link_capacity'] / edge[2]['residual_bandwidth'] - 1
        betweenness_centrality = edge_betweenness_centrality[(edge[0], edge[1])]
        weight = alpha * congestion_index + (1 - alpha) * betweenness_centrality
        edge[2]['weight'] = weight

    for node in G.nodes():
        congestion_index = 0
        betweenness_centrality = node_betweenness_centrality[node]
        weight = beta * congestion_index + (1 - beta) * betweenness_centrality

    return G


def test():
    G, pos = generate_topology()

    draw_topology(G, pos, title='Topology')

    nx.set_node_attributes(G, 0, 'weight')

    print(G.nodes(data=True))


if __name__ == '__main__':
    test()
