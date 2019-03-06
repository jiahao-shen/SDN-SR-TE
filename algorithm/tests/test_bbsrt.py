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
    G, pos = generate_topology(100)
    flows = generate_flow_requests(G, 10, 40)

    draw_topology(G, pos)

    graph, allocated_flows, multicast_trees = \
        generate_shortest_path_trees(G, flows)

    print(compute_num_branch_nodes(multicast_trees))

    for T in multicast_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='SPT')
        assert len(nx.cycle_basis(T)) == 0

    graph, allocated_flows, multicast_trees = \
        generate_bandwidth_efficient_branch_aware_segment_routing_trees(G,
                                                                        flows,
                                                                        w2=5)

    print(compute_num_branch_nodes(multicast_trees))

    for T in multicast_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='BBSRT')
        assert len(nx.cycle_basis(T)) == 0


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
