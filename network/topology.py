"""
@project: RoutingAlgorithm
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-01-30 15:27:54
@blog: https://jiahaoplus.com
"""
import warnings
import random
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from network.utils import *

warnings.filterwarnings('ignore')

__all__ = [
    'NetworkTopo',
    'MulticastFlows'
]


class NetworkTopo(nx.DiGraph):

    def __init__(self, method='waxman',
                 link_capacity=1000, flow_limit=1000, **kwargs):
        """Initialize a network topology
        :param method: The method of generating a graph('waxman', 'file')
        :param link_capacity: The link capacity in topology, here we consider
                              all of them are same, equal to 1GB(1000MB)
        :param flow_limit: The maximum number of flow entries, default 1000
        :param **kwargs
        :return:
        """
        # Initialize G
        G = None

        # Judge the method
        if method == 'waxman':
            # Get the attribute
            size = kwargs.get('size', 100)
            a = kwargs.get('a', 0.2)
            b = kwargs.get('b', 0.2)
            G = self.__waxman_graph(size, a, b)
        elif method == 'file':
            file = kwargs.get('file')
            G = self.__load_topology_zoo(file)
        elif method == 'ba':
            size = kwargs.get('size', 100)
            a = kwargs.get('a', 0.41)
            b = kwargs.get('b', 0.54)
            c = kwargs.get('c', 0.05)
            G = self.__scale_free_graph(size, a, b, c)

        super().__init__(G, **kwargs)

        # Set the attributes for graph
        self.link_capacity = link_capacity
        self.flow_limit = flow_limit

        # Add residual bandwidth for all edges
        nx.set_edge_attributes(self, link_capacity, 'residual_bandwidth')
        # Add residual flow entries for all nodes
        nx.set_node_attributes(self, flow_limit, 'residual_flow_entries')

    @classmethod
    def __waxman_graph(cls, size=100, a=0.2, b=0.2):
        """Generate a randomly topology using Waxman Method
        B. M. Waxman, "Routing of multipoint connections,"
        IEEE Journal on Selected Areas in Communications, vol. 6, no. 9, pp.
        1617-1622, December 1988.
        :param size: The number of nodes in topology, default 100
        :param a: Alpha (0, 1] float, default 0.2
        :param b: Beta (0, 1] float, default 0.2
        :return: G
        """
        # Randomly generate waxman graph
        G = nx.waxman_graph(size, a, b)
        # The cnt of tries
        cnt = 0
        # If the G isn't connected
        while not nx.is_connected(G):
            # Regenerate waxman graph again
            G = nx.waxman_graph(size, a, b)
            # The cnt of tries plus 1
            cnt += 1
            # If tries over 500 times, raise error
            if cnt >= 500:
                raise RuntimeError('Please choose appropriate alpha and beta')

        # Transfer to directed graph
        G = G.to_directed()

        return G

    @classmethod
    def __load_topology_zoo(cls, file=None):
        """Load graphml from topology zoo
        :param file: The path of file, default None
        :return: G
        """
        if file is None:
            file = os.path.dirname(os.path.dirname(__file__)) + \
                   '/topologyzoo/example.graphml'

        G = nx.Graph(nx.read_graphml(file)).to_directed()

        return G

    @classmethod
    def __scale_free_graph(cls, size=100, a=0.41, b=0.54, c=0.05):
        """Generate scale free graph
        :param size: The number of nodes in topology, default 100
        :param a: Alpha (0, 1] float, default 0.41
        :param b: Beta (0, 1] float, default 0.54
        :param c: Gamma (0, 1] float, default 0.05
        :return: G
        """
        # a + b + c == 1
        G = nx.Graph(nx.scale_free_graph(size, a, b, c))
        # Transfer to directed graph
        G = G.to_directed()

        return G


    def draw(self, title='Test'):
        """Draw the topology
        :param title: The title of figure
        :return:
        """
        pos = graphviz_layout(self)
        draw_topology(self, pos, title=title)


    def draw_degree_distribution(self, title=''):
        """Draw the distribution of degree
        :param title: The title of figure
        :return:
        """
        cnt = {}
        for v in self.nodes:
            if self.degree(v) in cnt.keys():
                cnt[self.degree(v)] += 1
            else:
                cnt[self.degree(v)] = 1
        cnt = dict(sorted(cnt.items(), key=lambda t: t[0]))

        x = cnt.keys()
        y = cnt.values()

        plt.rcParams['font.sans-serif'] = 'SimSun'
        plt.title(title)
        plt.scatter(x, y)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel('节点度', fontsize=20)
        plt.ylabel('个数', fontsize=20)
        plt.show()


class MulticastFlows(list):

    def __init__(self, G, flow_groups=1, group_size=5,
                 size_lower=10, size_upper=100):
        """According to graph G, generate flow requests for multicast
        :param G: The network topology
        :param flow_groups: The number of flow groups, default 1
        :param group_size: The size of each group, default 5
        :param size_lower: The minimum size of flow, default 10MB
        :param size_upper: The maximum size of flow, default 100MB
        """
        super().__init__()
        # Set the maximum delay
        self.delay = 0

        # Flow groups or flow entries can't be more than terminals
        if group_size + 1 > len(G):
            raise RuntimeError('Flow entries cannot be more than len(G)')

        # Randomly generate several source nodes
        # Traverse the source nodes in flows
        for _ in range(flow_groups):
            # Randomly choose source node from all nodes
            src = random.choice(list(G.nodes))
            # Initialize flow
            f = {}
            # Generate the destination nodes from G
            nodes = set(G.nodes)
            # Remove the source from nodes
            nodes.remove(src)
            # Destination nodes initialize
            destinations = {}
            # Traverse the destination nodes
            for dst in random.sample(nodes, group_size):
                # Set the path to None
                destinations[dst] = None
            # Randomly generate flow size
            size = round(random.uniform(size_lower, size_upper), 2)
            # Set the src, dst and size
            f['src'] = src
            f['dst'] = destinations
            f['size'] = size
            # Append the flow to flows
            self.append(f)

    def output(self):
        """Output flows
        :return:
        """
        for f in self:
            for dst in f['dst']:
                print(f['src'], '->', dst,
                      ':', f['dst'][dst], ',',
                      'size =', f['size'])
            print('--------------------------')
