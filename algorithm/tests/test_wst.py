"""
@project: RoutingAlgorithm
@author: sam
@file test_wst.py
@ide: PyCharm
@time: 2019-03-04 18:13:27
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.widest_steiner_tree import *


@count_time
def test_1():
    """Test no cycle in WST
    :return:
    """
    for _ in range(100):
        pass


def test_2():
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    wst = WidestSteinerTree(G, flows)
    wst.draw()
    print(wst.network_performance())

