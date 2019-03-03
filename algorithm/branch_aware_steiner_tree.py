"""
@project: RoutingAlgorithm
@author: sam
@file branch_aware_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:52:59
@blog: https://jiahaoplus.com
"""
from network import *
from collections import OrderedDict
from copy import deepcopy

__all__ = [
    'generate_branch_aware_steiner_trees'
]


def generate_branch_aware_steiner_trees(G, flows, w=1):
    """According to flows and graph, generate Branch-aware Steiner Tree(BST)
    Huang, L. H., Hung, H. J., Lin, C. C., & Yang, D. N. (2014).
    Scalable and bandwidth-efficient multicast for software-defined networks.
    2014 IEEE Global Communications Conference, GLOBECOM 2014, 1890–1896.
    https://doi.org/10.1109/GLOCOM.2014.7037084
    :param G: The origin graph
    :param flows: The flow request
    :param w: The parameter of branch node
    :return:
    """
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    branch_aware_steiner_trees = []
    # Pre-processing procedure for quickly lookup afterwards
    # Generate shortest path between any two nods in G
    all_pair_shortest_path = nx.shortest_path(graph, weight=None)

    for f in allocated_flows:
        branch_aware_steiner_tree = \
            generate_branch_aware_steiner_tree(graph, f['src'],
                                               f['dst'].keys(),
                                               all_pair_shortest_path, w)
        branch_aware_steiner_trees.append(branch_aware_steiner_tree)

    return branch_aware_steiner_trees


def generate_branch_aware_steiner_tree(G, source, destinations,
                                       all_pair_shortest_path, w=1):
    tree = edge_optimization_phase(G, source, destinations,
                                   all_pair_shortest_path)

    tree = branch_optimization_phase(G, source, destinations, tree,
                                     all_pair_shortest_path)
    # tree = branch_optimization_phase(G, tree)
    return tree


def edge_optimization_phase(G, source, destinations, all_pair_shortest_path):
    """The Edge Optimization Phase according to the paper
    :param G: The origin graph
    :param source: The source node of multicast tree
    :param destinations: The destination nodes of flow request
    :param all_pair_shortest_path: Shortest path between any two nodes
    :return:
    """
    # All destination nodes
    terminals = set(destinations)
    # The temp tree initialize and set source node as root of tree
    tree = nx.Graph()
    tree.add_node(source)
    tree.root = source
    # While terminals set isn't empty
    while terminals:
        # Traverse all nodes in tree
        for node in tree.nodes:
            # If node in terminals
            if node in terminals:
                # Remove node from terminals
                terminals.remove(node)
        # The final path need to add into the tree
        final_path = None
        # The paths to record all shortest paths from terminals to tree
        paths = {}
        # The minimal distance of all shortest paths
        min_dis = math.inf
        # Traverse all nodes in terminals
        for node in terminals:
            # Record the shortest path from node to tree
            paths[node] = shortest_path_to_tree(node, tree,
                                                all_pair_shortest_path)
            # Update minimal distance
            min_dis = min(min_dis, len(paths[node]))
        # Traverse all shortest paths
        for path in paths.values():
            # If the final path is None and current path length equals
            # the minial distance
            # Update the final_path
            if final_path is None and len(path) == min_dis:
                final_path = path
            # If the final path isn't None and current path length equals
            # the minimal distance and the intersection node is branch node
            elif final_path is not None and len(path) == min_dis and \
                    is_branch_node(tree, path[-1]):
                # Update the final path
                final_path = path
                break
        # Add the minial shortest path into the tree
        tree.add_path(final_path)
        # And remove the intersection node from terminals
        terminals.remove(final_path[0])

    return tree


def shortest_path_to_tree(target, tree, all_pair_shortest_path):
    """Compute the shortest path from node to current tree
    :param target: The target node
    :param tree: The constructed multicast tree
    :param all_pair_shortest_path: Shortest path for each two nodes
    :return: path
    """
    # Path initialization
    path = None
    # Traverse all nodes in tree
    for node in tree.nodes:
        # Compute all paths from node to v
        p = all_pair_shortest_path[target][node]
        # If path is None
        # Or path is not None and the current length of p is less than path
        # Then set p to path
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path


def branch_optimization_phase(G, source, destinations,
                              tree, all_pair_shortest_path):
    """The Branch Optimization Phase according to the paper
    :param G: The origin graph
    :param source:
    :param destinations:
    :param tree: The tree constructed by edge optimization phase
    :param all_pair_shortest_path:
    :return:
    """
    # Deletion Step
    branch_nodes = {}
    # Traverse all nodes in tree
    for node in tree.nodes:
        # If it is branch node
        if is_branch_node(tree, node):
            # Record the degree of branch node
            branch_nodes[node] = tree.degree(node)
    # Sort the branch nodes in the ascending order of degree
    branch_nodes = OrderedDict(sorted(branch_nodes.items(),
                                      key=lambda x: x[1]))

    # Initialize the terminals
    terminals = set(destinations)
    terminals.add(source)

    for v_d in branch_nodes.keys():
        neighbors = list(tree.neighbors(v_d))
        tree.remove_node(v_d)

        for v in neighbors:
            if v in branch_nodes.keys() or v in terminals:
                path = None
                for u in branch_nodes.keys():
                    if u == v_d:
                        continue
                    p = all_pair_shortest_path[v][u]
                    if path is None or (path is not None and
                                        len(p) < len(path)):
                        path = p
                tree.add_path(path)

    return tree

    # print(branch_nodes.keys())


def test_1():
    G, pos = generate_topology()
    flows = generate_flow_requests(G, flow_entries=8)
    output_flows(flows)
    draw_topology(G, pos)

    multicast_trees = generate_branch_aware_steiner_trees(G, flows)

    for tree in multicast_trees:
        draw_topology(tree, pos)


def test_2():
    pass


if __name__ == '__main__':
    test_1()
    # test_2()
