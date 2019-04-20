"""
@project: RoutingAlgorithm
@author: sam
@file test_bbsrt.py
@ide: PyCharm
@time: 2019-03-04 18:42:41
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.bandwidth_efficient_branch_aware_segment_routing_tree import *
from algorithm.shortest_path_tree import *


def test_1():
    for _ in range(1):
        G = generate_topology(100)
        flows = generate_flow_requests(G, 1, 40)

        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(G,
                                                                            flows)

        for T in multicast_trees:
            if len(nx.cycle_basis(T)) != 0:
                pos = graphviz_layout(T, prog='dot')
                draw_topology(T, pos)
            # print(nx.cycle_basis(T))
            # assert len(nx.cycle_basis(T)) == 0


def test_2():
    """Test the function of compute_intersection_node
    :return:
    """
    G = nx.Graph()
    G.root = 0
    G.add_path([0, 1, 2, 3])

    assert compute_intersection_node(G, [0, 1]) == (None, False)
    assert compute_intersection_node(G, [0, 1, 4]) == (1, True)
    assert compute_intersection_node(G, [0, 1, 2, 3, 4]) == (3, False)

    G.add_path([0, 1, 4])
    assert compute_intersection_node(G, [0, 1, 5]) == (1, False)
    assert compute_intersection_node(G, [0, 1, 4, 5]) == (4, False)


def test_3():
    G = generate_topology()

    eb = nx.edge_betweenness_centrality(G)
    nb = nx.betweenness_centrality(G)

    nx.set_edge_attributes(G, 0, 'weight')
    nx.set_node_attributes(G, 0, 'weight')
    G = generate_weighted_graph(G, nb, eb, 0.5, 0.5)

    paths = generate_k_shortest_paths(G, 0, 2, 5, 'weight')

    for p in paths:
        print(p, ',', compute_path_cost(G, p, 'weight'))


def test_4():
    G = generate_topology(100)

    nx.set_edge_attributes(G, 0, 'weight')

    for e in G.edges(data=True):
        e[2]['weight'] = random.uniform(0, 1)

    src = random.choice(list(G.nodes))
    dsts = random.sample(G.nodes, 5)

    T = nx.Graph()
    T.root = src

    for d in dsts:
        k_paths = generate_k_shortest_paths(G, src, d, 5, weight='weight')
        path = k_paths[1]
        print(path)
        T.add_path(path)

    pos = graphviz_layout(T, prog='dot')

    draw_topology(T, pos)
