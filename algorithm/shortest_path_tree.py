"""
@project: RoutingAlgorithm
@author: sam
@file shortest_path_tree.py
@ide: PyCharm
@time: 2019-01-30 20:41:58
@blog: https://jiahaoplus.com
"""
from network.topology import *
from queue import Queue
import multiprocessing as mp
import math

__all__ = [
    'generate_shortest_path_trees',
    'generate_widest_shortest_path_trees',
    'generate_widest_shortest_path'
]


def generate_shortest_path_trees(G, flows):
    """According to flows and graph, generate Shortest Path Tree(SPT)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, shortest_path_trees
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    shortest_path_trees = []  # Initialize

    # Traverse the flows
    for f in allocated_flows:
        # Compute all shortest paths from current multicast source node to
        # others, not considering weight
        all_shortest_paths = nx.shortest_path(graph, f['src'], weight=None)
        # Shortest path tree for current multicast initialization
        shortest_path_tree = nx.Graph()
        # Add nodes from graph with source=False
        shortest_path_tree.add_nodes_from(graph, source=False)
        # Set the 'source' attribute of source node to True
        shortest_path_tree.nodes[f['src']]['source'] = True
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


def generate_widest_shortest_path_trees(G, flows):
    """According to flows and graph, generate Widest Shortest Path Tree(WSPT)
    :param G: The origin graph
    :param flows: The flow request
    :return: graph, allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

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
        # Add nodes from graph with source=False
        widest_shortest_path_tree.add_nodes_from(graph, source=False)
        # Set the 'source' attribute of source node to True
        widest_shortest_path_tree.nodes[f['src']]['source'] = True
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


def generate_widest_shortest_path(G, source):
    """Compute all widest shortest path from source to other nodes in G
    Using Extension Dijkstra Algorithm
    :param G: The origin graph
    :param source: The source node
    :return: all_widest_shortest_path
    """
    # The array to store whether the node has been visited
    visited = {}
    # The array to store the distance from source to the other nodes
    distance = {}
    # The array to store the minimum bandwidth during path from source to
    # the other nodes
    minimum_bandwidth = {}
    # The array to store the father node in path for all nodes
    father_node = {}

    for node in G.nodes:
        visited[node] = False
        distance[node] = math.inf
        minimum_bandwidth[node] = math.inf
        father_node[node] = None

    # The source node initialize
    visited[source] = True
    distance[source] = 0

    # The open_list initialize
    open_list = Queue()
    open_list.put(source)

    while not open_list.empty():
        # Get the top node of open_list
        node = open_list.get()
        # Traverse all the neighbor nodes for node
        for item in G.neighbors(node):  # For current node item
            # If the item hasn't been visited
            if not visited[item]:
                # Compute the distance
                distance[item] = distance[node] + 1
                # Update the visited array
                visited[item] = True
                # Compute the minimum bandwidth from source to item
                minimum_bandwidth[item] = min(minimum_bandwidth[node],
                                              G[node][item][
                                                  'residual_bandwidth'])
                # Record the father node of item
                father_node[item] = node
                # Put the item node into open_list
                open_list.put(item)
            # If the item has been visited
            else:
                # If the new path length equals the old path length
                if distance[node] + 1 == distance[item]:
                    # If the minimum bandwidth of new path is bigger
                    # than the old path
                    if min(minimum_bandwidth[node],
                           G[node][item]['residual_bandwidth']) > \
                            minimum_bandwidth[item]:
                        # Update the minimum bandwidth for item
                        minimum_bandwidth[item] = min(minimum_bandwidth[node],
                                                      G[node][item][
                                                          'residual_bandwidth']
                                                      )
                        # Update the father node of item
                        father_node[item] = node
                # If the new path length is less than the old path length
                elif distance[node] + 1 < distance[item]:
                    # Update the distance from source to item
                    distance[item] = distance[node] + 1
                    # Update the father node of item
                    father_node[item] = node
                    # Update the minimum bandwidth of item
                    minimum_bandwidth[item] = min(minimum_bandwidth[node],
                                                  G[node][item][
                                                      'residual_bandwidth'])

    # The dict to store all widest shortest path from source to other nodes
    all_widest_shortest_path = {}
    # Create all nodes set
    destinations = set(G.nodes)
    # Remove the source node
    destinations.remove(source)
    # Traverse all other nodes
    for dst_node in destinations:
        # Initialize the path to dst_node
        path = []
        # Get the path from source to dst_node
        node = dst_node
        while node is not None:
            path.append(node)
            node = father_node[node]
        path.reverse()
        # Store the path for dst_node
        all_widest_shortest_path[dst_node] = path

    return all_widest_shortest_path


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

    draw_topology(G, pos, title='Topology')

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
