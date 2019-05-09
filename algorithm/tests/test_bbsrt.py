"""
@project: RoutingAlgorithm
@author: sam
@file test_bbsrt.py
@ide: PyCharm
@time: 2019-03-04 18:42:41
@blog: https://jiahaoplus.com
"""
import random
from networkx.utils import pairwise
from network import *
from algorithm.bandwidth_efficient_branch_aware_segment_routing_tree import *


def test_1():
    """Test no cycle in BBSRT
    :return:
    """
    for _ in range(100):
        G = NetworkTopo()
        flows = MulticastFlows(G, 10, 40)

        bbsrt = BandwidthefficientBranchawareSegmentRoutingTree(G, flows)
        for T in bbsrt.multicast_trees:
            assert len(nx.cycle_basis(T)) == 0


def test_2():
    """
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G, 10, 40, 100, 500)

    bbsrt = BandwidthefficientBranchawareSegmentRoutingTree(G, flows)
    bbsrt.draw()


def test_3():
    """Test function generate_k_shortest_path
    :return:
    """
    G = NetworkTopo(100)
    nx.set_edge_attributes(G, 0, 'weight')

    for e in G.edges(data=True):
        e[2]['weight'] = random.randint(10, 100)

    for _ in range(1 << 10):
        src, dst = random.sample(list(G.nodes), 2)
        paths = k_shortest_paths(G, src, dst, k=5, weight='weight')

        for p1, p2 in pairwise(paths):
            assert compute_path_cost(G, p1, 'weight') <= \
                   compute_path_cost(G, p2, 'weight')
