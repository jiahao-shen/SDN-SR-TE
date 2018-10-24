import networkx as nx
import networkx.algorithms.approximation
import matplotlib.pyplot as plt
import random

NETWORK_SIZE = 21  # 网络节点个数
PROBABILITY = 0.2  # 概率P
DESTINATION_NUMBER = 8  # 目标节点个数
NODE_COLOR = '#5BE7C4'
SOURCE_NODE_COLOR = '#FF2E63'
DESTINATION_NODE_COLOR = '#FFE869'
FIGURE_SIZE = 15


def generate_network_topology():
    """Generate Network Topology by random
    :return:
    """
    while True:
        G = nx.erdos_renyi_graph(NETWORK_SIZE, PROBABILITY)
        if nx.is_connected(G):
            break

    for edge in G.edges:
        G.add_weighted_edges_from([(edge[0], edge[1], random.randint(1, 10))])

    g_edge_labels = nx.get_edge_attributes(G, 'weight')
    g_nodes = list(G.nodes)

    destination_nodes = random.sample(g_nodes[1:], DESTINATION_NUMBER)
    destination_nodes.sort()
    pos = nx.circular_layout(G, FIGURE_SIZE // 2)
    print('Destination Nodes:', destination_nodes)

    draw_graphics(G, pos, destination_nodes, g_edge_labels, 'Network Topology')

    return G, pos, destination_nodes, g_edge_labels


def generate_shortest_path_tree(G, pos, destination_nodes, g_edge_labels):
    """Return Shortest Path Tree
    :param G:
    :param pos:
    :param destination_nodes:
    :param g_edge_labels:
    :return:
    """
    shortest_path_tree = nx.Graph()
    shortest_path_tree.add_nodes_from(G)

    print('Shortest Path Tree:')
    for node in destination_nodes:
        print(nx.shortest_path(G, 0, node))
        nx.add_path(shortest_path_tree, nx.shortest_path(G, 0, node, weight=None))

    for edge in shortest_path_tree.edges:
        shortest_path_tree.add_weighted_edges_from([(edge[0], edge[1], g_edge_labels[(edge[0], edge[1])])])

    shortest_path_tree_edge_labels = nx.get_edge_attributes(shortest_path_tree, 'weight')

    draw_graphics(shortest_path_tree, pos, destination_nodes, shortest_path_tree_edge_labels, 'Shortest Path Tree')

    return shortest_path_tree


def generate_steiner_tree(G, pos, destination_nodes, g_edge_labels):
    """Generate Steiner Tree
    :param G:
    :param pos:
    :param destination_nodes:
    :param g_edge_labels:
    :return:
    """
    steiner_tree = nx.Graph()
    steiner_tree.add_nodes_from(G)
    print('Steiner Tree:')
    for edge in nx.Graph(nx.algorithms.approximation.steiner_tree(G, destination_nodes + [0], weight=None)).edges:
        steiner_tree.add_weighted_edges_from([(edge[0], edge[1], g_edge_labels[(edge[0], edge[1])])])
        print(edge)

    steiner_tree_edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')

    draw_graphics(steiner_tree, pos, destination_nodes, steiner_tree_edge_labels, 'Steiner Tree')

    return steiner_tree


def generate_widest_shortest_path(G, pos, destination_nodes, g_edge_labels):
    maximum_spanning_tree = nx.Graph(nx.maximum_spanning_tree(G, weight='weight'))
    for edge in maximum_spanning_tree.edges:
        maximum_spanning_tree.add_weighted_edges_from([(edge[0], edge[1], g_edge_labels[(edge[0], edge[1])])])

    maximum_spanning_tree_edge_labels = nx.get_edge_attributes(maximum_spanning_tree, 'weight')

    draw_graphics(maximum_spanning_tree, pos, destination_nodes, maximum_spanning_tree_edge_labels, 'Widest Shortest Path')


def draw_graphics(graph, pos, destination_nodes, graph_edge_labels, title):
    """Draw Graphics
    :param graph:
    :param pos:
    :param destination_nodes:
    :param graph_edge_labels:
    :param title:
    :return:
    """
    plt.figure(figsize=(FIGURE_SIZE, FIGURE_SIZE))
    plt.title(title)
    nx.draw_networkx(graph, pos, node_color=NODE_COLOR)
    nx.draw_networkx_nodes(graph, pos, [0], node_color=SOURCE_NODE_COLOR)
    nx.draw_networkx_nodes(graph, pos, destination_nodes, node_color=DESTINATION_NODE_COLOR)
    if graph_edge_labels is not None:
        nx.draw_networkx_edge_labels(graph, pos, graph_edge_labels)
    plt.axis('off')
    plt.savefig("%s.png" % title)
    plt.show()
