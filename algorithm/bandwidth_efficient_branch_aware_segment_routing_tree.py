""""
@project: RoutingAlgorithm
@author: sam
@file bandwidth_efficient_branch_aware_segment_routing_tree.py
@ide: PyCharm
@time: 2019-02-14 20:42:59
@blog: https://jiahaoplus.com
"""
import math
from network import *
from collections import OrderedDict
from algorithm.multicast_tree import *

__all__ = [
    'BandwidthefficientBranchawareSegmentRoutingTree'
]


class BandwidthefficientBranchawareSegmentRoutingTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        super().__init__(G, flows, **kwargs)

        # Add node and edge weight
        nx.set_edge_attributes(self.graph, 0, 'weight')
        nx.set_node_attributes(self.graph, 0, 'weight')

        self.node_bc = nx.betweenness_centrality(self.graph)
        self.edge_bc = nx.edge_betweenness_centrality(self.graph)

        self.deploy()

    def compute(self, source, destinations, **kwargs):
        """BBSRT
        Sheu, J.-P., & Chen, Y.-C. (2017).
        A scalable and bandwidth-efficient multicast algorithm based on segment
        routing in software-defined networking.
        In 2017 IEEE International Conference on Communications (ICC) (pp. 1–6).
        https://doi.org/10.1109/ICC.2017.7997197
        :param source: The source of flow request
        :param destinations: The destinations of request
        :return: Branch-efficient Branch-aware Segment Routing Tree
        """
        # Get the parameter of algorithm
        k = kwargs.get('k', 5)
        alpha = kwargs.get('alpha', 0.5)
        beta = kwargs.get('beta', 0.5)
        w1 = kwargs.get('w1', 1)
        w2 = kwargs.get('w2', 1)

        # Add weight for nodes and edges
        self.__generate_weighted_graph(alpha, beta)
        # Initialize T
        T = nx.Graph()
        T.root = source
        # Dict to store k shortest paths for (source, destinations)
        d_sorted = {}
        # Traverse all destination nodes
        for dst in destinations:
            # Compute the k shortest path from source to dst
            d_sorted[dst] = generate_k_shortest_paths(self.graph, source, dst,
                                                      k, weight='weight')
        # Sort the dict by value
        d_sorted = OrderedDict(sorted(d_sorted.items(),
                                      key=lambda x: compute_path_cost(
                                          self.graph,
                                          x[1][0],
                                          weight='weight')))

        # Traverse the destination nodes in d_sorted
        for dst in d_sorted:
            # If dst already in T, then continue
            if dst in T.nodes:
                continue
            # Initialize path
            path = d_sorted[dst][0]
            # If T isn't empty
            if len(T) != 0:
                # Initialize the minimum cost
                minimum_cost = math.inf
                # Traverse the k shortest path for dst_node
                for p in d_sorted[dst]:
                    # Get the sub_path
                    sub_path = compute_acyclic_sub_path(T, p)
                    # Compute the extra cost according to the paper
                    extra_cost = self.__compute_extra_cost(T, sub_path, w1, w2)
                    # If extra cost less than minimum cost
                    if extra_cost < minimum_cost:
                        # Update minimum cost and path
                        minimum_cost = extra_cost
                        path = sub_path
            # Add path into T
            nx.add_path(T, path)

        return T

    def __generate_weighted_graph(self, alpha, beta):
        """Generate the weighted graph according to the paper
        :param alpha: The parameter of edges for weight
        :param beta: The parameter of nodes for weight
        :return: weighted G
        """
        # Traverse the edges
        for e in self.graph.edges(data=True):
            # Compute the congestion for links
            congestion_index = self.graph.link_capacity / e[2][
                'residual_bandwidth'] - 1
            # Compute the weight according to the equation 3
            e[2]['weight'] = alpha * congestion_index + (
                    1 - alpha) * self.edge_bc[(e[0], e[1])]
        # Traverse the nodes
        for v in self.graph.nodes(data=True):
            # Compute the congestion for nodes
            congestion_index = self.graph.flow_limit / v[1][
                'residual_flow_entries'] - 1
            # Compute the weight according to the equation 4
            v[1]['weight'] = beta * congestion_index + (
                    1 - beta) * self.node_bc[v[0]]

    def __compute_extra_cost(self, tree, path, w1, w2):
        """Compute the extra cost for path
        :param tree: The multicast tree
        :param path: The current path
        :param w1: The first parameter of extra cost
        :param w2: The second parameter of extra cost
        :return: extra_cost
        """
        # Compute the path cost
        extra_cost = w1 * compute_path_cost(self.graph, path, weight='weight')
        # Get the intersection
        intersection = path[0]
        # If intersection is new branch node, add cost of new branch node
        if (intersection == tree.root and tree.degree(intersection) == 1) or \
                (intersection != tree.root and tree.degree(intersection) == 2):
            extra_cost += w2 * self.graph.nodes[intersection]['weight']

        return extra_cost
