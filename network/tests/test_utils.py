"""
@project: RoutingAlgorithm
@author: sam
@file test_utils.py
@ide: PyCharm
@time: 2019-03-04 17:57:41
@blog: https://jiahaoplus.com
"""
import random
from network import *
from algorithm.shortest_path_tree import *


def test_1():
    """Test function draw_result
    :return:
    """

    def generate_test_result():
        result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}}

        for key in result:
            for index in range(10, 70, 10):
                result[key][index] = random.randint(10, 100)
        return result

    results = generate_test_result()
    draw_result(results, 'x', 'y', type='bar')


def test_2():
    """Test function compute_throughput
    :return:
    """
    G = NetworkTopo(100)
    flows = MulticastFlows(G, 1, 5, 100, 100)

    spt = ShortestPathTree(G, flows)
    assert spt.compute_throughput() == 500


def test_3():
    """Test function compute_path_cost
    :return:
    """
    G = nx.Graph()
    G.add_edge(0, 1, weight=10)
    G.add_edge(1, 5, weight=5)
    G.add_edge(1, 2, weight=3)
    G.add_edge(1, 4, weight=6)
    G.add_edge(2, 3, weight=7)
    G.add_edge(2, 6, weight=1)
    G.add_edge(6, 7, weight=8)
    G.add_edge(4, 8, weight=20)

    pos = graphviz_layout(G, prog='dot')
    draw_topology(G, pos, edge_attribute='weight')

    assert compute_path_cost(G, [0, 1, 2], 'weight') == 13
    assert compute_path_cost(G, [0, 1, 5], 'weight') == 15
    assert compute_path_cost(G, [0, 1, 2, 3], 'weight') == 20
    assert compute_path_cost(G, [0, 1, 2, 6], 'weight') == 14
    assert compute_path_cost(G, [0, 1, 2, 6, 7], 'weight') == 22
    assert compute_path_cost(G, [0, 1, 4], 'weight') == 16
    assert compute_path_cost(G, [0, 1, 4, 8], 'weight') == 36


@count_time
def test_4():
    """Test decorator count_time
    :return:
    """
    cnt = 1
    for i in range(1000):
        for j in range(1000):
            cnt += i + j


def test_5():
    """Test function compute_acyclic_sub_path
    :return:
    """
    T = nx.Graph()
    nx.add_path(T, [0, 1, 2, 3])
    nx.add_path(T, [0, 1, 2, 4])

    path = [0, 5, 2, 6]
    assert acyclic_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 6]
    assert acyclic_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 4, 6]
    assert acyclic_sub_path(T, path) == [4, 6]

    path = [0, 4, 3, 6]
    assert acyclic_sub_path(T, path) == [3, 6]

    path = [0, 5, 1, 6, 2, 7]
    assert acyclic_sub_path(T, path) == [2, 7]
