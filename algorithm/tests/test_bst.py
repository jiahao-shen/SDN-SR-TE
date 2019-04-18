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
    for _ in range(1000):
        G = generate_topology(100)
        flows = generate_flow_requests(G, 1, 20)

        src = flows[0]['src']
        dst = flows[0]['dst'].keys()

        all_pair_paths = nx.shortest_path(G)

        tree_1 = edge_optimization_phase(src, dst, all_pair_paths)
        pos_1 = graphviz_layout(tree_1)
        a = compute_objective_value(tree_1, 10)

        tree_2 = branch_optimization_phase(src, dst, tree_1, all_pair_paths)
        pos_2 = graphviz_layout(tree_2)
        b = compute_objective_value(tree_2, 10)

        if a != b:
            draw_topology(tree_1, pos_1, title=a)
            draw_topology(tree_2, pos_2, title=b)


def test_2():
    G = nx.Graph()
    G.add_node(1)
    v = 1
    if v in G.nodes:
        print('fuck')
