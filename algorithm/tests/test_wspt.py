"""
@project: RoutingAlgorithm
@author: sam
@file test_wspt.py
@ide: PyCharm
@time: 2019-03-04 18:13:15
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.widest_shortest_path_tree import *


@count_time
def test_1():
    """Test no cycle in WSPT
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        spt = WidestShortestPathTree(G, flows)

        for T in spt.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    wspt = WidestShortestPathTree(G, flows)
    wspt.draw()
    print(wspt.network_performance())
