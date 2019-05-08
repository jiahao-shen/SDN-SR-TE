"""
@project: RoutingAlgorithm
@author: sam
@file test_spt.py
@ide: PyCharm
@time: 2019-03-04 18:12:54
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.shortest_path_tree import *


@count_time
def test_1():
    """Test no cycle in SPT
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        spt = ShortestPathTree(G, flows)

        for T in spt.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    spt = ShortestPathTree(G, flows)
    spt.draw()
    print(spt.network_performance())
