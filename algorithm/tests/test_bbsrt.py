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
    """Test no cycle in BBSRT
    :return:
    """
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                G, flows)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0
