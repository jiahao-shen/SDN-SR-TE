"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
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
        all_paths = nx.shortest_path(graph, f['src'], weight=None)
        # Shortest path tree for current multicast initialization
        T = nx.Graph()
        # Set the root of shortest path tree
        T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the shortest path from source to destination
            path = all_paths[dst]
            # Check the current path whether valid
            if is_path_valid(graph, T, path, f['size']):
                # Record the shortest path for pair(source, destination)
                f['dst'][dst] = path
                # Add the shortest path into shortest path tree
                T.add_path(path)
        # Update the residual flow entries of nodes in the shortest path tree
        update_node_entries(graph, T)
        # Update the residual bandwidth of edges in the shortest path tree
        update_edge_bandwidth(graph, T, f['size'])
        # Add multicast tree in forest
        shortest_path_trees.append(T)

    return graph, allocated_flows, shortest_path_trees


def test_1():
    G, pos = generate_topology(100)
    flows = generate_flow_requests(G, 2, 20)

    draw_topology(G, pos)

    graph, allocated_flows, shortest_path_trees = \
        generate_shortest_path_trees(G, flows)

    output_flows(allocated_flows)

    for T in shortest_path_trees:
        position = graphviz_layout(T, prog='dot')
        draw_topology(T, position, title='SPT')

    print(compute_num_branch_nodes(shortest_path_trees))


if __name__ == '__main__':
    test_1()
