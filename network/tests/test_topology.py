"""
@project: RoutingAlgorithm
@author: sam
@file test_topology.py
@ide: PyCharm
@time: 2019-03-04 17:57:27
@blog: https://jiahaoplus.com
"""
import os
import json
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


def test_3():
    """Count the number of nodes in topologyzoo
    :return:
    """
    path = '../../topologyzoo/sources/'
    files = os.listdir(path)

    result = {}

    for f in files:
        G = NetworkTopo(method='file', file=path+f)
        result[f] = len(G)

    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    with open('../../topologyzoo.json', 'w') as f:
        json.dump(result, f)


def test_4():
    G = NetworkTopo(method='file',
                    file='../../topologyzoo/sources/Kdl.graphml')

    G.draw()
    G.draw_degree_distribution()

    G = NetworkTopo(method='file',
                    file='../../topologyzoo/sources/Cogentco.graphml')

    G.draw()
    G.draw_degree_distribution()
