"""
@project: RoutingAlgorithm
@author: sam
@file bst.py
@ide: PyCharm
@time: 2019-03-01 14:52:59
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy

__all__ = [
    'generate_branch_aware_steiner_trees'
]


def generate_branch_aware_steiner_trees(G, flows, w=1):
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    branch_aware_steiner_trees = []


def generate_branch_aware_steiner_tree(G, flows, w=1):
    pass


def branch_aware_edge_reduction():
    pass


def edge_optimization_phase(G, source, destinations):
    # All destination nodes
    terminals = set(destinations)
    # The temp tree
    tree = nx.Graph()
    # While terminals set isn't empty
    while terminals:
        # If tree is empty
        if len(tree) == 0:
            # Add source node into tree
            tree.add_node(source)
            # Set the root of tree
            tree.root = source
            #
        else:
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
                paths[node] = shortest_path_to_tree(G, node,
                                                    tree)
                # Update minimal distance
                min_dis = min(min_dis, len(paths[node]))
            # Traverse all shortest paths
            for path in paths.values():
                # If current path length equals the minimal distance
                # And the intersection node is branch node
                if len(path) == min_dis and check_intersection_is_branch(path,
                                                                         tree):
                    # Update the final path
                    final_path = path


def check_intersection_is_branch(path, tree):
    intersection_node = path[-1]
    if (intersection_node == tree.source and tree.degree(
            intersection_node) == 2) or (
            intersection_node != tree.source and tree.degree(
            intersection_node) == 3):
        return True
    return False


def shortest_path_to_tree(G, target, tree, weight=None):
    """Compute the shortest path from node to current tree
    :param G: The origin graph
    :param target: The target node
    :param tree: The constructed multicast tree
    :param weight: The weight for shortest path, default None
    :return: path
    """
    # Path initialization
    path = None
    # Traverse all nodes in tree
    for node in tree.nodes:
        # Compute all paths from node to v
        p = nx.shortest_path(G, target, node, weight)
        # If path is None
        # Or path is not None and the current length of p is less than path
        # Then set p to path
        if path is None or (path is not None and len(p) < len(path)):
            path = p

    return path


def branch_optimization_phase():
    pass


def test_1():
    G = nx.waxman_graph(10, alpha=0.4, beta=0.4)
    edge_optimization_phase(G, 0, [2])


if __name__ == '__main__':
    test_1()
