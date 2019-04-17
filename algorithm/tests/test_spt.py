"""
@project: RoutingAlgorithm
@author: sam
@file test_spt.py
@ide: PyCharm
@time: 2019-03-04 18:12:54
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.shortest_path_tree import *
import warnings

warnings.filterwarnings('ignore')


def test_1():
    G = generate_topology(100)
    pos = graphviz_layout(G)
    flows = generate_flow_requests(G, 2, 10)

    draw_topology(G, pos)

    graph, allocated_flows, shortest_path_trees = \
        generate_shortest_path_trees(G, flows)

    output_flows(allocated_flows)

    for T in shortest_path_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='SPT')
        assert len(nx.cycle_basis(T)) == 0

    print(compute_num_branch_nodes(shortest_path_trees))
