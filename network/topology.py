"""
@project: RoutingAlgorithm
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-01-30 15:27:54
@blog: https://jiahaoplus.com
"""
# from networkx.drawing.nx_agraph import graphviz_layout
import warnings
import random
import networkx as nx

warnings.filterwarnings('ignore')


def generate_topology(size=20, a=0.41, b=0.54, c=0.05,
                      link_capacity=1000, flow_limit=100):
    """Generate a randomly topology using Scale Free model
    :param size: The number of nodes in topology, default 20
    :param a: Alpha (0, 1] float, default 0.41
    :param b: Beta (0, 1] float, default 0.54
    :param c: Gamma (0, 1] float, default 0.05
              The sum of a, b, c must be 1
    :param link_capacity: The link capacity in topology, here we consider all
                          of them are same, equal to 1GB(1000MB)
    :param flow_limit: The maximum number of flow entries, default 100
    :return: G, pos
    """
    # Generate a scale free graph
    # Whose degree of nodes are obeying the power law distribution
    G = nx.Graph(nx.scale_free_graph(size, alpha=a, beta=b, gamma=c))
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

    # Get the layout of graph, here we use graphviz_layout
    # pos = graphviz_layout(G)

    # return G, pos
    return G


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
    terminals = []
    for v in G.nodes:
        if G.degree(v) == 1:
            terminals.append(v)

    # Initialize flows
    flows = []

    # Flow groups or flow entries can't be more than terminals
    if flow_entries + 1 > len(terminals):
        raise RuntimeError('Flow entries cannot be more than len(G)')

    # Randomly generate several source nodes
    # Traverse the source nodes in flows
    for _ in range(flow_groups):
        src = random.choice(terminals)
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
