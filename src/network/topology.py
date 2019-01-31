"""
@project: RoutingAlgorithm
@author: sam
@file topology.py
@ide: PyCharm
@time: 2019-01-30 15:27:54
@blog: https://jiahaoplus.com
"""
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import random

warnings.filterwarnings('ignore')


def generate_topology(size=20, b=0.7, a=0.7, link_capacity=1000):
    """Generate a topology using Waxman method
    :param size: The number of nodes in topology
    :param b: Beta (0, 1] float in Waxman method, default 0.7
    :param a: Alpha (0, 1] float in Waxman method, default 0.7
    :param link_capacity: The link capacity in topology, here we consider all of them are same, equal to 1GB(1MB)
    :return: G, position
    """
    # Generate network topology using Waxman method
    # References: B. M. Waxman, "Routing of multipoint connections",
    # IEEE Journal on Selected Areas in Communications, vol. 6, no. 9, pp. 1617-1622, December 1988.
    G = nx.waxman_graph(size, beta=b, alpha=a)
    while not nx.is_connected(G):
        G = nx.waxman_graph(size, beta=b, alpha=a)

    # Add link capacity for all edges
    nx.set_edge_attributes(G, link_capacity, 'link_capacity')
    # Add used bandwidth for all edges
    nx.set_edge_attributes(G, 0, 'used_bandwidth')
    # Get the layout of graph, here i use spring_layout
    pos = nx.spring_layout(G)

    return G, pos


def generate_flow_requests(G, flow_groups=1, flow_entries=5, size_lower=10, size_upper=100):
    """According the graph G, generate flow requests
    :param G: The topology graph
    :param flow_groups: The number of flow groups, default 1
    :param flow_entries: The number of flow entries in each group, default 5
    :param size_lower: The minimum size of flow, default 10MB
    :param size_upper: The maximum size of flow, default 100MB
    :return: flows
    """
    # Initialize flows
    flows = {}

    # If flow groups or flow entries are more than nodes of G, raise exception
    if flow_groups > len(G) or flow_entries > len(G):
        raise RuntimeError('flow_groups and flow_entries cannot be more than len(G)')

    # Randomly generate source nodes from G, no repeating
    src_nodes = random.sample(range(len(G)), flow_groups)

    # Traverse the source nodes in flows
    for src_node in src_nodes:
        nodes = list(range(len(G)))
        # Remove srs_node in nodes
        nodes.pop(src_node)
        # Randomly generate destination nodes from G, no repeating
        dst_nodes = {}
        # Add in flows
        for dst_node in random.sample(nodes, flow_entries):
            dst_nodes[dst_node] = {}
            # Randomly generate flow size
            dst_nodes[dst_node]['size'] = random.randint(size_lower, size_upper)
            # Set the flow path to None
            dst_nodes[dst_node]['path'] = None
        flows[src_node] = dst_nodes

    return flows


def draw_topology(G, position, title="Test"):
    """Draw topology and save as png
    :param G: The graph
    :param position: The position of graph
    :param title: The title of graph, default 'Test'
    :return:
    """
    # Set the figure size
    plt.figure(figsize=(15, 15))
    # Draw the graph according to the position with labels
    nx.draw(G, position, with_labels=True)
    # Save the picture as png
    plt.savefig("/Users/sam/Code/RoutingAlgorithm/img/%s.png" % title)
    plt.show()


def check_path_valid(G, path, flow_size):
    """Check whether the path can add into the graph
    :param G: The origin graph
    :param path: The computed path
    :param flow_size: Size of Flow
    :return: Boolean
    """
    # Traverse the edges in path
    for i in range(len(path) - 1):
        # If the residual bandwidth(link_capacity - used_bandwidth) less than flow_size
        # Then drop this flow
        if G[path[i]][path[i + 1]]['used_bandwidth'] + flow_size > G[path[i]][path[i + 1]]['link_capacity']:
            return False

    return True


def add_path_to_graph(G, path, flow_size):
    """Add the path into the graph
    :param G: The origin graph
    :param path: The computed path
    :param flow_size: Size of flow
    :return:
    """
    # Traverse the edges in path
    for i in range(len(path) - 1):
        # The link used bandwidth plus the current flow size
        G[path[i]][path[i + 1]]['used_bandwidth'] += flow_size


def output(flows):
    """Output flows
    :param flows:
    :return:
    """
    for src_node in flows:
        for dst_node in flows[src_node]:
            print(src_node, '->', dst_node, ':', flows[src_node][dst_node]['path'], ',size =',
                  flows[src_node][dst_node]['size'])


def test():
    # Test function
    g, pos = generate_topology()
    draw_topology(g, pos)
    generate_flow_requests(g)


if __name__ == '__main__':
    test()
