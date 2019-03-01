"""
@project: RoutingAlgorithm
@author: sam
@file wspt.py
@ide: PyCharm
@time: 2019-03-01 14:34:41
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm import *
from copy import deepcopy
import multiprocessing as mp
import math

__all__ = [
    'generate_widest_shortest_path_trees',
    'generate_widest_shortest_path'
]


def generate_widest_shortest_path_trees(G, flows):
    """According to flows and graph, generate Widest Shortest Path Tree(WSPT)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = deepcopy(G)  # Copy G
    allocated_flows = deepcopy(flows)  # Copy flows

    widest_shortest_path_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Compute all widest shortest paths from current multicast
        # source node to others
        # Considering residual bandwidth of edge as width
        all_widest_shortest_paths = generate_widest_shortest_path(graph,
                                                                  f['src'])
        # Widest Shortest Path Tree for current multicast initialization
        widest_shortest_path_tree = nx.Graph()
        # Set the root of widest shortest path tree
        widest_shortest_path_tree.root = f['src']
        # Traverse all destination nodes
        for dst_node in f['dst']:
            # Get the widest shortest path from source to destination
            widest_shortest_path = all_widest_shortest_paths[dst_node]
            # Check the current path whether valid
            if check_path_valid(graph, widest_shortest_path_tree,
                                widest_shortest_path, f['size']):
                # Record the widest shortest path for pair(source, destination)
                f['dst'][dst_node] = widest_shortest_path
                # Add the widest shortest path into widest shortest path tree
                widest_shortest_path_tree.add_path(widest_shortest_path)
        # Update the residual entries of nodes in graph
        update_node_entries(graph, widest_shortest_path_tree)
        # Update the residual bandwidth of edges in the widest
        # shortest path tree
        update_edge_bandwidth(graph, widest_shortest_path_tree, f['size'])
        # Add multicast tree in forest
        widest_shortest_path_trees.append(widest_shortest_path_tree)

    return graph, allocated_flows, widest_shortest_path_trees


def generate_widest_shortest_path(G, source,
                                  widest_attribute='residual_bandwidth'):
    """Compute all widest shortest path from source to other nodes in G
    Using Extension Dijkstra Algorithm
    :param G: The origin graph
    :param source: The source node
    :param widest_attribute: The attribute for widest path
    :return: paths
    """
    # Dict to store the paths
    paths = {source: [source]}
    # The next traverse
    next_level = {source: 1}
    # Dict to store the minimum bandwidth from source to current node
    minimum_bandwidth = {}
    # Initialize minimum bandwidth for all nodes
    for node in G.nodes:
        minimum_bandwidth[node] = math.inf
    # While not empty
    while next_level:
        this_level = next_level
        next_level = {}
        # Traverse current level
        for v in this_level:
            # Traverse all neighbor nodes of v
            for w in G.neighbors(v):
                # if w hasn't been visited
                if w not in paths:
                    # Record the path for w
                    paths[w] = paths[v] + [w]
                    # Record the minimum bandwidth of w
                    minimum_bandwidth[w] = min(minimum_bandwidth[v],
                                               G[v][w][widest_attribute])
                    # Put w into the next traverse
                    next_level[w] = 1
                # If w has been visited, and the current path length equals
                # the shortest path length and the current minimum bandwidth
                # less than the shortest path
                elif w in paths and len(paths[w]) == len(paths[v]) + 1 and \
                        min(minimum_bandwidth[v], G[v][w][widest_attribute]) \
                        > minimum_bandwidth[w]:
                    # Update the shortest path
                    paths[w] = paths[v] + [w]
                    # Update the minimum bandwidth
                    minimum_bandwidth[w] = min(minimum_bandwidth[v],
                                               G[v][w][widest_attribute])

    return paths


def test_1():
    """Test Widest Shortest Path algorithm
    Start 4 processes, each process runs 1 << 12 times, each time randomly
    generates a network topology, then randomly generates one pair
    (source, destination), then compute the widest shortest path and all
    shortest paths from source to destination.
    Then, compare the minimum bandwidth of each path. If the minimum bandwidth
    of other paths is bigger than the widest shortest path, then raise error.
    :return:
    """

    def task():
        for _ in range(1 << 10):
            G, pos = generate_topology()
            src, dst = random.sample(range(20), 2)

            all_widest_shortest_path = generate_widest_shortest_path(G, src)
            widest_shortest_path = all_widest_shortest_path[dst]
            all_shortest_path = nx.all_shortest_paths(G, src, dst, weight=None)

            for path in all_shortest_path:
                if compute_path_minimum_bandwidth(G, widest_shortest_path) < \
                        compute_path_minimum_bandwidth(G, path):
                    raise RuntimeError('Widest Shortest Path Error')

        print('Success')

    p = []

    for _ in range(4):
        p.append(mp.Process(target=task))

    for item in p:
        item.start()

    for item in p:
        item.join()


def test_2():
    """Test the Shortest Path Tree and Widest Shortest Path Tree
    :return:
    """
    G, pos = generate_topology()
    flows = generate_flow_requests(G, flow_groups=3)

    # SPT
    graph, allocated_flows, multicast_trees = \
        generate_shortest_path_trees(G, flows)

    draw_topology(graph, pos, title='Allocated Graph')
    output_flows(allocated_flows)

    for tree in multicast_trees:
        draw_topology(tree, pos, title='Tree')

    # WSPT
    graph, allocated_flows, multicast_trees = \
        generate_widest_shortest_path_trees(G, flows)

    draw_topology(graph, pos, title='Allocated Graph')
    output_flows(allocated_flows)

    for tree in multicast_trees:
        draw_topology(tree, pos, title='Tree')


def test_3():
    G, pos = generate_topology(a=0.4, b=0.4)
    flows = generate_flow_requests(G)

    output_flows(flows)

    draw_topology(G, pos, title='Topology')
    graph, allocated_flows, trees = generate_shortest_path_trees(G, flows)

    for t in trees:
        draw_topology(t, pos, title='Trees')

    print(compute_num_branch_nodes(trees))


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
