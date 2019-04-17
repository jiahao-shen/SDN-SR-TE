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
    G = generate_topology(100)
    pos = graphviz_layout(G)
    draw_topology(G, pos)
    flows = generate_flow_requests(G, 1, 20)
    src = flows[0]['src']
    dst = flows[0]['dst'].keys()

    all_pair_shortest_paths = nx.shortest_path(G)

    tree = edge_optimization_phase(src, dst, all_pair_shortest_paths)

    position = graphviz_layout(tree, prog='dot')
    draw_topology(tree, position)

    tree = branch_optimization_phase(G, src, dst, tree,
                                     all_pair_shortest_paths)

    position = graphviz_layout(tree, prog='dot')
    draw_topology(tree, position)
