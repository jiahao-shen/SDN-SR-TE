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


def test_1():
    G = generate_topology()
    flows = generate_flow_requests(G, 10, 30)

    graph, allocated_flows, trees = \
        generate_bandwidth_efficient_branch_aware_segment_routing_trees(G,
                                                                        flows)

    for T in trees:
        pos = graphviz_layout(T, prog='dot')
        draw_topology(T, pos)


def test_2():
    T = nx.Graph()
    T.add_path([0, 1, 2, 3])
    T.add_path([0, 1, 2, 4])

    path = [0, 5, 2, 6]
    assert compute_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 6]
    assert compute_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 4, 6]
    assert compute_sub_path(T, path) == [4, 6]

    path = [0, 4, 3, 6]
    assert compute_sub_path(T, path) == [3, 6]

    path = [0, 5, 1, 6, 2, 7]
    assert compute_sub_path(T, path) == [2, 7]
