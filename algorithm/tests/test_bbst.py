"""
@project: SDN-SR-TE
@author: sam
@file test_bbst.py
@ide: PyCharm
@time: 2019-04-20 14:35:33
@blog: https://jiahaoplus.com
"""
from network.topology import *
from network.utils import *
from algorithm.bandwidth_efficient_branch_aware_steiner_tree import *
from algorithm.shortest_path_tree import *


@count_time
def test_1():
    # for _ in range(10):
    G = generate_topology()
    flows = generate_flow_requests(G, 10, 40)

    graph, allocated_flows, multicast_trees = \
        generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows)

    # for T in multicast_trees:
    #     pos = graphviz_layout(T, prog='dot')
    #     draw_topology(T, pos)
    #
    # print(compute_num_branch_nodes(multicast_trees))

    # graph, allocated_flows, multicast_trees = \
    #     generate_shortest_path_trees(G, flows)

    # for T in multicast_trees:
    #     pos = graphviz_layout(T, prog='dot')
    #     draw_topology(T, pos)

    # print(compute_num_branch_nodes(multicast_trees))
