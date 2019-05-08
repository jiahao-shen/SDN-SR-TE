"""
@project: RoutingAlgorithm
@author: sam
@file branch_aware_steiner_tree.py
@ide: PyCharm
@time: 2019-03-01 14:52:59
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *
from copy import deepcopy
from collections import OrderedDict
from algorithm.steiner_tree import shortest_path_from_tree

__all__ = [
    'BranchawareSteinerTree',
]


class BranchawareSteinerTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        """
        :param G:
        :param flows:
        :param kwargs:
        """
        super().__init__(G, flows, **kwargs)

        self.all_pair_paths = nx.shortest_path(self.graph)

        self.deploy(**kwargs)

    def compute(self, source, destinations, **kwargs):
        """BST
        Huang, L. H., Hung, H. J., Lin, C. C., & Yang, D. N. (2014).
        Scalable and bandwidth-efficient multicast for software-defined networks.
        2014 IEEE Global Communications Conference, GLOBECOM 2014, 1890–1896.
        https://doi.org/10.1109/GLOCOM.2014.7037084
        :param source: The source node of flow request
        :param destinations: The destinations of flow request
        :return: Branch-aware Steiner Tree
        """
        w = kwargs.get('w', 5)
        # Edge Optimization Phase
        T = self.__edge_optimization_phase(source, destinations)
        # Branch Optimization Phase
        T = self.__branch_optimization_phase(source, destinations, T, w)

        return T

    def __edge_optimization_phase(self, source, destinations):
        """The Edge Optimization Phase according to the paper
        :param source: The source node of flow request
        :param destinations: The destination nodes of flow request
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
                # Get the shortest path from constructed tree to v
                p = shortest_path_from_tree(v, T, self.all_pair_paths)
                # Update path
                if path is None or \
                        (path is not None and len(p) < len(path)) or \
                        (path is not None and len(p) == len(path) and
                         is_branch_node(T, p[0])):
                    path = p
            # Add path into T
            nx.add_path(T, path)
            # Remove the terminal node in current path
            terminals.remove(path[-1])

            # Remove the terminals already in T
            v_d = set()
            for v in terminals:
                if v in T.nodes:
                    v_d.add(v)
            terminals = terminals - v_d

        return T

    def __branch_optimization_phase(self, source, destinations, tree, w=5):
        """The Branch Optimization Phase according to the paper
        :param source: The source node of flow request
        :param destinations: The destination nodes of flow request
        :param tree: The constructed multicast tree
        :param w: The weight of branch nodes
        :return:
        """
        # Deletion Step
        # Get the branch nodes in the ascending order of degree
        branch_nodes = self.__count_branch_nodes_degree(tree)
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
                    # Get the shortest path from v to u
                    p = self.all_pair_paths[v][u]
                    # Update the shortest path from v
                    if path is None or (
                            path is not None and len(p) < len(path)):
                        path = p
                # Add the path
                if path is not None:
                    nx.add_path(tmp_tree, path)

            # If tmp_tree is connected and the value of tmp_tree is less than
            # the old tree, then update the tree
            if nx.is_connected(tmp_tree) and \
                len(nx.cycle_basis(tmp_tree)) == 0 and \
                    self.__compute_objective_value(tmp_tree, w) < \
                    self.__compute_objective_value(tree, w):
                tree = deepcopy(tmp_tree)

        # Alternation Step
        # Get the branch nodes in the ascending order of degree
        branch_nodes = self.__count_branch_nodes_degree(tree)
        # Traverse all branch nodes
        for v_a in branch_nodes:
            # If v_a is source node or v_a in destination nodes
            # If v_a isn't branch node in tree
            # Then continue
            if v_a in destinations or v_a == source:
                continue
            # Store all neighbor nodes of v_a
            neighbors = list(tree.neighbors(v_a))
            # Try to move v_a to u
            for u in neighbors:
                # Copy tree as tmp_tree
                tmp_tree = deepcopy(tree)
                # Remove v_a from tmp_tree
                tmp_tree.remove_node(v_a)
                # Traverse all neighbor nodes for v_a
                for v in neighbors:
                    # Get the shortest path from v to u
                    path = self.all_pair_paths[v][u]
                    # Move path(v, v_a) to path(v, u)
                    nx.add_path(tmp_tree, path)
                # If tmp_tree is connected and the value of tmp_tree is less
                # than the old tree, then update the tree
                if nx.is_connected(tmp_tree) and \
                    len(nx.cycle_basis(tmp_tree)) == 0 and \
                        self.__compute_objective_value(tmp_tree, w) < \
                        self.__compute_objective_value(tree, w):
                    tree = deepcopy(tmp_tree)

        return tree

    @classmethod
    def __compute_objective_value(cls, tree, w):
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

    @classmethod
    def __count_branch_nodes_degree(cls, tree):
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
