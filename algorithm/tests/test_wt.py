"""
@project: RoutingAlgorithm
@author: sam
@file test_wt.py
@ide: PyCharm
@time: 2019-03-04 18:13:06
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.steiner_tree import *


def test_1():
    G, pos = generate_topology(100)
    flows = generate_flow_requests(G, 2, 10)

    draw_topology(G, pos)

    graph, allocated_flows, steiner_trees = generate_steiner_trees(G, flows)

    output_flows(allocated_flows)

    for T in steiner_trees:
        position = graphviz_layout(T, 'dot')
        draw_topology(T, position, title='SPT')
        assert len(nx.cycle_basis(T)) == 0

    print(compute_num_branch_nodes(steiner_trees))
