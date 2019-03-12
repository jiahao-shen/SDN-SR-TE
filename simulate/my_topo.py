"""
@project: SDN-SR-TE
@author: sam
@file my_topo.py
@ide: PyCharm
@time: 2019-03-11 21:32:16
@blog: https://jiahaoplus.com
"""
import sys

sys.path.append('..')

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from network import *


class MyTopology(Topo):

    def __init__(self):
        super(MyTopology, self).__init__()
        G = generate_topology()

        for v in G.nodes():
            if G.degree(v) == 1:
                self.addHost(str(v))
            else:
                self.addSwitch(str(v))

        for e in G.edges():
            self.addLink(str(e[0]), str(e[1]))


def test_topo():
    topo = MyTopology()
    net = Mininet(topo)
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    test_topo()
