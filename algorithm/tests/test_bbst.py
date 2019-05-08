"""
@project: SDN-SR-TE
@author: sam
@file test_bbst.py
@ide: PyCharm
@time: 2019-04-20 14:35:33
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.bandwidth_efficient_branch_aware_steiner_tree import *


@count_time
def test_1():
    """Test no cycle in BBST
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        bbst = BandwidthefficientBranchawareSteinerTree(G, flows,
                                                        alpha=0.5, beta=0.5,
                                                        w1=1, w2=5)

        for T in bbst.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    bbst = BandwidthefficientBranchawareSteinerTree(G, flows,
                                                    alpha=0.5, beta=0.5,
                                                    w1=1, w2=5)
    bbst.draw()
