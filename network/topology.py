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
import networkx as nx
import os

warnings.filterwarnings('ignore')

__all__ = [
    'generate_topology',
    'generate_flow_requests',
    'load_topology_zoo',
]


def generate_topology(size=100, a=0.2, b=0.2,
                      link_capacity=1000, flow_limit=1000):
    """Generate a randomly topology using Waxman Method
    B. M. Waxman, "Routing of multipoint connections,"
    IEEE Journal on Selected Areas in Communications, vol. 6, no. 9, pp.
    1617-1622, December 1988.
    :param size: The number of nodes in topology, default 100
    :param a: Alpha (0, 1] float, default 0.2
    :param b: Beta (0, 1] float, default 0.2
    :param link_capacity: The link capacity in topology, here we consider all
                          of them are same, equal to 1GB(1000MB)
    :param flow_limit: The maximum number of flow entries, default 1000
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

    return G


def generate_flow_requests(G,
                           flow_groups=1, flow_entries=5,
                           size_lower=10, size_upper=100):
    """According the graph G, generate flow requests for multicast
    :param G: The topology graph
    :param flow_groups: The number of flow groups, default 1
    :param flow_entries: The number of flow entries in each group, default 5
    :param size_lower: The minimum size of flow, default 10MB
    :param size_upper: The maximum size of flow, default 100MB
    :return: flows
    """
    # Initialize flows
    flows = []

    # Flow groups or flow entries can't be more than terminals
    if flow_entries + 1 > len(G):
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
        for dst in random.sample(nodes, flow_entries):
            # Set the path to None
            destinations[dst] = None
        # Randomly generate flow size
        size = round(random.uniform(size_lower, size_upper), 2)
        # Set the src, dst and size
        f['src'] = src
        f['dst'] = destinations
        f['size'] = size
        # Append the flow to flows
        flows.append(f)

    return flows


def load_topology_zoo(file=None, link_capacity=1000, flow_limit=1000):
    """Load graphml from topology zoo
    :param file: The path of file, default None
    :param link_capacity: The link capacity in topology, here we consider all
                          of them are same, equal to 1GB(1000MB)
    :param flow_limit: The maximum number of flow entries, default 1000
    :return: G
    """
    # Load the default graphml
    if file is None:
        file = os.path.dirname(os.path.dirname(__file__)) + \
               '/topologyzoo/example.graphml'

    G = nx.DiGraph(nx.read_graphml(file))

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

    return G
