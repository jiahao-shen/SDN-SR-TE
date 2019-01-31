"""
@project: RoutingAlgorithm
@author: sam
@file utils.py
@ide: PyCharm
@time: 2019-01-30 23:24:36
@blog: https://jiahaoplus.com
"""


def compute_network_performance(G, allocated_flows, allocated_graph):
    """Compute performance of the network
    Including number of branch nodes, average rejection rate, average network throughput and link utilization
    :param G:
    :param allocated_flows:
    :param allocated_graph:
    :return: num_branch_nodes, average_rejection_rate, throughput, link_utilization
    """
    # Compute the number of branch nodes
    num_branch_nodes = 0
    for node in allocated_graph.nodes:
        # If the degrees of node bigger than two, it is a branch node
        if allocated_graph.degree(node) > 2:
            num_branch_nodes += 1
    print('Number of branch nodes:', num_branch_nodes)

    num_total_flows = 0
    num_allocated_flows = 0
    throughput = 0
    for src_node in allocated_flows:
        for dst_node in allocated_flows[src_node]:
            # Compute the number of total flows
            num_total_flows += 1
            # If current flow is allocated
            if allocated_flows[src_node][dst_node]['path'] is not None:
                num_allocated_flows += 1
                # Sum the flow size
                throughput += allocated_flows[src_node][dst_node]['size']

    # Compute the average rejection rate
    average_rejection_rate = 1 - (num_allocated_flows / num_total_flows)
    print('Average Rejection Rate:', average_rejection_rate * 100, "%")
    print('Average Network Throughput:', throughput)

    # Compute the link utilization
    total_bandwidth = 0
    used_bandwidth = 0
    for edge in G.edges(data=True):
        total_bandwidth += edge[2]['link_capacity']
        used_bandwidth += edge[2]['used_bandwidth']

    link_utilization = used_bandwidth / total_bandwidth
    print('Link Utilization:', link_utilization * 100, "%")

    return num_branch_nodes, average_rejection_rate, throughput, link_utilization


def test():
    pass


if __name__ == '__main__':
    test()
