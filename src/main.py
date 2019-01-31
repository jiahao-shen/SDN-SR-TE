"""
@project: RoutingAlgorithm
@author: sam
@file main.py
@ide: PyCharm
@time: 2019-01-30 20:10:18
@blog: https://jiahaoplus.com
"""
from algorithm.shortest_path_tree import *
from algorithm.steiner_tree import *
from network.utils import *


def main():
    # lab_1()
    # lab_2()
    # lab_3()
    lab_4()


def lab_1():
    # Number of branch nodes vs multicast group size
    NETWORK_SIZE = 100
    TIMES = 4
    BETA = 0.3
    ALPHA = 0.3
    print('Figure 1')

    spt = {}
    st = {}
    wspt = {}

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] = 0
        st[multi_group_size] = 0
        wspt[multi_group_size] = 0

    for t in range(TIMES):

        print('Times', t)

        g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

        for multi_group_size in range(10, 60, 10):
            flows = generate_flow_requests(g, 10, multi_group_size)

            graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
            spt[multi_group_size] += compute_num_branch_nodes(allocated_graph)

            graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
            st[multi_group_size] += compute_num_branch_nodes(allocated_graph)

            graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
            wspt[multi_group_size] += compute_num_branch_nodes(allocated_graph)

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] /= TIMES
        st[multi_group_size] /= TIMES
        wspt[multi_group_size] /= TIMES

    print('SPT :', spt)
    print('ST :', st)
    print('WSPT :', wspt)


def lab_2():
    # Average rejection rate vs number of requests
    NETWORK_SIZE = 100
    TIMES = 4
    BETA = 0.2
    ALPHA = 0.2
    print('Figure 2')

    spt = {}
    st = {}
    wspt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0

    for t in range(TIMES):

        print('Times', t)

        g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

        for num_requests in range(10, 90, 10):
            flows = generate_flow_requests(g, num_requests, 30)

            graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
            spt[num_requests] += compute_average_rejection_rate(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
            st[num_requests] += compute_average_rejection_rate(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
            wspt[num_requests] += compute_average_rejection_rate(allocated_flows)

    for num_requests in range(10, 90, 10):
        spt[num_requests] /= TIMES
        st[num_requests] /= TIMES
        wspt[num_requests] /= TIMES

    print('SPT :', spt)
    print('ST :', st)
    print('WSPT :', wspt)


def lab_3():
    # Average network throughput vs number of requests
    NETWORK_SIZE = 100
    TIMES = 4
    BETA = 0.2
    ALPHA = 0.2
    print('Figure 3')

    spt = {}
    st = {}
    wspt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0

    for t in range(TIMES):

        print('Times', t)

        g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

        for num_requests in range(10, 90, 10):
            flows = generate_flow_requests(g, num_requests, 30)

            graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
            spt[num_requests] += compute_throughput(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
            st[num_requests] += compute_throughput(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
            wspt[num_requests] += compute_throughput(allocated_flows)

    for num_requests in range(10, 90, 10):
        spt[num_requests] /= TIMES
        st[num_requests] /= TIMES
        wspt[num_requests] /= TIMES

    print('SPT :', spt)
    print('ST :', st)
    print('WSPT :', wspt)


def lab_4():
    # Average network throughput vs different network size
    TIMES = 4
    BETA = 0.15
    ALPHA = 0.15
    print('Figure 4')

    spt = {}
    st = {}
    wspt = {}

    for network_size in range(100, 500, 100):
        spt[network_size] = 0
        st[network_size] = 0
        wspt[network_size] = 0

    for t in range(TIMES):

        print('Times', t)

        for network_size in range(100, 500, 100):
            print(network_size)
            g, pos = generate_topology(network_size, BETA, ALPHA)

            flows = generate_flow_requests(g, 10, network_size // 4)

            graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
            spt[network_size] += compute_throughput(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
            st[network_size] += compute_throughput(allocated_flows)

            graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
            wspt[network_size] += compute_throughput(allocated_flows)

    for network_size in range(100, 500, 100):
        spt[network_size] /= TIMES
        st[network_size] /= TIMES
        wspt[network_size] /= TIMES

    print('SPT :', spt)
    print('ST :', st)
    print('WSPT :', wspt)


def test():
    g, pos = generate_topology(100)
    flows = generate_flow_requests(g, 30, 30, 400, 600)

    graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
    print(compute_average_rejection_rate(allocated_flows))


if __name__ == '__main__':
    main()
