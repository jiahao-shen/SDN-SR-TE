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
import matplotlib.pyplot as plt
import networkx as nx
import random
import math


def network_performance(G, allocated_flows, multicast_trees):
    """Compute performance of the network
    Including number of branch nodes, average rejection rate, average network
    throughput and link utilization
    :param G:
    :param allocated_flows:
    :param multicast_trees:
    :return: num_branch_nodes, average_rejection_rate,
             throughput,link_utilization
    """
    return [compute_num_branch_nodes(multicast_trees),
            compute_average_rejection_rate(allocated_flows),
            compute_throughput(allocated_flows),
            compute_link_utilization(G)]


def compute_num_branch_nodes(multicast_trees):
    """Compute the number of branch nodes
    :param multicast_trees: The list of multicast tree
    :return: num_branch_nodes
    """
    num_branch_nodes = 0
    # Traverse all multicast trees
    for T in multicast_trees:
        for v in T.nodes:
            if is_branch_node(T, v):
                num_branch_nodes += 1
    # print('Number of branch nodes:', num_branch_nodes)
    return num_branch_nodes


def is_branch_node(multicast_tree, node):
    """According to the tree, check whether is branch node
    :param multicast_tree: The current multicast tree
    :param node: The node needs to check
    :return: Boolean
    """
    # The degree of branch node is bigger than 3
    if multicast_tree.degree(node) >= 3:
        return True
    # Else isn't branch node
    return False


def compute_average_rejection_rate(allocated_flows):
    """Compute the number of average rejection rate
    :param allocated_flows:
    :return: average_rejection_rate(%)
    """
    num_total_flows = 0
    num_unallocated_flows = 0
    # Traverse all allocated flows
    for f in allocated_flows:
        for dst in f['dst']:
            # Compute the number of total flows
            num_total_flows += 1
            # If current flow is allocated
            if f['dst'][dst] is None:
                num_unallocated_flows += 1

    # Compute the average rejection rate
    average_rejection_rate = num_unallocated_flows / num_total_flows
    # Transform to percentage
    average_rejection_rate *= 100
    # print('Average Rejection Rate:', average_rejection_rate * 100, "%")
    return average_rejection_rate


def compute_throughput(allocated_flows):
    """Compute the network throughput
    :param allocated_flows:
    :return: throughput(MB)
    """
    throughput = 0
    # Traverse all allocated flows
    for f in allocated_flows:
        for dst in f['dst']:
            # If current flow is allocated
            if f['dst'][dst] is not None:
                # Sum the flow size
                throughput += f['size']
    # print('Average Network Throughput:', throughput)
    return throughput


def compute_link_utilization(G):
    """Compute the link utilization
    :param G:
    :return: link_utilization
    """
    total_bandwidth = 0
    total_residual_bandwidth = 0
    # Traverse all edges in G
    for e in G.edges(data=True):
        total_bandwidth += e[2]['link_capacity']
        total_residual_bandwidth += e[2]['residual_bandwidth']

    # Compute the link utilization
    link_utilization = 1 - total_residual_bandwidth / total_bandwidth
    # Transform to percentage
    link_utilization *= 100
    # print('Link Utilization:', link_utilization * 100, "%")
    return link_utilization


def is_path_valid(G, multicast_tree, path, flow_size):
    """Check whether the path can add into the graph
    From two points: residual bandwidth and residual flow entries
    :param G: The origin graph
    :param multicast_tree: The current multicast tree for multicast
    :param path: The computed path
    :param flow_size: Size of Flow
    :return: Boolean
    """
    # Copy multicast tree as temp tree
    tmp_tree = deepcopy(multicast_tree)
    # Add path to temp tree
    tmp_tree.add_path(path)
    # Traverse nodes during the path except destination node
    for v, u in pairwise(path):
        # If the residual bandwidth less than flow_size
        # Then drop this flow
        if G[v][u]['residual_bandwidth'] < flow_size:
            return False
        # If current node is root in multicast tree and the residual
        # flow entries in G is less than the degree in temp tree
        # Then drop this flow
        if v == multicast_tree.root and \
                G.nodes[v]['residual_flow_entries'] < tmp_tree.degree(v):
            return False
        # If current node is branch node in multicast tree and the residual
        # flow entries in G is less than the (degree - 1) in temp tree
        # Then drop this flow
        elif v != multicast_tree.root and is_branch_node(tmp_tree, v) and \
                G.nodes[v]['residual_flow_entries'] < tmp_tree.degree(v) - 1:
            return False

    return True


def update_node_entries(G, multicast_tree):
    """Update the residual node entries
    With Segment Routing in SDN, we exploit the branch forwarding technique. We
    only need store the entries in ingress and branch nodes instead of all
    nodes in multicast tree.
    :param G: The origin graph
    :param multicast_tree: The current multicast tree
    :return:
    """
    # Traverse all nodes in multicast tree
    for v in multicast_tree.nodes:
        # If current node is root
        if v == multicast_tree.root:
            # Residual flow entries minus degree
            G.nodes[v]['residual_flow_entries'] -= multicast_tree.degree(v)
        # If current node is branch node
        elif v != multicast_tree.root and is_branch_node(multicast_tree, v):
            # Residual flow entries minus degree - 1
            G.nodes[v]['residual_flow_entries'] -= \
                (multicast_tree.degree(v) - 1)


def update_edge_bandwidth(G, multicast_tree, flow_size):
    """Update the residual bandwidth of edges in the tree
    :param G: The origin graph
    :param multicast_tree: The multicast tree
    :param flow_size: The size of current flow
    :return:
    """
    # The residual bandwidth of all edges in multicast tree minus flow size
    for e in multicast_tree.edges:
        G[e[0]][e[1]]['residual_bandwidth'] -= flow_size


def output_flows(flows):
    """Output flows
    :param flows:
    :return:
    """
    for f in flows:
        for dst in f['dst']:
            print(f['src'], '->', dst, ':', f['dst'][dst],
                  ',', 'size =', f['size'])


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


def draw_topology(G, position, node_attribute=None, edge_attribute=None,
                  title="Test"):
    """Draw topology and save as png
    :param G: The graph
    :param position: The position of graph
    :param node_attribute: The node attribute correspond the node label,
     default None
    :param edge_attribute: The edge attribute correspond the edge label,
    default None
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
    nx.draw_networkx_edge_labels(G, position,
                                 edge_labels=nx.get_edge_attributes(
                                     G, edge_attribute))
    # Figure show
    plt.show()


def draw_result(result, x_label='Multigroup Size',
                y_label='Number of Branch Node', type='line'):
    """Draw results for main.py
    :param result: The final result as dict
    :param x_label: The x label of figure
    :param y_label: The y label of figure
    :param type: The figure type, including line and bar, default line
    :return:
    """
    # The default point marker and color
    POINT_MARKER = {'SPT': 'o', 'ST': 'v', 'WSPT': 's', 'WST': '*',
                    'BBSRT': 'D'}
    POINT_COLOR = {'SPT': 'r', 'ST': 'm', 'WSPT': 'y', 'WST': 'g',
                   'BBSRT': 'b'}

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
        width = (x_value[1] - x_value[0]) / 6
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


def generate_test_result():
    result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}}

    for key in result:
        for index in range(10, 70, 10):
            result[key][index] = random.randint(10, 100)

    return result


def test_1():
    results = generate_test_result()
    draw_result(results, type='bar')


if __name__ == '__main__':
    test_1()
