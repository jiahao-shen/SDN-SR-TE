"""
@project: RoutingAlgorithm
@author: sam
@file utils.py
@ide: PyCharm
@time: 2019-01-30 23:24:36
@blog: https://jiahaoplus.com
"""
import matplotlib.pyplot as plt
import networkx as nx


def compute_network_performance(G, allocated_flows, allocated_graph):
    """Compute performance of the network
    Including number of branch nodes, average rejection rate, average network throughput and link utilization
    :param G:
    :param allocated_flows:
    :param allocated_graph:
    :return: num_branch_nodes, average_rejection_rate, throughput, link_utilization
    """
    return compute_num_branch_nodes(allocated_graph), compute_average_rejection_rate(
        allocated_flows), compute_throughput(allocated_flows), compute_link_utilization(G)


def compute_num_branch_nodes(allocated_graph):
    """Compute the number of branch nodes
    :param allocated_graph:
    :return:
    """
    num_branch_nodes = 0
    for node in allocated_graph.nodes:
        # If the degrees of node bigger than two, it is a branch node
        if allocated_graph.degree(node) > 2:
            num_branch_nodes += 1
    # print('Number of branch nodes:', num_branch_nodes)
    return num_branch_nodes


def compute_average_rejection_rate(allocated_flows):
    """Compute the number of average rejection rate
    :param allocated_flows:
    :return:
    """
    num_total_flows = 0
    num_allocated_flows = 0
    for src_node in allocated_flows:
        for dst_node in allocated_flows[src_node]:
            # Compute the number of total flows
            num_total_flows += 1
            # If current flow is allocated
            if allocated_flows[src_node][dst_node]['path'] is not None:
                num_allocated_flows += 1

    # Compute the average rejection rate
    average_rejection_rate = 1 - (num_allocated_flows / num_total_flows)
    # print('Average Rejection Rate:', average_rejection_rate * 100, "%")
    return average_rejection_rate


def compute_throughput(allocated_flows):
    """Compute the network throughput
    :param allocated_flows:
    :return:
    """
    throughput = 0
    for src_node in allocated_flows:
        for dst_node in allocated_flows[src_node]:
            # If current flow is allocated
            if allocated_flows[src_node][dst_node]['path'] is not None:
                # Sum the flow size
                throughput += allocated_flows[src_node][dst_node]['size']
    # print('Average Network Throughput:', throughput)
    return throughput


def compute_link_utilization(G):
    """Compute the link utilization
    :param G:
    :return:
    """
    total_bandwidth = 0
    total_residual_bandwidth = 0
    for edge in G.edges(data=True):
        total_bandwidth += edge[2]['link_capacity']
        total_residual_bandwidth += edge[2]['residual_bandwidth']

    link_utilization = 1 - total_residual_bandwidth / total_bandwidth
    # print('Link Utilization:', link_utilization * 100, "%")
    return link_utilization


def draw_topology(G, position, edge_attribute='residual_bandwidth', title="Test"):
    """Draw topology and save as png
    :param G: The graph
    :param position: The position of graph
    :param title: The title of graph, default 'Test'
    :return:
    """
    # Set the figure size
    plt.figure(figsize=(15, 15))
    plt.title(title)
    # Draw the graph according to the position with labels
    nx.draw(G, position, with_labels=True)
    nx.draw_networkx_edge_labels(G, position, edge_labels=nx.get_edge_attributes(G, edge_attribute))
    # Save the picture as png
    # plt.savefig("/Users/sam/Code/RoutingAlgorithm/img/%s.png" % title)
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
        # If the residual bandwidth less than flow_size
        # Then drop this flow
        if G[path[i]][path[i + 1]]['residual_bandwidth'] < flow_size:
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
        # The link residual bandwidth minus the current flow size
        G[path[i]][path[i + 1]]['residual_bandwidth'] -= flow_size


def output_flows(flows):
    """Output flows
    :param flows:
    :return:
    """
    for src_node in flows:
        for dst_node in flows[src_node]:
            print(src_node, '->', dst_node, ':', flows[src_node][dst_node]['path'], ',size =',
                  flows[src_node][dst_node]['size'])


def test():
    pass


if __name__ == '__main__':
    test()
