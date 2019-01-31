"""
@project: RoutingAlgorithm
@author: sam
@file steiner_tree.py
@ide: PyCharm
@time: 2019-01-31 15:44:27
@blog: https://jiahaoplus.com
"""
from network.topology import *
from network.utils import *
import networkx.algorithms.approximation as nxaa


def generate_steiner_tree(G, flows):
    """According to the flows and graph, generate Steiner Tree for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    allocated_graph = nx.Graph()  # Steiner Trees initialization
    allocated_graph.add_nodes_from(G)  # Add nodes from G to steiner_trees

    # Traverse source nodes in flows
    for src_node in flows:
        # Generate the steiner tree(src_node, dst_nodes), not considering weight
        steiner_tree = nx.Graph(nxaa.steiner_tree(graph, list(flows[src_node].keys()) + [src_node], weight=None))

        # Traverse the destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Find the path for current flow in steiner tree
            path = nx.shortest_path(steiner_tree, src_node, dst_node, weight=None)
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, path, flow_size):
                # Add the path into the graph
                # Link capacity minus flow_size
                add_path_to_graph(graph, path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = path
                # Add the path into the allocated_graph
                nx.add_path(allocated_graph, path)

    output(allocated_flows)

    compute_network_performance(graph, allocated_flows, allocated_graph)
    return allocated_flows, allocated_graph


def test():
    g, pos = generate_topology(100)
    draw_topology(g, pos, 'Network Topology')
    flows = generate_flow_requests(g, 50, 10)
    allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
    draw_topology(allocated_graph, pos, 'Steiner Tree')


if __name__ == '__main__':
    test()
