"""
@project: RoutingAlgorithm
@author: sam
@file test_bst.py
@ide: PyCharm
@time: 2019-03-04 18:42:52
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.steiner_tree import *
from algorithm.branch_aware_steiner_tree import *


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


def test_3():
    w = 10
    cnt = 0
    times = 10
    groups = 50

    for _ in range(times):
        G = NetworkTopo()
        flows = MulticastFlows(G, groups, 40)

        st = SteinerTree(G, flows)
        res1 = []
        for T in st.multicast_trees:
            res1.append(compute_objective_value(T, w))

        bst = BranchawareSteinerTree(G, flows, w=w)
        res2 = []
        for T in bst.multicast_trees:
            res2.append(compute_objective_value(T, w))

        for i in range(len(res1)):
            if res1[i] <= res2[i]:
                cnt += 1

    print(cnt * 100 / (times * groups))
