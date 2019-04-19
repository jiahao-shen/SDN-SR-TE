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


def test_1():
    for _ in range(100):
        G = generate_topology(100)
        flows = generate_flow_requests(G, 2, 10)

        graph, allocated_flows, steiner_trees = generate_steiner_trees(G, flows)

        for T in steiner_trees:
            assert len(nx.cycle_basis(T)) == 0

