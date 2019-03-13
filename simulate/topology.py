"""
@project: SDN-SR-TE
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-03-11 21:32:16
@blog: https://jiahaoplus.com
"""
import sys

sys.path.append('..')

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import Controller
from mininet.log import info, setLogLevel


class RandomScaleFreeTopo(Topo):

    def __init__(self, G, *args, **params):
        super().__init__(*args, **params)

        info('*** RandomScaleFreeTopo init\n')

        for v in G.nodes():
            if G.degree(v) == 1:
                self.addHost(str(v))
            else:
                self.addSwitch(str(v))

        for e in G.edges(data=True):
            self.addLink(str(e[0]), str(e[1]), bw=e[2]['link_capacity'])


def main():
    pass


if __name__ == '__main__':
    setLogLevel('info')
    main()
