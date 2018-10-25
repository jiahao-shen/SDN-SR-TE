import networkx as nx
import networkx.algorithms.approximation
import matplotlib.pyplot as plt
import random
import math

NETWORK_SIZE = 21  # 网络节点个数
PROBABILITY = 0.2  # 概率P
DESTINATION_NUMBER = 8  # 目标节点个数
NODE_COLOR = '#5BE7C4'  # 普通节点颜色
SOURCE_NODE_COLOR = '#FF2E63'  # 源节点颜色
DESTINATION_NODE_COLOR = '#FFE869'  # 目标节点颜色
FIGURE_SIZE = 15  # 画布大小


def generate_network_topology():
    """Generate Network Topology by random
    :return:
    """
    while True:
        G = nx.erdos_renyi_graph(NETWORK_SIZE, PROBABILITY)  # 随机生成拓扑
        if nx.is_connected(G):  # 如果图是连通的则生成完毕
            break

    for edge in G.edges:
        G.add_weighted_edges_from([(edge[0], edge[1], random.randint(1, 10))])  # 给边添加随机权值

    g_edge_labels = nx.get_edge_attributes(G, 'weight')  # 获取边labels

    destination_nodes = random.sample(list(G.nodes)[1:], DESTINATION_NUMBER)  # 随机生成目标节点
    destination_nodes.sort()  # 目标节点排序
    pos = nx.circular_layout(G, FIGURE_SIZE // 2)  # 生成节点在画布中的分布
    print('Destination Nodes:', destination_nodes)  # 打印目标节点

    draw_graphics(G, pos, destination_nodes, g_edge_labels, 'Network Topology')  # 画对应的图

    return G, pos, destination_nodes


def generate_shortest_path_tree(G, pos, destination_nodes):
    """Return Shortest Path Tree
    :param G:
    :param pos:
    :param destination_nodes:
    :return:
    """
    shortest_path_tree = nx.Graph()
    shortest_path_tree.add_nodes_from(G)  # 从G中添加节点

    print('Shortest Path Tree:')
    for node in destination_nodes:
        shortest_path = nx.shortest_path(G, 0, node, weight=None)
        print(shortest_path)
        nx.add_path(shortest_path_tree, shortest_path)  # 添加从源到i的最短路径

    for edge in shortest_path_tree.edges:
        node_1, node_2 = edge[0], edge[1]
        shortest_path_tree.add_weighted_edges_from([(node_1, node_2, G[node_1][node_2]['weight'])])  # 往图中添加权值

    shortest_path_tree_edge_labels = nx.get_edge_attributes(shortest_path_tree, 'weight')

    draw_graphics(shortest_path_tree, pos, destination_nodes, shortest_path_tree_edge_labels, 'Shortest Path Tree')

    return shortest_path_tree


def generate_steiner_tree(G, pos, destination_nodes):
    """Generate Steiner Tree
    :param G:
    :param pos:
    :param destination_nodes:
    :return:
    """
    steiner_tree = nx.Graph()
    steiner_tree.add_nodes_from(G)
    print('Steiner Tree:')

    # 遍历斯坦纳树
    for edge in nx.Graph(nx.algorithms.approximation.steiner_tree(G, destination_nodes + [0], weight=None)).edges:
        node_1, node_2 = edge[0], edge[1]
        steiner_tree.add_weighted_edges_from([(node_1, node_2, G[node_1][node_2]['weight'])])  # 添加权值
        print(edge)

    steiner_tree_edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')

    draw_graphics(steiner_tree, pos, destination_nodes, steiner_tree_edge_labels, 'Steiner Tree')

    return steiner_tree


def generate_widest_shortest_path_tree(G, pos, destination_nodes):
    widest_shortest_path_tree = nx.Graph()
    widest_shortest_path_tree.add_nodes_from(G)

    print('Widest Shortest Path Tree:')
    for node in destination_nodes:
        shortest_paths = nx.all_shortest_paths(G, 0, node, weight=None)  # 找到从0到目标节点的所有最短路
        widest_shortest_path = None  # 初始最宽最短路
        max_minimum_weight = -math.inf  # 初始最大最小权值
        for shortest_path in shortest_paths:  # 遍历所有最短路
            minimum_weight = math.inf  # 最小权值=正无穷
            # print(shortest_path)
            for i in range(len(shortest_path) - 1):  # 遍历该最短路径
                node_1 = shortest_path[i]
                node_2 = shortest_path[i + 1]
                minimum_weight = min(minimum_weight, G[node_1][node_2]['weight'])  # 找到该路径的最小权值
            if minimum_weight > max_minimum_weight:  # 如果该路径的最小权值大于当前的最大最小权值
                max_minimum_weight = minimum_weight  # 更新最大最小权值
                widest_shortest_path = shortest_path  # 更新最宽最短路
        print(widest_shortest_path, max_minimum_weight)
        nx.add_path(widest_shortest_path_tree, widest_shortest_path)

    for edge in widest_shortest_path_tree.edges:
        node_1, node_2 = edge[0], edge[1]
        widest_shortest_path_tree.add_weighted_edges_from([(node_1, node_2, G[node_1][node_2]['weight'])])

    widest_shortest_path_tree_labels = nx.get_edge_attributes(widest_shortest_path_tree, 'weight')

    draw_graphics(widest_shortest_path_tree, pos, destination_nodes, widest_shortest_path_tree_labels, 'Widest '
                                                                                                       'Shortest Path '
                                                                                                       'Tree')


def draw_graphics(graph, pos, destination_nodes, graph_edge_labels, title):
    """Draw Graphics
    :param graph:
    :param pos:
    :param destination_nodes:
    :param graph_edge_labels:
    :param title:
    :return:
    """
    plt.figure(figsize=(FIGURE_SIZE, FIGURE_SIZE))  # 画布大小
    plt.title(title)  # 标题
    nx.draw_networkx(graph, pos, node_color=NODE_COLOR, node_size=600)  # 画对应的路径图
    nx.draw_networkx_nodes(graph, pos, [0], node_color=SOURCE_NODE_COLOR, node_size=600)  # 画源节点
    nx.draw_networkx_nodes(graph, pos, destination_nodes, node_color=DESTINATION_NODE_COLOR, node_size=600)  # 画目标节点
    if graph_edge_labels is not None:
        nx.draw_networkx_edge_labels(graph, pos, graph_edge_labels)  # 给边标注权值
    plt.axis('off')  # 座标轴关闭
    plt.savefig("%s.png" % title)  # 保存图片
    plt.show()
