"""
@project: RoutingAlgorithm
@author: sam
@file test_wst.py
@ide: PyCharm
@time: 2019-03-04 18:13:27
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.widest_steiner_tree import *


@count_time
def test_1():
    """Test no cycle in WST
    :return:
    """
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, trees = generate_widest_steiner_trees(G, flows)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0
