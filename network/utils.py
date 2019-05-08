"""
@project: RoutingAlgorithm
@author: sam
@file utils.py
@ide: PyCharm
@time: 2019-01-30 23:24:36
@blog: https://jiahaoplus.com
"""
from copy import deepcopy
from networkx.utils import pairwise
from itertools import islice
from time import time
import logging
import matplotlib.pyplot as plt
import networkx as nx
import math

__all__ = [
    'compute_path_minimum_bandwidth',
    'compute_path_cost',
    'is_branch_node',
    'is_path_valid',
    'update_topo_info',
    'draw_result',
    'draw_topology',
    'generate_k_shortest_paths',
    'count_time',
    'compute_acyclic_sub_path'
]

logging.basicConfig(level=logging.DEBUG, format='(%(levelname)s)%(message)s')


def is_branch_node(tree, node):
    """Check whether is branch node
    :param tree: The current multicast tree
    :param node: The node needs to check
    :return: Boolean
    """
    if node == tree.root:
        return tree.degree(node) >= 2
    else:
        return tree.degree(node) >= 3


def is_path_valid(G, tree, path, flow_size):
    """Check whether the path can add into the graph
    From two points: residual bandwidth and residual flow entries
    :param G: The origin graph
    :param tree: The current multicast tree
    :param path: The computed path
    :param flow_size: Size of Flow
    :return: Boolean
    """
    # Copy multicast tree as temp tree
    tmp_tree = deepcopy(tree)
    # Add path into temp tree
    nx.add_path(tmp_tree, path)
    # Traverse nodes during the path except destination node
    for v, u in pairwise(path):
        if G[v][u]['residual_bandwidth'] < flow_size:
            return False
        if v == tmp_tree.root and \
                G.nodes[v]['residual_flow_entries'] < tmp_tree.degree(v):
            return False
        elif is_branch_node(tmp_tree, v) and \
                G.nodes[v]['residual_flow_entries'] < tmp_tree.degree(v) - 1:
            return False

    return True


def update_topo_info(G, tree, flow_size):
    """Update the information of nodes and links in topology
    :param G: The origin graph
    :param tree: The constructed multicast tree
    :param flow_size: The size of current flow
    :return:
    """
    # Traverse all nodes in multicast tree
    for v in tree.nodes:
        # Only root and branch nodes maintenance the flow entries
        if v == tree.root:
            G.nodes[v]['residual_flow_entries'] -= tree.degree(v)
        elif is_branch_node(tree, v):
            G.nodes[v]['residual_flow_entries'] -= (tree.degree(v) - 1)

    # The residual bandwidth of all edges in multicast tree minus flow size
    for e in tree.edges:
        G[e[0]][e[1]]['residual_bandwidth'] -= flow_size


def compute_path_minimum_bandwidth(G, path):
    """Compute the minimum bandwidth during the path
    :param G: The origin path
    :param path: The path in G
    :return: minimum_bandwidth
    """
    minimum_bandwidth = math.inf
    for v, u in pairwise(path):
        minimum_bandwidth = min(minimum_bandwidth,
                                G[v][u]['residual_bandwidth'])

    return minimum_bandwidth


def compute_path_cost(G, path, weight=None):
    """Compute the cost of path according to the parameter weight
    :param G: The origin graph
    :param path: The path need to compute
    :param weight: The edge value
    :return: cost
    """
    # Initialize cost
    cost = 0
    # If weight is None
    if weight is None:
        cost = len(path) - 1
    else:
        # Traverse nodes during the path
        for v, u in pairwise(path):
            # Sum all weight of edges during the path
            cost += G[v][u][weight]

    return cost


def generate_k_shortest_paths(G, source, destination, k=2, weight=None):
    """Generate the k shortest paths from source to destination in G
    :param G: The origin graph
    :param source: The source node
    :param destination: The destination node
    :param k: The parameter in k shortest path, default 2
    :param weight: The weight value in shortest path algorithm, default None
    :return: The list of k shortest paths
    """
    return list(
        islice(nx.shortest_simple_paths(G, source, destination, weight), k))


def draw_topology(G, position,
                  node_attribute=None, edge_attribute=None,
                  title="Test"):
    """Draw topology
    :param G: The topology graph
    :param position: The position of graph
    :param node_attribute: The node label, default None
    :param edge_attribute: The edge label, default None
    :param title: The title of graph, default 'Test'
    :return:
    """
    # Set the figure size
    plt.figure(figsize=(15, 15))
    plt.title(title)
    # Draw the graph according to the position with labels
    nx.draw(G, position, with_labels=True)
    # Show the node labels
    nx.draw_networkx_labels(G, position,
                            labels=nx.get_node_attributes(G, node_attribute))
    # Show the edge labels
    nx.draw_networkx_edge_labels(G, position, label_pos=0.2,
                                 edge_labels=nx.get_edge_attributes(
                                     G, edge_attribute))
    # Figure show
    plt.show()


def draw_result(result, x_label, y_label, type='line'):
    """Draw results for main.py
    :param result: The final result as dict
    :param x_label: The x label of figure
    :param y_label: The y label of figure
    :param type: The figure type, including line and bar, default line
    :return:
    """
    # The default point marker and color
    POINT_MARKER = {'SPT': 'o', 'ST': 'v',
                    'WSPT': 's', 'WST': '*',
                    'BST': 'p', 'BBSRT': 'x',
                    'BBST': 'D'}
    POINT_COLOR = {'SPT': '#c3637f', 'ST': '#eb8773',
                   'WSPT': '#f4b861', 'WST': '#d9ea70',
                   'BST': '#81d2b4', 'BBSRT': '#5bc0d5',
                   'BBST': '#70acf6'}
    # The figure size
    plt.figure(figsize=(9, 6))
    # Check the figure type
    if type == 'line':
        # Draw the line figure
        for key in result:
            plt.plot(*zip(*sorted(result[key].items())), label=key,
                     color=POINT_COLOR[key], marker=POINT_MARKER[key])

    elif type == 'bar':
        # Draw the bar figure
        # Get the x values
        x_value = list(result['SPT'].keys())
        # Compute the appropriate width
        width = (x_value[1] - x_value[0]) / 8
        # Compute the offset
        offset = [i - (len(result) - 1) / 2 for i in range(len(result))]
        index = 0
        for key in result:
            # Compute the x value of each result
            x = list(result[key].keys())
            for i in range(len(x)):
                # The origin value plus the offset value
                x[i] += offset[index] * width
            plt.bar(x, list(result[key].values()), width=width,
                    label=key, color=POINT_COLOR[key])
            index += 1

    # Set the y line
    plt.grid(axis='y')
    # Set the legend
    plt.legend(bbox_to_anchor=(1.05, 0.4), loc=3, borderaxespad=0)
    # Set x and y labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Show the figure
    plt.show()


def count_time(func):
    """Count the run time of function
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        over_time = time()
        total_time = over_time - start_time
        logging.info('Func: %s, Run Time: %.6f' % (func.__name__, total_time))
        return res

    return wrapper


def compute_acyclic_sub_path(tree, path):
    """Compute the sub path without loop edges in tree
    :param tree: The multicast tree
    :param path: The current path
    :return: Path with no cycle edges
    """
    for u, v in pairwise(reversed(path)):
        if v in tree.nodes and u not in tree.nodes:
            return path[path.index(v):]
