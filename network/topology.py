"""
@project: RoutingAlgorithm
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-01-30 15:27:54
@blog: https://jiahaoplus.com
"""
from figure.utils import *
import warnings
import random
import networkx as nx

warnings.filterwarnings('ignore')


def generate_topology(size=20, a=0.7, b=0.7, link_capacity=1000,
                      flow_limit=100):
    """Generate a topology using Waxman method
    :param size: The number of nodes in topology, default 20
    :param a: Alpha (0, 1] float in Waxman method, default 0.7
    :param b: Beta (0, 1] float in Waxman method, default 0.7
    :param link_capacity: The link capacity in topology, here we consider all
     of them are same, equal to 1GB(1000MB)
    :param flow_limit: The maximum number of flow entries, default 100
    :return: G, position
    """
    # Generate network topology using Waxman method
    # References: B. M. Waxman, "Routing of multipoint connections",
    # IEEE Journal on Selected Areas in Communications, vol. 6, no. 9, pp.
    # 1617-1622, December 1988.
    G = nx.waxman_graph(size, alpha=a, beta=b)
    # Count variables
    cnt = 0
    # If the graph is not connected
    while not nx.is_connected(G):
        # Generate the graph again
        G = nx.waxman_graph(size, alpha=a, beta=b)
        cnt += 1
        # If cnt is bigger than 100, raise exception
        if cnt >= 100:
            raise RuntimeError('The parameter alpha and beta is not '
                               'appropriate, please change other values')

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

    # Get the layout of graph, here we use spring_layout
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
    # Initialize flows
    flows = []

    # If flow groups or flow entries are more than nodes of G, raise exception
    if flow_groups > len(G) or flow_entries > len(G):
        raise RuntimeError('Flow_groups and flow_entries cannot '
                           'be more than len(G)')

    # Randomly generate several source nodes
    # Traverse the source nodes in flows
    for src_node in random.sample(G.nodes, flow_groups):
        # Initialize flow
        f = {}
        # Generate the destination nodes from G
        nodes = set(G.nodes)
        # Remove the source from nodes
        nodes.remove(src_node)
        # Destination nodes initialize
        dst_nodes = {}
        # Traverse the destination nodes
        for dst_node in random.sample(nodes, flow_entries):
            # Set the path to None
            dst_nodes[dst_node] = None
        # Randomly generate flow size
        size = random.randint(size_lower, size_upper)
        # Set the src, dst and size
        f['src'] = src_node
        f['dst'] = dst_nodes
        f['size'] = size
        # Append the flow to flows
        flows.append(f)

    return flows


def test():
    # Test function
    g, pos = generate_topology()
    draw_topology(g, pos)
    flows = generate_flow_requests(g, flow_groups=4, flow_entries=10)
    for item in flows:
        print(item)


if __name__ == '__main__':
    test()
