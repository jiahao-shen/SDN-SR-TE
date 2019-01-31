"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
@ide: PyCharm
@time: 2019-01-30 20:41:58
@blog: https://jiahaoplus.com
"""
from network.topology import *
from network.utils import *
import math

__all__ = [
    'generate_shortest_path_tree',
    'generate_widest_shortest_path_tree'
]


def generate_shortest_path_tree(G, flows):
    """According to the flows and graph, generate Shortest Path Tree(SPT) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    allocated_graph = nx.Graph()  # Allocated Graph(Only including path, without link capacity)
    allocated_graph.add_nodes_from(G)  # Add nodes from G to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Compute the shortest path from src_node to dst_node, not considering weight
            path = nx.shortest_path(graph, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = path
                # Add the path into the allocated_graph
                nx.add_path(allocated_graph, path)

    output(allocated_flows)

    compute_network_performance(graph, allocated_flows, allocated_graph)
    return allocated_flows, allocated_graph


def generate_widest_shortest_path_tree(G, flows):
    """According to the flows and graph, generate Widest Shortest Path Tree(WSPT) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    allocated_graph = nx.Graph()  # Widest Shortest Path Tree initialization
    allocated_graph.add_nodes_from(G)  # Add nodes from G to to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Get the widest shortest path in all shortest paths from src_node to dst_node, not considering weight
            path = generate_widest_shortest_path(nx.all_shortest_paths(graph, src_node, dst_node, weight=None), graph)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = path
                # Add the path into the allocated_graph
                nx.add_path(allocated_graph, path)

        # output(allocated_flows)

    compute_network_performance(graph, allocated_flows, allocated_graph)
    return allocated_flows, allocated_graph


def generate_widest_shortest_path(all_shortest_paths, graph):
    """Compute the widest path in all shortest paths
    :param all_shortest_paths: All shortest paths
    :param graph: The origin graph
    :return: widest_shortest_path
    """
    # Initialization
    widest_shortest_path = None
    # Initialization
    max_minimum_residual_bandwidth = -math.inf

    # Traverse all shortest paths
    for path in all_shortest_paths:
        minimum_residual_bandwidth = math.inf
        # Traverse current path edges
        for i in range(len(path) - 1):
            # Get the residual bandwidth for current edge
            residual_bandwidth = graph[path[i]][path[i + 1]]['link_capacity'] - graph[path[i]][path[i + 1]][
                'used_bandwidth']
            # Get the minimum residual bandwidth
            minimum_residual_bandwidth = min(minimum_residual_bandwidth, residual_bandwidth)

        # If find the wider minimum residual bandwidth
        if minimum_residual_bandwidth > max_minimum_residual_bandwidth:
            max_minimum_residual_bandwidth = minimum_residual_bandwidth
            widest_shortest_path = path

    return widest_shortest_path


def test():
    g, pos = generate_topology()
    draw_topology(g, pos, 'Network Topology')
    flows = generate_flow_requests(g, 19, 19)
    allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
    draw_topology(allocated_graph, pos, 'Shortest Path Tree')


if __name__ == '__main__':
    test()
