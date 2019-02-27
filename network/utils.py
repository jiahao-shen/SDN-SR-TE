"""
@project: RoutingAlgorithm
@author: sam
@file utils.py
@ide: PyCharm
@time: 2019-01-30 23:24:36
@blog: https://jiahaoplus.com
"""
import math


def compute_network_performance(G, allocated_flows, multicast_trees):
    """Compute performance of the network
    Including number of branch nodes, average rejection rate, average network
    throughput and link utilization
    :param G:
    :param allocated_flows:
    :param multicast_trees:
    :return: num_branch_nodes, average_rejection_rate, throughput,
    link_utilization
    """
    return [compute_num_branch_nodes(
        multicast_trees), compute_average_rejection_rate(
        allocated_flows), compute_throughput(
        allocated_flows), compute_link_utilization(G)]


def compute_num_branch_nodes(multicast_trees):
    """Compute the number of branch nodes
    :param multicast_trees: The list of multicast tree
    :return: num_branch_nodes
    """
    num_branch_nodes = 0
    # Traverse all multicast trees
    for tree in multicast_trees:
        for node in tree.nodes:
            if node == tree.source and tree.degree(node) >= 2:
                num_branch_nodes += 1
            elif node != tree.source and tree.degree(node) >= 3:
                num_branch_nodes += 1
    # print('Number of branch nodes:', num_branch_nodes)
    return num_branch_nodes


def compute_average_rejection_rate(allocated_flows):
    """Compute the number of average rejection rate
    :param allocated_flows:
    :return: average_rejection_rate(%)
    """
    num_total_flows = 0
    num_allocated_flows = 0
    # Traverse all allocated flows
    for f in allocated_flows:
        for dst_node in f['dst']:
            # Compute the number of total flows
            num_total_flows += 1
            # If current flow is allocated
            if f['dst'][dst_node] is not None:
                num_allocated_flows += 1

    # Compute the average rejection rate
    average_rejection_rate = 1 - (num_allocated_flows / num_total_flows)
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
        for dst_node in f['dst']:
            # If current flow is allocated
            if f['dst'][dst_node] is not None:
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
    for edge in G.edges(data=True):
        total_bandwidth += edge[2]['link_capacity']
        total_residual_bandwidth += edge[2]['residual_bandwidth']

    # Compute the link utilization
    link_utilization = 1 - total_residual_bandwidth / total_bandwidth
    # Transform to percentage
    link_utilization *= 100
    # print('Link Utilization:', link_utilization * 100, "%")
    return link_utilization


def check_path_valid(G, multicast_tree, path, flow_size):
    """Check whether the path can add into the graph
    From two points: residual bandwidth and residual flow entries
    :param G: The origin graph
    :param multicast_tree: The current multicast tree for multicast
    :param path: The computed path
    :param flow_size: Size of Flow
    :return: Boolean
    """
    # Copy multicast tree as temp tree
    tmp_tree = multicast_tree.copy()
    # Add path to temp tree
    tmp_tree.add_path(path)
    # Traverse nodes during the path except destination node
    for i in range(len(path) - 1):
        # If the residual bandwidth less than flow_size
        # Then drop this flow
        if G[path[i]][path[i + 1]]['residual_bandwidth'] < flow_size:
            return False
        # If current node is source node in multicast tree and the residual
        # flow entries in G is less than the degree in temp tree
        # Then drop this flow
        if path[i] == multicast_tree.source and G.nodes[path[i]][
            'residual_flow_entries'] < tmp_tree.degree(path[i]):
            return False
        # If current node isn't source node in multicast tree and the residual
        # flow entries in G is less than the (degree - 1) in temp tree
        # Then drop this flow
        if path[i] != multicast_tree.source and G.nodes[path[i]][
            'residual_flow_entries'] < tmp_tree.degree(path[i]) - 1:
            return False

    return True


def update_node_entries(G, multicast_tree):
    """Update the residual node entries
    In Segment Routing in SDN, we exploit the branch forwarding technique. We
    only need store the entries in ingress and branch nodes instead of all
    nodes in multicast tree.
    :param G: The origin graph
    :param multicast_tree: The current multicast tree
    :return:
    """
    # Traverse all nodes in multicast tree
    for node in multicast_tree.nodes:
        # If current node is source node
        if node == multicast_tree.source:
            # Residual flow entries minus degree
            G.nodes[node]['residual_flow_entries'] -= multicast_tree.degree(
                node)
        # If current node is branch node
        elif node != multicast_tree.source and \
                multicast_tree.degree(node) >= 3:
            # Residual flow entries minus degree - 1
            G.nodes[node]['residual_flow_entries'] -= \
                (multicast_tree.degree(node) - 1)


def update_edge_bandwidth(G, multicast_tree, flow_size):
    """Update the residual bandwidth of edges in the tree
    :param G: The origin graph
    :param multicast_tree: The multicast tree
    :param flow_size: The size of current flow
    :return:
    """
    # The residual bandwidth of all edges in multicast tree minus flow size
    for edge in multicast_tree.edges:
        G[edge[0]][edge[1]]['residual_bandwidth'] -= flow_size


def output_flows(flows):
    """Output flows
    :param flows:
    :return:
    """
    for f in flows:
        src_node = f['src']
        for dst_node in f['dst']:
            print(src_node, '->', dst_node, ':', f['dst'][dst_node], ',',
                  'size =', f['size'])


def compute_path_minimum_bandwidth(G, path):
    """Compute the minimum bandwidth during the path
    :param G: The origin path
    :param path: The path in G
    :return: minimum_bandwidth
    """
    minimum_bandwidth = math.inf
    for i in range(len(path) - 1):
        minimum_bandwidth = min(minimum_bandwidth,
                                G[path[i]][path[i + 1]]['residual_bandwidth'])

    return minimum_bandwidth


def test_1():
    pass


if __name__ == '__main__':
    test_1()
