"""
@project: RoutingAlgorithm
@author: sam
@file branch_aware_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:52:59
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.steiner_tree import shortest_path_to_tree
from collections import OrderedDict
from copy import deepcopy

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
    :param w: The weight of branch nodes
    :return:
    """
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    branch_aware_steiner_trees = []
    # Pre-processing procedure for quickly lookup afterwards
    # Generate shortest path between any two nods in G
    all_pair_paths = nx.shortest_path(graph)

    for f in allocated_flows:
        origin_T = generate_branch_aware_steiner_tree(f['src'],
                                                      f['dst'].keys(),
                                                      all_pair_paths, w)
        # Add origin_T into branch_aware_steiner_trees
        branch_aware_steiner_trees.append(origin_T)

        # # Compute all paths in origin_T
        # all_paths = nx.shortest_path(origin_T, f['src'])
        # # Initialize allocated_T
        # allocated_T = nx.Graph()
        # allocated_T.root = f['src']
        # # Traverse all destination nodes
        # for dst in f['dst']:
        #     # Get the path from src to dst
        #     path = all_paths[dst]
        #     # Check whether the path valid
        #     if is_path_valid(graph, allocated_T, path, f['size']):
        #         # Record the path
        #         f['dst'][dst] = path
        #         # Add path into allocated_T
        #         allocated_T.add_path(path)
        # # Update the residual flow entries of nodes in the allocated_T
        # update_node_entries(graph, allocated_T)
        # # Update the residual bandwidth of edges in the allocated_T
        # update_edge_bandwidth(graph, allocated_T, f['size'])

    return graph, allocated_flows, branch_aware_steiner_trees


def generate_branch_aware_steiner_tree(source, destinations,
                                       all_pair_paths, w):
    """Generate Branch-aware Steiner Tree
    :param source: The source node of multicast tree
    :param destinations: The destination nodes of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :param w: The weight of branch nodes
    :return: tree
    """
    # Edge Optimization Phase
    tree = edge_optimization_phase(source, destinations,
                                   all_pair_paths)
    # Branch Optimization Phase
    tree = branch_optimization_phase(source, destinations, tree,
                                     all_pair_paths, w)
    return tree


def edge_optimization_phase(source, destinations, all_pair_paths):
    """The Edge Optimization Phase according to the paper
    :param source: The source node of multicast tree
    :param destinations: The destination nodes of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :return: tree
    """
    # All destination nodes
    terminals = set(destinations)
    # Initialize T and set source node as root of T
    tree = nx.Graph()
    tree.add_node(source)
    tree.root = source
    # While terminals set isn't empty
    while terminals:
        # Path initialize
        path = None
        # Traverse all nodes in terminals
        for v in terminals:
            # Compute the shortest path from node to tree
            p = shortest_path_to_tree(v, tree, all_pair_paths)
            # If current distance less than min_dis
            if path is None or \
                    (path is not None and len(p) < len(path)) or \
                    (path is not None and len(p) == len(path) and
                     is_branch_node(tree, p[0])):
                # And record current path
                path = p
        # Add the minial shortest path into the tree
        tree.add_path(path)
        # Remove the terminals corresponding to the path
        terminals.remove(path[-1])

    return tree


# TODO(Loop edges)
def branch_optimization_phase(source, destinations,
                              tree, all_pair_paths, w):
    """The Branch Optimization Phase according to the paper
    :param source: The source node of multicast tree
    :param destinations: The destination nodes of flow request
    :param tree: The tree constructed by edge optimization phase
    :param all_pair_paths: Shortest path between any two nodes
    :param w: The weight of branch node
    :return: tree
    """
    T_1 = deepcopy(tree)
    # Deletion Step
    # Get the branch nodes in the ascending order of degree
    branch_nodes = count_branch_nodes_degree(tree)
    # Traverse all branch nodes
    for v_d in branch_nodes:
        # If v_d is source node or v_d in destination nodes
        # If v_d isn't branch node in tree
        # Then continue
        if v_d in destinations or v_d == source or \
                not is_branch_node(tree, v_d):
            continue
        # Store all neighbor nodes of v_d
        neighbors = list(tree.neighbors(v_d))
        # Copy tree as tmp_tree
        tmp_tree = deepcopy(tree)
        # Remove v_d from tmp_tree
        tmp_tree.remove_node(v_d)
        # Traverse all neighbor nodes of v_d
        for v in neighbors:
            # Initialize path
            path = None
            # Traverse all branch nodes
            for u in branch_nodes:
                # If v == u
                # If node v isn't in tmp_tree
                # If u isn't branch node after deleting v_d
                # If v and u are in the same connected components
                # Then continue
                if v == u or \
                        u not in tmp_tree.nodes or \
                        not is_branch_node(tmp_tree, u) or \
                        nx.node_connectivity(tmp_tree, v, u):
                    continue
                # Get the shortest path from neighbor node v to branch node u
                p = all_pair_paths[v][u]
                # Update the shortest path from v
                if path is None or (path is not None and len(p) < len(path)):
                    path = p
            # If the path is None, then break
            if path is None:
                break
            else:
                print('Delete:', v_d, ', Neighbor:', v, ', path:', path)
                # Else add path into tmp_tree
                tmp_tree.add_path(path)

        # If tmp_tree is connected and the value of tmp_tree is less than the
        # old tree, then update the tree
        if nx.is_connected(tmp_tree) and \
                compute_objective_value(tmp_tree, w) < \
                compute_objective_value(tree, w):
            tree = deepcopy(tmp_tree)

        if nx.cycle_basis(tree):
            pos = graphviz_layout(T_1, prog='dot')
            draw_topology(T_1, pos, title='Edge Optimization Phase')

            pos = graphviz_layout(tree, prog='dot')
            draw_topology(tree, pos, title='Delete %s' % v_d)

    # # Alternation Step
    # # Get the branch nodes in the ascending order of degree
    # branch_nodes = count_branch_nodes_degree(tree)
    # # Traverse all branch nodes
    # for v_a in branch_nodes:
    #     # If v_a is source node or v_a in destination nodes
    #     # If v_a isn't branch node in tree
    #     # Then continue
    #     if v_a in destinations or v_a == source or \
    #             not is_branch_node(tree, v_a):
    #         continue
    #     # Store all neighbor nodes of v_a
    #     neighbors = list(tree.neighbors(v_a))
    #     # Try to move v_a to u
    #     for u in neighbors:
    #         # Copy tree as tmp_tree
    #         tmp_tree = deepcopy(tree)
    #         # Remove v_a from tmp_tree
    #         tmp_tree.remove_node(v_a)
    #         # Traverse all neighbor nodes for v_a
    #         for v in neighbors:
    #             # Get the shortest path from v to u
    #             path = all_pair_paths[v][u]
    #             # Add path into tmp_tree
    #             # Move path(v, v_a) to path(v, u)
    #             tmp_tree.add_path(path)
    #         # If tmp_tree is connected and the value of tmp_tree is less than
    #         # the old tree, then update the tree
    #         if nx.is_connected(tmp_tree) and \
    #                 compute_objective_value(tmp_tree, w) < \
    #                 compute_objective_value(tree, w):
    #             tree = deepcopy(tmp_tree)

    return tree


def compute_objective_value(tree, w):
    """Compute the objective value according to the paper
    A(T) = c(T) + b(T) * w
    :param tree: The generated multicast tree
    :param w: The weight of branch nodes
    :return: value
    """
    # A(T) = c(T)
    value = nx.number_of_edges(tree)
    # Traverse all nodes in tree
    for v in tree.nodes:
        # If v is branch node
        if is_branch_node(tree, v):
            # Value add w
            value += w

    return value


def count_branch_nodes_degree(tree):
    """Count the degree of branch nodes and sort them in the ascending order of
    the degree in tree
    :param tree: The origin multicast tree
    :return: The ordered branch nodes
    """
    # Initialize branch nodes
    branch_nodes = {}
    # Traverse all nodes in tree
    for v in tree.nodes:
        # If v is branch nodes
        if is_branch_node(tree, v):
            # Store the degree of node v
            branch_nodes[v] = tree.degree(v)
    # Sort all branch nodes in the ascending order of the degree in tree
    branch_nodes = OrderedDict(sorted(branch_nodes.items(),
                                      key=lambda x: x[1]))

    return branch_nodes
