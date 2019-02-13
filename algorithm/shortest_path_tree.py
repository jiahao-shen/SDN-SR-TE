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
import math

__all__ = [
    'generate_shortest_path_trees',
    'generate_widest_shortest_path_trees',
    'generate_widest_shortest_path'
]


def generate_shortest_path_trees(G, flows):
    """According to the flows and graph, generate Shortest Path Tree(SPT) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    shortest_path_trees = nx.Graph()  # Allocated Graph(Only including path, without link capacity)
    shortest_path_trees.add_nodes_from(G)  # Add nodes from G to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Compute all shortest path from src_node to other nodes
        all_shortest_path = nx.shortest_path(graph, src_node, weight=None)
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Get the shortest path from src_node to dst_node
            shortest_path = all_shortest_path[dst_node]
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, shortest_path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, shortest_path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = shortest_path
                # Add the path into the allocated_graph
                nx.add_path(shortest_path_trees, shortest_path)

    return graph, allocated_flows, shortest_path_trees


def generate_widest_shortest_path_trees(G, flows):
    """According to the flows and graph, generate Widest Shortest Path Tree(WSPT) for multicast
    :param G: The origin graph
    :param flows: The flow request
    :return: allocated_flows, allocated_graph
    """
    graph = G.copy()  # Copy G
    allocated_flows = flows.copy()  # Copy flows

    widest_shortest_path_trees = nx.Graph()  # Widest Shortest Path Tree initialization
    widest_shortest_path_trees.add_nodes_from(G)  # Add nodes from G to to allocated_graph

    # Traverse source nodes in flows
    for src_node in flows:
        # Compute all widest shortest path from src_node to other nodes
        all_widest_shortest_path = generate_widest_shortest_path(graph, src_node)
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Get the widest shortest path from src_node to dst_node
            widest_shortest_path = all_widest_shortest_path[dst_node]
            # Get the size of current flow
            flow_size = flows[src_node][dst_node]['size']
            # Check whether the flow can add into the graph
            if check_path_valid(graph, widest_shortest_path, flow_size):
                # Add the path into the graph
                add_path_to_graph(graph, widest_shortest_path, flow_size)
                # Add the path into the allocated_flows
                allocated_flows[src_node][dst_node]['path'] = widest_shortest_path
                # Add the path into the allocated_graph
                nx.add_path(widest_shortest_path_trees, widest_shortest_path)

    return graph, allocated_flows, widest_shortest_path_trees


def generate_widest_shortest_path(G, source):
    """Compute the widest shortest path from source to other nodes in G
    Using Extension Dijkstra Algorithm
    :param G: The origin graph
    :param source: The source node
    :return: widest_shortest_path
    """
    # The array to store whether the node has been visited
    visited = [False for _ in range(len(G))]
    # The array to store the distance from source to the other nodes
    distance = [math.inf for _ in range(len(G))]
    # The array to store the minimum bandwidth on the path from source to the other nodes
    minimum_bandwidth = [math.inf for _ in range(len(G))]
    # The array to store the father node in path for all nodes
    father_node = [None for _ in range(len(G))]

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
                minimum_bandwidth[item] = min(minimum_bandwidth[node], G[node][item]['residual_bandwidth'])
                # Record the father node of item
                father_node[item] = node
                # Put the item node into open_list
                open_list.put(item)
            # If the item has been visited
            else:
                # The the new path length equals the old path length
                if distance[node] + 1 == distance[item]:
                    # If the minimum bandwidth of new path is bigger than the old path
                    if min(minimum_bandwidth[node], G[node][item]['residual_bandwidth']) > minimum_bandwidth[item]:
                        # Update the minimum bandwidth for item
                        minimum_bandwidth[item] = min(minimum_bandwidth[node], G[node][item]['residual_bandwidth'])
                        # Update the father node of item
                        father_node[item] = node
                # If the new path length is less than the old path length
                elif distance[node] + 1 < distance[item]:
                    # Update the distance from source to item
                    distance[item] = distance[node] + 1
                    # Update the father node of item
                    father_node[item] = node

    # The dict to store all widest shortest path from source to other nodes
    all_widest_shortest_path = {}
    # Create all nodes set
    destinations = set(range(len(G)))
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


def test():
    # g, pos = generate_topology()
    # draw_topology(g, pos, 'Network Topology')
    # flows = generate_flow_requests(g, 19, 19)
    # allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
    # draw_topology(allocated_graph, pos, 'Shortest Path Tree')
    pass


if __name__ == '__main__':
    test()
