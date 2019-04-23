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


@count_time
def test_1():
    """Test no cycle in SPT
    :return:
    """
    for _ in range(100):
        G = generate_topology(100)
        flows = generate_flow_requests(G, 10, 10)

        graph, allocated_flows, trees = \
            generate_shortest_path_trees(G, flows)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0
