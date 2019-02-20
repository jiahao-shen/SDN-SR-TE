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
from algorithm.segment_routing import *
from network.topology import *
import multiprocessing as mp


def main():
    # print('Lab 1')
    # run_task(lab_1)
    print('Lab 2')
    run_task(lab_2)
    print('Lab 3')
    run_task(lab_3)
    # print('Lab 4')
    # run_task(lab_4)


def run_task(fnc, times=4):
    """Run different experiments
    :param fnc: Lab name
    :param times: The running times for each lab
    :return:
    """
    # Process list
    processes = []
    # Number of experiments

    # Shared list to store datas
    datas = mp.Manager().list()
    # The lock for parallel computing
    lock = mp.Manager().Lock()

    # Create multiprocess to run
    for i in range(times):
        processes.append(mp.Process(target=fnc, args=(datas, lock)))

    # Start all the process
    for process in processes:
        process.start()

    # Block
    for process in processes:
        process.join()

    # The final result
    result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}, 'BBSRT': {}}

    # Traverse each data
    for data in datas:
        # Add each data to the result
        for name in data:
            for index in data[name]:
                if index in result[name].keys():
                    result[name][index] += data[name][index]
                else:
                    result[name][index] = 0

    # Compute the average data
    for name in result:
        for index in result[name]:
            result[name][index] /= times

    # Output the result
    print('', end='\t')
    for index in result['SPT']:
        print(index, end='\t')

    print()

    for name in result:
        print(name, end='\t')
        for index in result[name]:
            print(result[name][index], end='\t')
        print()

    print('----------------------------')


def lab_1(datas, lock):
    # Number of branch nodes vs multicast group size
    NETWORK_SIZE = 100
    ALPHA = 0.3
    BETA = 0.3

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] = 0
        st[multi_group_size] = 0
        wspt[multi_group_size] = 0
        wst[multi_group_size] = 0
        bbsrt[multi_group_size] = 0

    g, pos = generate_topology(NETWORK_SIZE, ALPHA, BETA, flow_limit=50)

    for multi_group_size in range(10, 60, 10):
        flows = generate_flow_requests(g, 10, multi_group_size)

        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(g, flows)
        spt[multi_group_size] += compute_num_branch_nodes(multicast_trees)

        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(g, flows)
        st[multi_group_size] += compute_num_branch_nodes(multicast_trees)

        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(g, flows)
        wspt[multi_group_size] += compute_num_branch_nodes(multicast_trees)

        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(g, flows)
        wst[multi_group_size] += compute_num_branch_nodes(multicast_trees)

        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                g, flows)
        bbsrt[multi_group_size] += compute_num_branch_nodes(multicast_trees)

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


def lab_2(datas, lock):
    # Average rejection rate vs number of requests
    NETWORK_SIZE = 100
    ALPHA = 0.2
    BETA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0
        wst[num_requests] = 0
        bbsrt[num_requests] = 0

    g, pos = generate_topology(NETWORK_SIZE, ALPHA, BETA)

    for num_requests in range(10, 90, 10):
        flows = generate_flow_requests(g, num_requests, 30, size_lower=100,
                                       size_upper=200)

        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(g, flows)
        spt[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(g, flows)
        st[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(g, flows)
        wspt[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(g, flows)
        wst[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                g, flows)
        bbsrt[num_requests] += compute_average_rejection_rate(allocated_flows)

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


def lab_3(datas, lock):
    # Average network throughput vs number of requests
    NETWORK_SIZE = 100
    ALPHA = 0.2
    BETA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0
        wst[num_requests] = 0
        bbsrt[num_requests] = 0

    g, pos = generate_topology(NETWORK_SIZE, ALPHA, BETA)

    for num_requests in range(10, 90, 10):
        flows = generate_flow_requests(g, num_requests, 30, size_lower=100,
                                       size_upper=200)

        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(g, flows)
        spt[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(g, flows)
        st[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(g, flows)
        wspt[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = generate_widest_steiner_trees(
            g, flows)
        wst[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                g, flows)
        bbsrt[num_requests] += compute_throughput(allocated_flows)

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


def lab_4(datas, lock):
    # Average network throughput vs different network size
    BETA = 0.2
    ALPHA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for network_size in range(100, 500, 100):
        spt[network_size] = 0
        st[network_size] = 0
        wspt[network_size] = 0
        wst[network_size] = 0
        bbsrt[network_size] = 0

    for network_size in range(100, 500, 100):
        g, pos = generate_topology(network_size, ALPHA, BETA)

        flows = generate_flow_requests(g, network_size // 4, network_size // 4,
                                       size_lower=100, size_upper=200)

        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(g, flows)
        spt[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(g, flows)
        st[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(g, flows)
        wspt[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(g, flows)
        wst[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                g, flows)
        bbsrt[network_size] += compute_throughput(allocated_flows)

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


if __name__ == '__main__':
    main()
