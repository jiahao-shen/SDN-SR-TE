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

