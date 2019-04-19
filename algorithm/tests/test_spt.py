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
    for _ in range(100):
        G = generate_topology(100)
        flows = generate_flow_requests(G, 10, 10)

        graph, allocated_flows, shortest_path_trees = \
            generate_shortest_path_trees(G, flows)

        for T in shortest_path_trees:
            assert len(nx.cycle_basis(T)) == 0
