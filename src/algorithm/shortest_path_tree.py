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


def generate_shortest_path_tree(G, flows):
    """According to the flows and graph, generate Shortest Path Tree for multicast
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
            shortest_path = nx.shortest_path(graph, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, shortest_path, flow_size):
                # Add the path into the graph
                # Link capacity minus flow_size
                add_path_to_graph(graph, shortest_path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = shortest_path
                # Add the path into the allocated_graph
                nx.add_path(allocated_graph, shortest_path)

    output(allocated_flows)

    compute_network_performance(graph, allocated_flows, allocated_graph)
    return allocated_flows, allocated_graph


def test():
    g, pos = generate_topology()
    draw_topology(g, pos, 'Network Topology')
    flows = generate_flow_requests(g, 18, 18)
    allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
    draw_topology(allocated_graph, pos, 'Shortest Path Tree')


if __name__ == '__main__':
    test()
