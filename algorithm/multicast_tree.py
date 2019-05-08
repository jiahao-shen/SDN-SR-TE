"""
@project: SDN-SR-TE
@author: sam
@file multicast_tree.py
@ide: PyCharm
@time: 2019-05-08 17:31:21
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy
from abc import abstractmethod

__all__ = [
    'MulticastTree'
]


class MulticastTree(object):

    def __init__(self, G, flows, **kwargs):
        """
        :param G:
        :param flows:
        :param kwargs:
        """
        self.graph = deepcopy(G)
        self.allocated_flows = deepcopy(flows)
        self.multicast_trees = []

    @abstractmethod
    def compute(self, source, destinations, **kwargs):
        """The abstract method for each algorithm
        :param source:
        :param destinations:
        :param kwargs:
        :return:
        """
        pass

    def deploy(self, **kwargs):
        """Deploy the multicast tree in topology graph
        :param kwargs:
        :return:
        """
        # Traverse all flows
        for f in self.allocated_flows:
            # Compute the origin_T
            origin_T = self.compute(f['src'], f['dst'], **kwargs)
            # Add origin_T into multicast_trees
            self.multicast_trees.append(origin_T)

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
                if is_path_valid(self.graph, allocated_T, path, f['size']):
                    # Record the path
                    f['dst'][dst] = path
                    # Add path into allocated_T
                    nx.add_path(allocated_T, path)
            # Update the information of graph
            update_topo_info(self.graph, allocated_T, f['size'])

    def network_performance(self):
        """Compute performance of the network
        Including number of branch nodes, average rejection rate,
        average network throughput and link utilization
        :return:
        """
        return [self.compute_num_branch_nodes(),
                self.compute_average_rejection_rate(),
                self.compute_throughput(),
                self.compute_link_utilization()]

    def compute_num_branch_nodes(self):
        """Compute the number of branch nodes
        :return: num_branch_nodes
        """
        num_branch_nodes = 0

        for T in self.multicast_trees:
            for v in T.nodes:
                if is_branch_node(T, v):
                    num_branch_nodes += 1

        num_branch_nodes /= len(self.multicast_trees)

        return num_branch_nodes

    def compute_average_rejection_rate(self):
        """Compute the number of average rejection rate
        :return: average_rejection_rate(%)
        """
        num_total_flows = 0
        num_unallocated_flows = 0
        # Traverse all allocated flows
        for f in self.allocated_flows:
            for dst in f['dst']:
                # Compute the number of total flows
                num_total_flows += 1
                # If current flow is allocated
                if f['dst'][dst] is None:
                    num_unallocated_flows += 1

        # Compute the average rejection rate
        average_rejection_rate = num_unallocated_flows / num_total_flows
        # Transform to percentage
        average_rejection_rate *= 100

        return average_rejection_rate

    def compute_throughput(self):
        """Compute the network throughput
        :return: throughput(MB)
        """
        throughput = 0
        # Traverse all allocated flows
        for f in self.allocated_flows:
            for dst in f['dst']:
                # If current flow is allocated
                if f['dst'][dst] is not None:
                    # Sum the flow size
                    throughput += f['size']

        return throughput

    def compute_link_utilization(self):
        """Compute the link utilization
        :return: link_utilization
        """
        total_bandwidth = 0
        total_residual_bandwidth = 0
        # Traverse all edges in G
        for e in self.graph.edges(data=True):
            total_bandwidth += self.graph.link_capacity
            total_residual_bandwidth += e[2]['residual_bandwidth']

        # Compute the link utilization
        link_utilization = 1 - total_residual_bandwidth / total_bandwidth
        # Transform to percentage
        link_utilization *= 100

        return link_utilization

    def draw(self):
        """
        :return:
        """
        for T in self.multicast_trees:
            pos = graphviz_layout(T, prog='dot')
            draw_topology(T, pos)
