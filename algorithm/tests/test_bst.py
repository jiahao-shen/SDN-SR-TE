"""
@project: RoutingAlgorithm
@author: sam
@file test_bst.py
@ide: PyCharm
@time: 2019-03-04 18:42:52
@blog: https://jiahaoplus.com
"""
from algorithm.branch_aware_steiner_tree import *
from network import *


@count_time
def test_1():
    """Test no cycle in BST
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        bst = BranchawareSteinerTree(G, flows)

        for T in bst.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    bst = BranchawareSteinerTree(G, flows)
    bst.draw()

