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
from networkx.exception import NetworkXNoCycle


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
            try:
                nx.find_cycle(T, orientation='ignore')
                exit(-1)
            except NetworkXNoCycle:
                pass


def test_2():
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    wspt = WidestShortestPathTree(G, flows)
    wspt.draw()
    print(wspt.network_performance())
