"""
@project: RoutingAlgorithm
@author: sam
@file test_wst.py
@ide: PyCharm
@time: 2019-03-04 18:13:27
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm import *


def test_1():
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(G, flows)

        for T in multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    G = generate_topology()
    flows = generate_flow_requests(G, 1, 40)

    graph, allocated_flows, multicast_trees = \
        generate_widest_steiner_trees(G, flows)

    for T in multicast_trees:
        print(len(T))

    graph, allocated_flows, multicast_trees = \
        generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows)

    for T in multicast_trees:
        print(len(T))
