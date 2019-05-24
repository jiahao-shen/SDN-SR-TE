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


def test_6():
    """
    :return:
    """
    # Lab1-1
    spt = {10: 4.6, 20: 8.1, 30: 11.0, 40: 13.9, 50: 15.8}
    st = {10: 4.0, 20: 6.9, 30: 9.4, 40: 11.8, 50: 13.6}
    wspt = {10: 4.6, 20: 8.2, 30: 11.3, 40: 14, 50: 16}
    wst = {10: 4.1, 20: 7.1, 30: 9.5, 40: 11.7, 50: 13.7}
    bst = {10: 3.6, 20: 6.2, 30: 8.6, 40: 11.4, 50: 13.2}
    bbsrt = {10: 4.2, 20: 7.9, 30: 10.5, 40: 13.0, 50: 15}
    bbst = {10: 2.4, 20: 4.8, 30: 7.2, 40: 9.6, 50: 11.3}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播成员个数', '分支节点数(个)')

    # Lab1-2
    spt = {10: 0.8, 20: 3.0, 30: 6.4, 40: 11, 50: 14.4}
    st = {10: 0, 20: 2.1, 30: 4.8, 40: 7.6, 50: 12.8}
    wspt = {10: 0, 20: 1.2, 30: 3.1, 40: 6.4, 50: 9.2}
    wst = {10: 0, 20: 1.0, 30: 3.3, 40: 6.1, 50: 8.1}
    bst = {10: 0, 20: 1.8, 30: 4.2, 40: 7, 50: 10.2}
    bbsrt = {10: 0, 20: 0.4, 30: 1.2, 40: 3.0, 50: 4.8}
    bbst = {10: 0, 20: 0.3, 30: 1.1, 40: 2.8, 50: 4.4}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播成员个数', '平均拒绝率(%)')

    # lab1-3
    spt = {10: 31000, 20: 57000, 30: 80000, 40: 104000, 50: 134000}
    st = {10: 31000, 20: 59000, 30: 83000, 40: 107000, 50: 139000}
    wspt = {10: 31500, 20: 58900, 30: 83400, 40: 109000, 50: 145000}
    wst = {10: 31600, 20: 58600, 30: 84000, 40: 112000, 50: 148000}
    bst = {10: 31400, 20: 58100, 30: 82000, 40: 106000, 50: 142000}
    bbsrt = {10: 31700, 20: 60500, 30: 86000, 40: 119000, 50: 159000}
    bbst = {10: 31800, 20: 61000, 30: 87000, 40: 121000, 50: 163000}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播成员个数', '吞吐量(MB/s)', type='bar')

    # Lab1-4
    spt = {10: 15.8, 20: 25.2, 30: 30.6, 40: 38, 50: 42}
    st = {10: 12, 20: 21, 30: 25, 40: 32.5, 50: 35.5}
    wspt = {10: 16, 20: 26.8, 30: 32, 40: 40.2, 50: 45}
    wst = {10: 11.8, 20: 21, 30: 26, 40: 32.2, 50: 38}
    bst = {10: 11.8, 20: 21.2, 30: 25.3, 40: 31.8, 50: 35.3}
    bbsrt = {10: 18.6, 20: 28.3, 30: 34.2, 40: 42.5, 50: 48}
    bbst = {10: 13, 20: 23, 30: 28.5, 40: 36, 50: 43}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播成员个数', '链路利用率(%)')

    # lab2-1
    spt = {10: 4.8, 20: 4.6, 30: 4.8, 40: 4.7, 50: 4.52, 60: 4.75, 70: 4.7}
    st = {10: 4.1, 20: 4.0, 30: 4.12, 40: 4.2, 50: 4.0, 60: 4.1, 70: 4.08}
    wspt = {10: 4.6, 20: 4.46, 30: 4.7, 40: 4.8, 50: 4.48, 60: 4.8, 70: 4.6}
    wst = {10: 4.08, 20: 3.98, 30: 4.05, 40: 4.1, 50: 4.0, 60: 4.15, 70: 4.06}
    bst = {10: 3.7, 20: 3.58, 30: 3.65, 40: 3.78, 50: 3.68, 60: 3.78, 70: 3.7}
    bbsrt = {10: 3.86, 20: 4.5, 30: 4.65, 40: 4.46, 50: 4.6, 60: 4.72, 70: 4.74}
    bbst = {10: 2.1, 20: 2.6, 30: 2.96, 40: 3.06, 50: 3.1, 60: 3.35, 70: 3.44}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '分支节点数(个)')

    # lab2-2
    spt = {10: 0, 20: 1.5, 30: 4, 40: 9.5, 50: 12, 60: 17, 70: 22}
    st = {10: 0, 20: 1.2, 30: 2.3, 40: 7.4, 50: 9, 60: 12.5, 70: 16.5}
    wspt = {10: 0, 20: 0.5, 30: 2.0, 40: 4.8, 50: 6.6, 60: 10.5, 70: 14.8}
    wst = {10: 0, 20: 0.5, 30: 2.0, 40: 4.7, 50: 6.7, 60: 9.2, 70: 12.6}
    bst = {10: 0, 20: 2, 30: 2.7, 40: 7.8, 50: 9.6, 60: 12.8, 70: 18}
    bbsrt = {10: 0, 20: 0.1, 30: 0.2, 40: 2.0, 50: 2.4, 60: 3.8, 70: 5.8}
    bbst = {10: 0, 20: 0.1, 30: 0.2, 40: 1.8, 50: 2.2, 60: 3.4, 70: 5.2}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '平均拒绝率(%)')

    # lab2-3
    spt = {10: 14000, 20: 31000, 30: 44000, 40: 56000, 50: 64000, 60: 73000, 70: 82000}
    st = {10: 14050, 20: 31500, 30: 45000, 40: 56400, 50: 67000, 60: 76000, 70: 86000}
    wspt = {10: 14150, 20: 31400, 30: 46000, 40: 58500, 50: 68000, 60: 78000, 70: 88500}
    wst = {10: 14250, 20: 31600, 30: 45900, 40: 57600, 50: 69000, 60: 80500, 70: 91000}
    bst = {10: 14050, 20: 31200, 30: 45200, 40: 56300, 50: 66500, 60: 76000, 70: 86500}
    bbsrt = {10: 14300, 20: 31700, 30: 47000, 40: 61000, 50: 72000, 60: 83500, 70: 98000}
    bbst = {10: 14450, 20: 32000, 30: 47500, 40: 61500, 50: 74000, 60: 86000, 70: 104000}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '吞吐量(MB/s)', type='bar')

    # lab3-3
    spt = {100: 20000, 200: 160000, 300: 360000, 400: 610000}
    st = {100: 21000, 200: 165000, 300: 365000, 400: 620000}
    wspt = {100: 24000, 200: 180000, 300: 405000, 400: 680000}
    wst = {100: 23000, 200: 181000, 300: 415000, 400: 700000}
    bst = {100: 22000, 200: 170000, 300: 390000, 400: 650000}
    bbsrt = {100: 33000, 200: 205000, 300: 470000, 400: 850000}
    bbst = {100: 34000, 200: 220000, 300: 490000, 400: 900000}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '网络大小', '吞吐量(MB/s)', type='bar')

    # lab4-1
    spt = {10: 7.2, 20: 7.18, 30: 7.1, 40: 7.15, 50: 7.03, 60: 7.1, 70: 6.9}
    st = {10: 5.85, 20: 6.04, 30: 6.05, 40: 5.9, 50: 5.95, 60: 5.75, 70: 6.02}
    wspt = {10: 7.2, 20: 7.16, 30: 7.15, 40: 7.05, 50: 7.0, 60: 7.08, 70: 6.9}
    wst = {10: 5.9, 20: 6.0, 30: 5.95, 40: 5.85, 50: 5.9, 60: 5.75, 70: 5.98}
    bst = {10: 5.72, 20: 5.92, 30: 5.9, 40: 5.8, 50: 5.82, 60: 5.65, 70: 5.88}
    bbsrt = {10: 6.3, 20: 6.73, 30: 6.7, 40: 6.65, 50: 6.6, 60: 6.63, 70: 6.7}
    bbst = {10: 5.3, 20: 5.63, 30: 5.55, 40: 5.5, 50: 5.48, 60: 5.35, 70: 5.58}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '分支节点数(个)')

    # lab4-2
    spt = {10: 2, 20: 26, 30: 39, 40: 45, 50: 53, 60: 58, 70: 61}
    st = {10: 1, 20: 22, 30: 34, 40: 42, 50: 47, 60: 54.5, 70: 58}
    wspt = {10: 1.8, 20: 25, 30: 37.5, 40: 44, 50: 51, 60: 56, 70: 60}
    wst = {10: 1.8, 20: 18, 30: 32, 40: 40, 50: 46, 60: 53, 70: 57}
    bst = {10: 0, 20: 21, 30: 33, 40: 41, 50: 48, 60: 55.5, 70: 58.5}
    bbsrt = {10: 0, 20: 7.5, 30: 22, 40: 33, 50: 40.5, 60: 48, 70: 52}
    bbst = {10: 0.5, 20: 9.5, 30: 21, 40: 29, 50: 37, 60: 45, 70: 50}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '平均拒绝率(%)')

    # lab4-3
    spt = {10: 16000, 20: 24000, 30: 31000, 40: 35000, 50: 37000, 60: 41000, 70: 44000}
    st = {10: 16500, 20: 25000, 30: 35000, 40: 41000, 50: 45000, 60: 47000, 70: 49500}
    wspt = {10: 16300, 20: 24300, 30: 32500, 40: 35500, 50: 38000, 60: 42000, 70: 45000}
    wst = {10: 17000, 20: 26000, 30: 34800, 40: 41500, 50: 46000, 60: 49000, 70: 50500}
    bst = {10: 16900, 20: 25700, 30: 33800, 40: 41200, 50: 45400, 60: 47500, 70: 49700}
    bbsrt = {10: 16950, 20: 29000, 30: 43500, 40: 48500, 50: 51500, 60: 57000, 70: 58000}
    bbst = {10: 17000, 20: 29900, 30: 47000, 40: 53000, 50: 57000, 60: 64000, 70: 66000}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '吞吐量(MB/s)', type='bar')

    # lab4-3
    spt = {10: 14, 20: 23, 30: 27, 40: 29.5, 50: 33, 60: 34, 70: 34.5}
    st = {10: 12, 20: 20.2, 30: 24.8, 40: 27.5, 50: 31.5, 60: 32, 70: 34}
    wspt = {10: 14.2, 20: 23.5, 30: 28, 40: 30.5, 50: 34, 60: 35.5, 70: 36.5}
    wst = {10: 12, 20: 22, 30: 25.5, 40: 28.5, 50: 32, 60: 33.2, 70: 34.5}
    bst = {10: 12, 20: 20.5, 30: 24.5, 40: 28, 50: 31.5, 60: 31, 70: 34}
    bbsrt = {10: 16, 20: 33, 30: 40, 40: 43, 50: 47, 60: 48, 70: 49}
    bbst = {10: 15.5, 20: 28, 30: 36, 40: 41, 50: 44.5, 60: 46, 70: 47}
    result = {'SPT': spt, 'ST': st,
              'WSPT': wspt, 'WST': wst,
              'BST': bst, 'BBSRT': bbsrt,
              'BBST': bbst}
    draw_result(result, '组播组个数', '链路利用率(%)')
