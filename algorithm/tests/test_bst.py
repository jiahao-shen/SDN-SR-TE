"""
@project: RoutingAlgorithm
@author: sam
@file test_bst.py
@ide: PyCharm
@time: 2019-03-04 18:42:52
@blog: https://jiahaoplus.com
"""
from algorithm.branch_aware_steiner_tree import *
from algorithm.steiner_tree import *
from network import *


def test_1():
    """Test no cycle in BST
    :return:
    """
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, trees = \
            generate_branch_aware_steiner_trees(G, flows, 5)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0


@count_time
def test_2():
    """Test the effect of BST
    :return:
    """
    times = 100
    groups = 20
    w = 5
    cnt = 0

    for _ in range(times):
        G = generate_topology()
        flows = generate_flow_requests(G, groups, 40)

        graph, allocated_flows, trees = generate_steiner_trees(G, flows)
        res1 = []
        for T in trees:
            res1.append(compute_objective_value(T, w))

        graph, allocated_flows, trees = generate_branch_aware_steiner_trees(
            G, flows, w)
        res2 = []
        for T in trees:
            res2.append(compute_objective_value(T, w))

        for i in range(len(res1)):
            if res2[i] > res1[i]:
                cnt += 1


    percent = cnt * 100 / (times * groups)

    print('Percent:%.2f%%' % percent)
