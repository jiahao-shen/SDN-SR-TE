"""
@project: RoutingAlgorithm
@author: sam
@file test_st.py
@ide: PyCharm
@time: 2019-03-04 18:13:06
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.steiner_tree import *


@count_time
def test_1():
    """Test no cycle in ST
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        st = SteinerTree(G, flows)

        for T in st.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    st = SteinerTree(G, flows)
    st.draw()
    print(st.network_performance())
