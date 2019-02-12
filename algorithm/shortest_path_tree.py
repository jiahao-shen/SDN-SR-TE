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
    'generate_widest_shortest_path_trees'
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
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Compute the shortest path from src_node to dst_node, not considering weight
            shortest_path = nx.shortest_path(graph, src_node, dst_node, weight=None)
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
        # Traverse destination nodes corresponding to src_node
        for dst_node in flows[src_node].keys():
            # Get the widest shortest path in all shortest paths from src_node to dst_node, not considering weight
            widest_shortest_path = generate_widest_shortest_path(graph, src_node, dst_node)
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


# def generate_widest_shortest_path(all_shortest_paths, graph):
#     """Compute the widest path in all shortest paths
#     :param all_shortest_paths: All shortest paths
#     :param graph: The origin graph
#     :return: widest_shortest_path
#     """
#     # Initialization
#     widest_shortest_path = None
#     # Initialization
#     max_minimum_residual_bandwidth = -math.inf
#
#     # Traverse all shortest paths
#     for path in all_shortest_paths:
#         minimum_residual_bandwidth = math.inf
#         # Traverse current path edges
#         for i in range(len(path) - 1):
#             # Get the residual bandwidth for current edge
#             residual_bandwidth = graph[path[i]][path[i + 1]]['link_capacity'] - graph[path[i]][path[i + 1]][
#                 'used_bandwidth']
#             # Get the minimum residual bandwidth
#             minimum_residual_bandwidth = min(minimum_residual_bandwidth, residual_bandwidth)
#
#         # If find the wider minimum residual bandwidth
#         if minimum_residual_bandwidth > max_minimum_residual_bandwidth:
#             max_minimum_residual_bandwidth = minimum_residual_bandwidth
#             widest_shortest_path = path
#
#     return widest_shortest_path


def generate_widest_shortest_path(G, source, destination):
    """Compute the widest shortest path from source to destination in G
    Using Extension Dijkstra Algorithm
    :param G: The origin graph
    :param source: The source node
    :param destination: The destination node
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
    # Put the source node into queue
    open_list.put(source)

    while not open_list.empty():
        # Get the top node of open_list
        node = open_list.get()
        # If the node is destination node, then break the loop
        if node == destination:
            break
        # Traverse all the neighbor nodes for node
        for item in G.neighbors(node):  # For current node item
            # If the item hasn't been visited
            if not visited[item]:
                # Compute the distance
                distance[item] = distance[node] + 1
                # Update the visited array
                visited[item] = True
                # Compute the residual bandwidth of edge[node][item]
                residual_bandwidth = G[node][item]['link_capacity'] - G[node][item]['used_bandwidth']
                # Compute the minimum bandwidth from source to item
                minimum_bandwidth[item] = min(minimum_bandwidth[node], residual_bandwidth)
                # Record the father node of item
                father_node[item] = node
                # Put the item node into open_list
                open_list.put(item)
            # If the item has been visited
            else:
                # The the new path length equals the old path length
                if distance[node] + 1 == distance[item]:
                    # Compute the residual bandwidth of edge[node][item]
                    residual_bandwidth = G[node][item]['link_capacity'] - G[node][item]['used_bandwidth']
                    # If the minimum bandwidth of new path is bigger than the old path
                    if min(minimum_bandwidth[node], residual_bandwidth) > minimum_bandwidth[item]:
                        # Update the minimum bandwidth for item
                        minimum_bandwidth[item] = min(minimum_bandwidth[node], residual_bandwidth)
                        # Update the father node of item
                        father_node[item] = node
                # If the new path length is less than the old path length
                elif distance[node] + 1 < distance[item]:
                    # Update the distance from source to item
                    distance[item] = distance[node] + 1
                    # Update the father node of item
                    father_node[item] = node

    # The final path
    widest_shortest_path = []

    # Reverse traversal
    node = destination
    while node is not None:
        widest_shortest_path.append(node)
        node = father_node[node]
    widest_shortest_path.reverse()

    return widest_shortest_path


def test():
    # g, pos = generate_topology()
    # draw_topology(g, pos, 'Network Topology')
    # flows = generate_flow_requests(g, 19, 19)
    # allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
    # draw_topology(allocated_graph, pos, 'Shortest Path Tree')
    pass


if __name__ == '__main__':
    test()
