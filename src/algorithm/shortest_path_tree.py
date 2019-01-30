"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
@ide: PyCharm
@time: 2019-01-30 20:41:58
@blog: https://jiahaoplus.com
"""
from network.topology import *


def check_path_valid(G, path, flow_size):
    """Check whether the path can add into the graph
    :param G: The origin graph
    :param path: The computed path
    :param flow_size: Size of Flow
    :return: Boolean
    """
    # Traverse the edges in path
    for i in range(len(path) - 1):
        # If the link capacity is lower than the size of current flow
        # It means the current flow should be dropped
        if G[path[i]][path[i + 1]]['link_capacity'] < flow_size:
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
        # The link capacity of each edge minus the size of current flow
        G[path[i]][path[i + 1]]['link_capacity'] -= flow_size


def generate_shortest_path_tree(G, flows):
    """According to the flows and graph, generate Shortest Path Tree for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    for src_node in flows:  # Traverse source nodes in flows
        for dst_node in flows[src_node].keys():  # Traverse destination nodes corresponding to src_node
            # Compute the shortest path from src_node to dst_node, not considering weight
            shortest_path = nx.shortest_path(graph, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']

            if check_path_valid(graph, shortest_path, flow_size):  # Check whether the flow can add into the graph
                # Add the path into the graph
                add_path_to_graph(graph, shortest_path, flow_size)
                # Add the path into the flows
                allocated_flows[src_node][dst_node]['path'] = shortest_path

    for src_node in allocated_flows:
        for dst_node in allocated_flows[src_node]:
            print(src_node, '->', dst_node, ':', allocated_flows[src_node][dst_node]['path'], ',size =',
                  allocated_flows[src_node][dst_node]['size'])


    return allocated_flows


def test():
    graph = generate_topology()
    draw_topology(graph, "Network Topology")
    flows = generate_flow_requests(graph)
    generate_shortest_path_tree(graph, flows)


if __name__ == '__main__':
    test()
