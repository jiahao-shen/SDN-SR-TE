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
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        wst = WidestSteinerTree(G, flows)

        for T in wst.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    wst = WidestSteinerTree(G, flows)
    wst.draw()
    print(wst.network_performance())


def test_3():
    """Test function compute_path_minimum_bandwidth
    :return:
    """
    G = nx.Graph()
    G.add_edge(0, 1, residual_bandwidth=10)
    G.add_edge(1, 5, residual_bandwidth=5)
    G.add_edge(1, 2, residual_bandwidth=3)
    G.add_edge(1, 4, residual_bandwidth=6)
    G.add_edge(2, 3, residual_bandwidth=7)
    G.add_edge(2, 6, residual_bandwidth=1)
    G.add_edge(6, 7, residual_bandwidth=8)
    G.add_edge(4, 8, residual_bandwidth=20)
    G.add_edge(4, 9, residual_bandwidth=9)

    pos = graphviz_layout(G, prog='dot')
    draw_topology(G, pos, edge_attribute='residual_bandwidth')

    assert compute_path_minimum_bandwidth(G, [0, 1, 5]) == 5
    assert compute_path_minimum_bandwidth(G, [0, 1, 4, 9]) == 6
    assert compute_path_minimum_bandwidth(G, [0, 1, 4, 8]) == 6
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 3]) == 3
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 6]) == 1
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 6, 7]) == 1
