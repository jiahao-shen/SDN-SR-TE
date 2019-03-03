"""
@project: RoutingAlgorithm
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-01-30 15:27:54
@blog: https://jiahaoplus.com
"""
from network.utils import *
import warnings
import random
import networkx as nx

warnings.filterwarnings('ignore')


def generate_topology(size=20, a=0.7, b=0.7, link_capacity=1000,
                      flow_limit=100):
    """Generate a randomly topology
    :param size: The number of nodes in topology, default 20
    :param a: Alpha (0, 1] float in Waxman method, default 0.7
    :param b: Beta (0, 1] float in Waxman method, default 0.7
    :param link_capacity: The link capacity in topology, here we consider all
                          of them are same, equal to 1GB(1000MB)
    :param flow_limit: The maximum number of flow entries, default 100
    :return: G, pos
    """
    # References: B. M. Waxman, "Routing of multipoint connections",
    # IEEE Journal on Selected Areas in Communications, vol. 6, no. 9, pp.
    # 1617-1622, December 1988.
    # Randomly generate number of core nodes in topology
    n = random.randint(size // 3, size // 2)
    # Generate the waxman graph of core nodes
    G = nx.waxman_graph(n, alpha=a, beta=b)
    # Maximum number of tries to create a graph
    tries = 0
    # If graph isn't connected
    while not nx.is_connected(G):
        # Regenerate it again
        G = nx.waxman_graph(n, alpha=a, beta=b)
        tries += 1
        # If tries bigger than 100 times, raise Error
        if tries >= 100:
            raise RuntimeError('The parameter alpha and beta isn\'t'
                               'appropriate, please change other values ')
    # Get all core nodes in topology
    core_nodes = list(G.nodes)
    # For all edge nodes
    for v in range(n, size):
        # Randomly choice core nodes in topology
        u = random.choice(core_nodes)
        # Add edge between edge node and core node
        G.add_edge(v, u)

    # Add edge attributes
    # Add link capacity for all edges
    nx.set_edge_attributes(G, link_capacity, 'link_capacity')
    # Add residual bandwidth for all edges
    nx.set_edge_attributes(G, link_capacity, 'residual_bandwidth')

    # Add node attributes
    # Add flow limit for all nodes
    nx.set_node_attributes(G, flow_limit, 'flow_limit')
    # Add residual flow entries for all nodes
    nx.set_node_attributes(G, flow_limit, 'residual_flow_entries')

    # Get the layout of graph, here we use random_layout
    pos = nx.spring_layout(G)

    return G, pos


def generate_flow_requests(G, flow_groups=1, flow_entries=5, size_lower=10,
                           size_upper=100):
    """According the graph G, generate flow requests for multicast
    :param G: The topology graph
    :param flow_groups: The number of flow groups, default 1
    :param flow_entries: The number of flow entries in each group, default 5
    :param size_lower: The minimum size of flow, default 10MB
    :param size_upper: The maximum size of flow, default 100MB
    :return: flows
    """
    # Here we define the node whose degree is one as edge node
    terminals = set()
    for v in G.nodes:
        if G.degree(v) == 1:
            terminals.add(v)

    # Initialize flows
    flows = []

    # Flow groups or flow entries can't be more than terminals
    if flow_groups > len(terminals) or flow_entries > len(terminals):
        raise RuntimeError('Flow_groups and flow_entries cannot '
                           'be more than len(G)')

    # Randomly generate several source nodes
    # Traverse the source nodes in flows
    for src in random.sample(terminals, flow_groups):
        # Initialize flow
        f = {}
        # Generate the destination nodes from G
        nodes = set(terminals)
        # Remove the source from nodes
        nodes.remove(src)
        # Destination nodes initialize
        destinations = {}
        # Traverse the destination nodes
        for dst in random.sample(nodes, flow_entries):
            # Set the path to None
            destinations[dst] = None
        # Randomly generate flow size
        size = random.randint(size_lower, size_upper)
        # Set the src, dst and size
        f['src'] = src
        f['dst'] = destinations
        f['size'] = size
        # Append the flow to flows
        flows.append(f)

    return flows


def test():
    G, pos = generate_topology(50)
    flows = generate_flow_requests(G)

    draw_topology(G, pos)
    output_flows(flows)


if __name__ == '__main__':
    test()
