"""
@project: RoutingAlgorithm
@author: sam
@file test_wst.py
@ide: PyCharm
@time: 2019-03-04 18:13:27
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.steiner_tree import *
from algorithm.widest_steiner_tree import *


def test_1():
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(G, flows)

        for T in multicast_trees:
            assert len(nx.cycle_basis(T)) == 0

