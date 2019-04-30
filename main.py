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
from tqdm import trange
import multiprocessing as mp

PERFORMANCE = ['Number of Branch Nodes', 'Average Rejection Rate(%)',
               'Throughput', 'Link Utilization(%)']


def main():
    run_task(lab_1, 'Multicast Group Size')
    run_task(lab_2, 'Number of Requests')
    run_task(lab_3, 'Network Size')


def run_task(fnc, independent_variable, times=6):
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
        result = {'SPT': {}, 'ST': {},
                  'WSPT': {}, 'WST': {},
                  'BST': {}, 'BBSRT': {},
                  'BBST': {}}
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

        if i == 2:
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

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bst = {}
    bbsrt = {}
    bbst = {}

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        st[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        wspt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        wst[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        bst[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]
        bbst[multi_group_size] = [0 for _ in range(len(PERFORMANCE))]

    G = generate_topology(NETWORK_SIZE)

    for multi_group_size in trange(10, 60, 10, desc='Lab 1'):
        flows = generate_flow_requests(G, 20, multi_group_size, 10, 300)

        performance = network_performance(*generate_shortest_path_trees(G,
                                                                        flows))
        spt[multi_group_size] = [spt[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        performance = network_performance(*generate_steiner_trees(G, flows))
        st[multi_group_size] = [st[multi_group_size][i] + performance[i] for i
                                in range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_shortest_path_trees(G, flows))
        wspt[multi_group_size] = [wspt[multi_group_size][i] + performance[i]
                                  for i in range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_steiner_trees(G, flows))
        wst[multi_group_size] = [wst[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_branch_aware_steiner_trees(G, flows, 5))
        bst[multi_group_size] = [bbst[multi_group_size][i] + performance[i]
                                 for i in range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows,
                                                                             5, 0.5, 0.5,
                                                                             1, 5))
        bbsrt[multi_group_size] = [bbsrt[multi_group_size][i] + performance[i]
                                   for i in range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows,
                                                                     0.5, 0.5,
                                                                     1, 5))
        bbst[multi_group_size] = [bbst[multi_group_size][i] + performance[i]
                                  for i in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st,
                  'WSPT': wspt, 'WST': wst,
                  'BST': bst, 'BBSRT': bbsrt,
                  'BBST': bbst})
    lock.release()


def lab_2(datas, lock):
    """The variable is the number of requests
    Compute the performance of network
    :return:
    """
    NETWORK_SIZE = 100

    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bst = {}
    bbsrt = {}
    bbst = {}

    for num_requests in range(10, 80, 10):
        spt[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        st[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        wspt[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        wst[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        bst[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[num_requests] = [0 for _ in range(len(PERFORMANCE))]
        bbst[num_requests] = [0 for _ in range(len(PERFORMANCE))]

    G = generate_topology(NETWORK_SIZE)

    for num_requests in trange(10, 80, 10, desc='Lab 2'):
        flows = generate_flow_requests(G, num_requests, 10, 10, 300)

        performance = network_performance(*generate_shortest_path_trees(G,
                                                                        flows))
        spt[num_requests] = [spt[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(*generate_steiner_trees(G, flows))
        st[num_requests] = [st[num_requests][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_shortest_path_trees(G, flows))
        wspt[num_requests] = [wspt[num_requests][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_steiner_trees(G, flows))
        wst[num_requests] = [wst[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_branch_aware_steiner_trees(G, flows, 5))
        bst[num_requests] = [bst[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows,
                                                                             5, 0.5, 0.5,
                                                                             1, 5))
        bbsrt[num_requests] = [bbsrt[num_requests][i] + performance[i] for i in
                               range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows,
                                                                     0.5, 0.5,
                                                                     1, 5))
        bbst[num_requests] = [bbst[num_requests][i] + performance[i]
                              for i in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st,
                  'WSPT': wspt, 'WST': wst,
                  'BST': bst, 'BBSRT': bbsrt,
                  'BBST': bbst})
    lock.release()


def lab_3(datas, lock):
    """The variable is the network size
    Compute the performance of network
    :return:
    """
    spt = {}
    st = {}
    wspt = {}
    wst = {}
    bst = {}
    bbsrt = {}
    bbst = {}

    for network_size in range(100, 500, 100):
        spt[network_size] = [0 for _ in range(len(PERFORMANCE))]
        st[network_size] = [0 for _ in range(len(PERFORMANCE))]
        wspt[network_size] = [0 for _ in range(len(PERFORMANCE))]
        wst[network_size] = [0 for _ in range(len(PERFORMANCE))]
        bst[network_size] = [0 for _ in range(len(PERFORMANCE))]
        bbsrt[network_size] = [0 for _ in range(len(PERFORMANCE))]
        bbst[network_size] = [0 for _ in range(len(PERFORMANCE))]

    for network_size in trange(100, 500, 100, desc='Lab 3'):
        G = generate_topology(network_size)
        flows = generate_flow_requests(G, network_size // 10,
                                       network_size // 10, 100, 1000)

        performance = network_performance(*generate_shortest_path_trees(G,
                                                                        flows))
        spt[network_size] = [spt[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(*generate_steiner_trees(G, flows))
        st[network_size] = [st[network_size][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_shortest_path_trees(G, flows))
        wspt[network_size] = [wspt[network_size][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_widest_steiner_trees(G, flows))
        wst[network_size] = [wst[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_branch_aware_steiner_trees(G, flows, 5))
        bst[network_size] = [bst[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_segment_routing_trees(G, flows,
                                                                             5, 0.5, 0.5,
                                                                             1, 5))
        bbsrt[network_size] = [bbsrt[network_size][i] + performance[i] for i in
                               range(len(PERFORMANCE))]

        performance = network_performance(
            *generate_bandwidth_efficient_branch_aware_steiner_trees(G, flows,
                                                                     0.5, 0.5,
                                                                     1, 5))
        bbst[network_size] = [bbst[network_size][i] + performance[i] for i
                              in range(len(PERFORMANCE))]

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st,
                  'WSPT': wspt, 'WST': wst,
                  'BST': bst, 'BBSRT': bbsrt,
                  'BBST': bbst})
    lock.release()


if __name__ == '__main__':
    main()
