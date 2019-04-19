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
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, multicast_trees = \
            generate_branch_aware_steiner_trees(G, flows, 5)

        for T in multicast_trees:
            if len(nx.cycle_basis(T)) != 0:
                pos = graphviz_layout(G, prog='dot')
                draw_topology(T, pos)


def test_2():
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 20, 40)

        all_pair_paths = nx.shortest_path(G)

        src = flows[0]['src']
        dst = flows[0]['dst'].keys()

        T_1 = edge_optimization_phase(src, dst, all_pair_paths)

        branch_optimization_phase(src, dst, T_1, all_pair_paths, 5)
