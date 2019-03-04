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
    """Test Steiner Tree and Widest Steiner Tree
    :return:
    """
    G, pos = generate_topology(100)
    flows = generate_flow_requests(G, 2, 10)

    draw_topology(G, pos)

    # ST
    graph, allocated_flows, steiner_trees = generate_steiner_trees(G, flows)

    output_flows(allocated_flows)

    for T in steiner_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='ST')

    print(compute_num_branch_nodes(steiner_trees))

    # WST
    graph, allocated_flows, widest_steiner_trees = \
        generate_widest_steiner_trees(G, flows)

    output_flows(allocated_flows)

    for T in widest_steiner_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='WST')

    print(compute_num_branch_nodes(widest_steiner_trees))
