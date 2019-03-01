"""
@project: RoutingAlgorithm
@author: sam
@file spt.py
@ide: PyCharm
@time: 2019-03-01 14:33:05
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy

__all__ = [
    'generate_shortest_path_trees',
]


def generate_shortest_path_trees(G, flows):
    """According to flows and graph, generate Shortest Path Tree(SPT)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, shortest_path_trees
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    shortest_path_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Compute all shortest paths from current multicast source node to
        # others, not considering weight
        all_shortest_paths = nx.shortest_path(graph, f['src'], weight=None)
        # Shortest path tree for current multicast initialization
        shortest_path_tree = nx.Graph()
        # Set the source node of shortest path tree
        shortest_path_tree.source = f['src']
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Get the shortest path from source to destination
            shortest_path = all_shortest_paths[dst_node]
            # Check the current path whether valid
            if check_path_valid(graph, shortest_path_tree, shortest_path,
                                f['size']):
                # Record the shortest path for pair(source, destination)
                f['dst'][dst_node] = shortest_path
                # Add the shortest path into shortest path tree
                shortest_path_tree.add_path(shortest_path)
        # Update the residual flow entries of nodes in the shortest path tree
        update_node_entries(graph, shortest_path_tree)
        # Update the residual bandwidth of edges in the shortest path tree
        update_edge_bandwidth(graph, shortest_path_tree, f['size'])
        # Add multicast tree in forest
        shortest_path_trees.append(shortest_path_tree)

    return graph, allocated_flows, shortest_path_trees
