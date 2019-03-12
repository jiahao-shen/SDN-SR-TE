"""
@project: RoutingAlgorithm
@author: sam
@file test_topology.py
@ide: PyCharm
@time: 2019-03-04 17:57:27
@blog: https://jiahaoplus.com
"""
from network import *
from networkx.drawing.nx_agraph import graphviz_layout


def test_1():
    """Test the connection of scale free graph in networkx
    :return:
    """
    for i in range(1 << 10):
        G = nx.Graph(nx.scale_free_graph(100))
        assert nx.is_connected(G) == True


def test_2():
    """Test the function of count_degree
    :return:
    """
    G, pos = generate_topology(100)
    cnt = count_degree(G)
    print(cnt)


def test_3():
    """Test the node whose degree is one
    :return:
    """
    G = nx.Graph(nx.scale_free_graph(100))
    pos = graphviz_layout(G)

    draw_topology(G, pos)

    num_total = len(G)
    num_degree_one = 0

    for v in list(G.nodes()):
        if G.degree(v) == 1:
            G.remove_node(v)
            num_degree_one += 1

    draw_topology(G, pos)
    print(num_degree_one)

    assert len(G) + num_degree_one == num_total


def test_4():
    """Test the degree of terminals whether equal to 1
    :return:
    """
    G, pos = generate_topology(100)
    flows = generate_flow_requests(G, 10, 50)

    for f in flows:
        assert G.degree(f['src']) == 1

        for dst in f['dst']:
            assert G.degree(dst) == 1


def test_5():
    for _ in range(1 << 10):
        G = generate_topology()
        for e in G.edges():
            assert e[0] != e[1]

