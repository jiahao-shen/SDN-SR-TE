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
]


def generate_branch_aware_steiner_trees(G, flows, w=1):
    """According to flows and graph, generate Branch-aware Steiner Tree(BST)
    :param G: The origin graph
    :param flows: The flow request
    :param w: The weight of branch nodes
    :return:
    """
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    # Generate all pair shortest path
    all_pair_paths = nx.shortest_path(graph)
    # Initialize branch_aware_steiner_trees
    branch_aware_steiner_trees = []

    for f in allocated_flows:
        origin_T = generate_branch_aware_steiner_tree(f['src'], f['dst'],
                                                      all_pair_paths, w)
        # Add origin_T into branch_aware_steiner_trees
        branch_aware_steiner_trees.append(origin_T)

        # Compute all paths in origin_T
        all_paths = nx.shortest_path(origin_T, f['src'])
        # Initialize allocated_T
        allocated_T = nx.Graph()
        allocated_T.root = f['src']
        # Traverse all destination nodes
        for dst in f['dst']:
            # Get the path from src to dst
            path = all_paths[dst]
            # Check whether the path valid
            if is_path_valid(graph, allocated_T, path, f['size']):
                # Record the path
                f['dst'][dst] = path
                # Add path into allocated_T
                allocated_T.add_path(path)
        # Update the information of graph
        update_topo_info(graph, allocated_T, f['size'])

    return graph, allocated_flows, branch_aware_steiner_trees


def generate_branch_aware_steiner_tree(source, destinations,
                                       all_pair_paths, w):
    """Generate Branch-aware Steiner Tree(BST)
    Huang, L. H., Hung, H. J., Lin, C. C., & Yang, D. N. (2014).
    Scalable and bandwidth-efficient multicast for software-defined networks.
    2014 IEEE Global Communications Conference, GLOBECOM 2014, 1890–1896.
    https://doi.org/10.1109/GLOCOM.2014.7037084
    :param source: The source node of flow request
    :param destinations: The destinations of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :param w: The weight of branch nodes
    :return: Branch-aware Steiner Tree
    """
    # Edge Optimization Phase
    T = edge_optimization_phase(source, destinations, all_pair_paths)
    # Branch Optimization Phase
    T = branch_optimization_phase(source, destinations, T, all_pair_paths, w)

    return T


def edge_optimization_phase(source, destinations, all_pair_paths):
    """The Edge Optimization Phase according to the paper
    :param source: The source node of flow request
    :param destinations: The destination nodes of flow request
    :param all_pair_paths: Shortest paths between any two nodes
    :return: T
    """
    # Initialize T
    T = nx.Graph()
    T.add_node(source)
    T.root = source
    # Initialize terminals
    terminals = set(destinations)
    # While terminals isn't empty
    while terminals:
        # Initialize path
        path = None
        # Traverse all terminals
        for v in terminals:
            # Get the shortest path fro v to constructed tree
            p = shortest_path_to_tree(v, T, all_pair_paths)
            # Update path
            if path is None or \
                    (path is not None and len(p) < len(path)) or \
                    (path is not None and len(p) == len(path) and
                     is_branch_node(T, p[0])):
                path = p
        # Add path into T
        T.add_path(path)
        # Remove the terminal node in current path
        terminals.remove(path[-1])

        # Remove the terminals already in T
        v_d = set()
        for v in terminals:
            if v in T.nodes:
                v_d.add(v)
        terminals = terminals - v_d

    return T


def branch_optimization_phase(source, destinations, tree, all_pair_paths, w):
    """The Branch Optimization Phase according to the paper
    :param source: The source node of flow request
    :param destinations: The destinations of flow request
    :param tree: The constructed multicast tree
    :param all_pair_paths: Shortest paths between any two nodes
    :param w: The weight of branch nodes
    :return: T
    """
    # Deletion Step
    # Get the branch nodes in the ascending order of degree
    branch_nodes = count_branch_nodes_degree(tree)
    # Traverse all branch nodes
    for v_d in branch_nodes:
        # If v_d is source node or v_d in destination nodes
        # Then continue
        if v_d in destinations or v_d == source:
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
                # If u isn't in tmp_tree
                # If v and u are in the same connected components
                # Then continue
                if v == u or \
                        u not in tmp_tree.nodes or \
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
                # Else add path into tmp_tree
                tmp_tree.add_path(path)

        # If tmp_tree is connected and the value of tmp_tree is less than the
        # old tree, then update the tree
        if nx.is_connected(tmp_tree) and \
                nx.cycle_basis(tmp_tree) == 0 and \
                compute_objective_value(tmp_tree, w) < \
                compute_objective_value(tree, w):
            tree = deepcopy(tmp_tree)

    # Alternation Step
    # Get the branch nodes in the ascending order of degree
    branch_nodes = count_branch_nodes_degree(tree)
    # Traverse all branch nodes
    for v_a in branch_nodes:
        # If v_a is source node or v_a in destination nodes
        # If v_a isn't branch node in tree
        # Then continue
        if v_a in destinations or v_a == source:
            continue
        # Store all neighbor nodes of v_a
        neighbors = list(tree.neighbors(v_a))
        # Copy tree as tmp_tree
        tmp_tree = deepcopy(tree)
        # Remove v_a from tmp_tree
        tmp_tree.remove_node(v_a)
        # Try to move v_a to u
        for u in neighbors:
            # Traverse all neighbor nodes for v_a
            for v in neighbors:
                # Get the shortest path from v to u
                path = all_pair_paths[v][u]
                # Move path(v, v_a) to path(v, u)
                tmp_tree.add_path(path)
            # If tmp_tree is connected and the value of tmp_tree is less than
            # the old tree, then update the tree
            if nx.is_connected(tmp_tree) and \
                len(nx.cycle_basis(tmp_tree)) == 0 and \
                    compute_objective_value(tmp_tree, w) < \
                    compute_objective_value(tree, w):
                tree = deepcopy(tmp_tree)

    return tree


def compute_objective_value(tree, w):
    """Compute the objective value according to the paper
    A(T) = c(T) + b(T) * w
    :param tree: The constructed multicast tree
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
    :param tree: The constructed multicast tree
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
