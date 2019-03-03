"""
@project: RoutingAlgorithm
@author: sam
@file main.py
@ide: PyCharm
@time: 2019-01-30 20:10:18
@blog: https://jiahaoplus.com
"""
from algorithm import *
from network import *
from time import time
import multiprocessing as mp


PERFORMANCE = ['Number of Branch Nodes', 'Average Rejection Rate(%)',
               'Throughput', 'Link Utilization(%)', 'Generate Time']


def main():
    print('Lab 1')
    run_task(lab_1, 'Multicast Group Size')
    # print('Lab 2')
    # run_task(lab_2)
    # print('Lab 3')
    # run_task(lab_3)


def run_task(fnc, independent_variable, times=4):
    """Run different experiments
    :param fnc: Lab name
    :param independent_variable: The independent variable for current lab
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

    for i in range(len(PERFORMANCE)):
        # Result initialize
        result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}, 'BBSRT': {}}
        # Traverse each data and sum all data
        for data in datas:
            # Add each data to the result
            for name in data:
                # Traverse the index
                for index in data[name]:
                    if index in result[name].keys():
                        result[name][index] += data[name][index][i]
                    else:
                        result[name][index] = 0
        # Compute the average data
        for name in result:
            for index in result[name]:
                result[name][index] /= times

        # Output the result
        print(PERFORMANCE[i])
        print('', end='\t')
        for index in result['SPT']:
            print(index, end='\t')
        print()

        for name in result:
            print(name, end='\t')
            for index in result[name]:
                print(result[name][index], end='\t')
            print()

        if i == 2 or i == 4:
            draw_result(result, independent_variable, PERFORMANCE[i], 'bar')
        else:
            draw_result(result, independent_variable, PERFORMANCE[i], 'line')

        print('-------------------------')


def lab_1(datas, lock):
    """The variable is the number of multicast group size
    Compute the performance of network
    :return:
    """
    NETWORK_SIZE = 100
    ALPHA = 0.2
    BETA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        st[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        wspt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        wst[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]

    G, pos = generate_topology(NETWORK_SIZE, ALPHA, BETA)

    for multi_group_size in range(10, 60, 10):
        flows = generate_flow_requests(G, 10, multi_group_size, 100, 500)

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        spt[multi_group_size] = [spt[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        st[multi_group_size] = [st[multi_group_size][i] + performance[i] for i
                                in range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wspt[multi_group_size] = [wspt[multi_group_size][i] + performance[i]
                                  for i in range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wst[multi_group_size] = [wst[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        bbsrt[multi_group_size] = [bbsrt[multi_group_size][i] + performance[i]
                                   for i in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


def lab_2(datas, lock):
    """The variable is the number of requests
    Compute the performance of network
    :return:
    """
    NETWORK_SIZE = 100
    ALPHA = 0.2
    BETA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        st[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        wspt[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        wst[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[num_requests] = [0 for _ in range(len(PERFORMANCE))]

    G, pos = generate_topology(NETWORK_SIZE, ALPHA, BETA)

    for num_requests in range(10, 90, 10):
        flows = generate_flow_requests(G, num_requests, 30, 100, 500)

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        spt[num_requests] = [spt[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        st[num_requests] = [st[num_requests][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wspt[num_requests] = [wspt[num_requests][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wst[num_requests] = [wst[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        bbsrt[num_requests] = [bbsrt[num_requests][i] + performance[i] for i
                               in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


def lab_3(datas, lock):
    """The variable is the network size
    Compute the performance of network
    :return:
    """
    ALPHA = 0.2
    BETA = 0.2

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bbsrt = {}

    for network_size in range(100, 500, 100):
        spt[network_size] = [0 for _ in range(len(PERFORMANCE))]
        st[network_size] = [0 for _ in range(len(PERFORMANCE))]
        wspt[network_size] = [0 for _ in range(len(PERFORMANCE))]
        wst[network_size] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[network_size] = [0 for _ in range(len(PERFORMANCE))]

    for network_size in range(100, 500, 100):
        G, pos = generate_topology(network_size, ALPHA, BETA)
        flows = generate_flow_requests(G, 50, 50, 100, 500)

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        spt[network_size] = [spt[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        st[network_size] = [st[network_size][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_shortest_path_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wspt[network_size] = [wspt[network_size][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_widest_steiner_trees(G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        wst[network_size] = [wst[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        t = time()
        graph, allocated_flows, multicast_trees = \
            generate_bandwidth_efficient_branch_aware_segment_routing_trees(
                G, flows)
        t = time() - t
        performance = network_performance(graph, allocated_flows,
                                          multicast_trees)
        performance.append(t)
        bbsrt[network_size] = [bbsrt[network_size][i] + performance[i] for i
                               in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append(
        {'SPT': spt, 'ST': st, 'WSPT': wspt, 'WST': wst, 'BBSRT': bbsrt})
    lock.release()


if __name__ == '__main__':
    main()
