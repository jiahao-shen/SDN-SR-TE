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
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        bbsrt = BandwidthefficientBranchawareSegmentRoutingTree(G, flows)
        for T in bbsrt.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    bbsrt = BandwidthefficientBranchawareSegmentRoutingTree(G, flows)
    bbsrt.draw()
