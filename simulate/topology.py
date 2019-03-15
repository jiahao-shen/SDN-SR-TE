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
from mininet.topolib import TreeTopo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.log import info, setLogLevel
from networkx.drawing.nx_agraph import graphviz_layout
from network import *
import yaml


class MyTopo(Topo):

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
    G = generate_topology()
    nx.write_graphml(G, 'topo.gml')

    flows = generate_flow_requests(G, 3, 5)
    nx.write_yaml(flows, 'flows.yaml')

    topo = MyTopo(G)
    net = Mininet(topo, controller=RemoteController('c0', ip='127.0.0.1',
                                                    port=8080))

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    # cleanup()

    main()
