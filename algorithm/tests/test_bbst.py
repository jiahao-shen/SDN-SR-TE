"""
@project: SDN-SR-TE
@author: sam
@file test_bbst.py
@ide: PyCharm
@time: 2019-04-20 14:35:33
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.bandwidth_efficient_branch_aware_steiner_tree import *


@count_time
def test_1():
    """Test no cycle in BBST
    :return:
    """
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 5, 20)
        output_flows(flows)
        graph, allocated_flows, trees = \
            generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0

