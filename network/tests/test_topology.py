"""
@project: RoutingAlgorithm
@author: sam
@file test_topology.py
@ide: PyCharm
@time: 2019-03-04 17:57:27
@blog: https://jiahaoplus.com
"""
from network import *


def test_1():
    """Test class NetworkTopo
    :return:
    """
    G = NetworkTopo()
    G.draw()
    G.draw_degree_distribution()

    G = NetworkTopo(size=20, a=0.8, b=0.6)
    G.draw()
    G.draw_degree_distribution()

    G = NetworkTopo(method='file')
    G.draw()
    G.draw_degree_distribution()

    G = NetworkTopo(method='file',
                    file='../../topologyzoo/sources/Colt.graphml')
    G.draw()
    G.draw_degree_distribution()


def test_2():
    """Test class MulticastFlows
    :return:
    """
    G = NetworkTopo()
    flows = MulticastFlows(G)
    flows.output()

    G = NetworkTopo(method='file',
                    file='../../topologyzoo/sources/Colt.graphml')
    flows = MulticastFlows(G, 2, 10)
    flows.output()
