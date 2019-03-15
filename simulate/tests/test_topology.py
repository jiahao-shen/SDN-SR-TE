"""
@project: SDN-SR-TE
@author: sam
@file test_topology.py
@ide: PyCharm
@time: 2019-03-13 15:54:41
@blog: https://jiahaoplus.com
"""
import sys

sys.path.append('../..')

from network import *
from simulate.topology import *


def test_1():
    """Test class Random ScaleFreeTopo
    :return:
    """
    cleanup()
    setLogLevel('info')

    G = generate_topology()
    topo = MyTopo(G)
    net = Mininet(topo)

    net.start()
    net.stop()


def test_2():
    """Test tree topo
    :return:
    """
    cleanup()
    setLogLevel('info')

    G = nx.Graph(nx.random_tree(20))
    net = Mininet(controller=Controller)
    net.addController('c0')

    for v in G.nodes():
        if G.degree(v) == 1:
            net.addHost(str(v))
        else:
            net.addSwitch(str(v))

    for e in G.edges():
        net.addLink(str(e[0]), str(e[1]))

    net.start()
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    test_1()
    test_2()
