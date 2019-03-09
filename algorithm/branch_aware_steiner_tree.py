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
import math

__all__ = [
    'generate_branch_aware_steiner_trees',
    'edge_optimization_phase',
    'branch_optimization_phase'
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
    all_pair_shortest_paths = nx.shortest_path(graph, weight=None)

    for f in allocated_flows:
        branch_aware_steiner_tree = \
            generate_branch_aware_steiner_tree(graph, f['src'],
                                               f['dst'].keys(),
                                               all_pair_shortest_paths, w)
        branch_aware_steiner_trees.append(branch_aware_steiner_tree)

    return branch_aware_steiner_trees


def generate_branch_aware_steiner_tree(G, source, destinations,
                                       all_pair_shortest_paths, w=1):
    tree = edge_optimization_phase(source, destinations,
                                   all_pair_shortest_paths)

    branch_optimization_phase(G, source, destinations, tree,
                              all_pair_shortest_paths)
    # tree = branch_optimization_phase(G, source, destinations, tree,
    #                                  all_pair_shortest_paths)
    # tree = branch_optimization_phase(G, tree)
    # return tree


def edge_optimization_phase(source, destinations, all_pair_shortest_paths):
    """The Edge Optimization Phase according to the paper
    :param source: The source node of multicast tree
    :param destinations: The destination nodes of flow request
    :param all_pair_shortest_paths: Shortest path between any two nodes
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
        # The final path need to add into the tree
        path = None
        # The minimal distance of all shortest paths
        min_dis = math.inf
        # Traverse all nodes in terminals
        for v in terminals:
            # Compute the shortest path from node to tree
            p = shortest_path_to_tree(v, tree, all_pair_shortest_paths)
            # If current distance less than min_dis
            if len(p) < min_dis:
                # Update the min_dis
                min_dis = len(p)
                # And record current path
                path = p
            # If current distance equals min_dis and the first node of path
            # is branch node
            elif len(p) == min_dis and is_branch_node(tree, p[0]):
                # Update the path
                path = p
        # Add the minial shortest path into the tree
        tree.add_path(path)
        # Remove the terminals corresponding to the path
        terminals.remove(path[-1])

    return tree


def shortest_path_to_tree(target, tree, all_pair_shortest_paths):
    """Compute the shortest path from target node to current tree
    :param target: The target node
    :param tree: The constructed multicast tree
    :param all_pair_shortest_paths: Shortest paths for each two nodes
    :return: path(from tree to target)
    """
    # Path initialization
    path = None
    # Traverse all nodes in tree
    for v in tree.nodes:
        # Compute all paths from v to target
        p = all_pair_shortest_paths[v][target]
        # If path is None
        # Or path is not None and the current length of p is less than path
        # Then set p to path
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path


def branch_optimization_phase(G, source, destinations,
                              tree, all_pair_shortest_paths):
    """The Branch Optimization Phase according to the paper
    :param G: The origin graph
    :param source:
    :param destinations:
    :param tree: The tree constructed by edge optimization phase
    :param all_pair_shortest_paths:
    :return:
    """
    # Deletion Step
    branch_nodes = {}
    # Traverse all nodes in tree
    for v in tree.nodes:
        # If it is branch node
        if is_branch_node(tree, v):
            # Record the degree of branch node
            branch_nodes[v] = tree.degree(v)
    # Sort the branch nodes in the ascending order of degree
    branch_nodes = OrderedDict(sorted(branch_nodes.items(),
                                      key=lambda x: x[1]))

    for v_d in branch_nodes:
        print('Remove', v_d)
        neighbors = list(tree.neighbors(v_d))
        tree.remove_node(v_d)

        for v in neighbors:
            path = None
            print('Neighbor', v)
            for u in branch_nodes:
                if u == v_d or nx.node_connectivity(tree, v, u):
                    continue
                p = all_pair_shortest_paths[v][u]
                print('Branch', u, p)
                if path is None or (path is not None and len(p) < len(path)):
                    path = p
            if path is not None:
                tree.add_path(path)
    return tree


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
