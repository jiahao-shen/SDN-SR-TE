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
import multiprocessing as mp


def main():
    # print('Lab 1')
    # run_task(lab_1)
    # print('Lab 2')
    # run_task(lab_2)
    # print('Lab 3')
    # run_task(lab_3)
    print('Lab 4')
    run_task(lab_4)


def run_task(fnc, times=4):
    """Run different experiments
    :param fnc: Lab name
    :param times: The running times for each lab
    :return:
    """
    # Process list
    p = []
    # Number of experiments

    # Shared list to store datas
    datas = mp.Manager().list()
    # The lock for parallel computing
    lock = mp.Manager().Lock()

    # Create multiprocess to run
    for i in range(times):
        p.append(mp.Process(target=fnc, args=(datas, lock)))

    # Start all the process
    for item in p:
        item.start()

    # Block
    for item in p:
        item.join()

    # The final result
    result = {'SPT': {}, 'ST': {}, 'WSPT': {}}

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
    BETA = 0.3
    ALPHA = 0.3

    spt = {}
    st = {}
    wspt = {}

    for multi_group_size in range(10, 60, 10):
        spt[multi_group_size] = 0
        st[multi_group_size] = 0
        wspt[multi_group_size] = 0

    g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

    for multi_group_size in range(10, 60, 10):
        flows = generate_flow_requests(g, 10, multi_group_size)

        graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
        spt[multi_group_size] += compute_num_branch_nodes(allocated_graph)

        graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
        st[multi_group_size] += compute_num_branch_nodes(allocated_graph)

        graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
        wspt[multi_group_size] += compute_num_branch_nodes(allocated_graph)

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st, 'WSPT': wspt})
    lock.release()


def lab_2(datas, lock):
    # Average rejection rate vs number of requests
    NETWORK_SIZE = 100
    BETA = 0.2
    ALPHA = 0.2

    spt = {}
    st = {}
    wspt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0

    g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

    for num_requests in range(10, 90, 10):
        flows = generate_flow_requests(g, num_requests, 30)

        graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
        spt[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
        st[num_requests] += compute_average_rejection_rate(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
        wspt[num_requests] += compute_average_rejection_rate(allocated_flows)

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st, 'WSPT': wspt})
    lock.release()


def lab_3(datas, lock):
    # Average network throughput vs number of requests
    NETWORK_SIZE = 100
    BETA = 0.2
    ALPHA = 0.2

    spt = {}
    st = {}
    wspt = {}

    for num_requests in range(10, 90, 10):
        spt[num_requests] = 0
        st[num_requests] = 0
        wspt[num_requests] = 0

    g, pos = generate_topology(NETWORK_SIZE, BETA, ALPHA)

    for num_requests in range(10, 90, 10):
        flows = generate_flow_requests(g, num_requests, 30)

        graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
        spt[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
        st[num_requests] += compute_throughput(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
        wspt[num_requests] += compute_throughput(allocated_flows)

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st, 'WSPT': wspt})
    lock.release()


def lab_4(datas, lock):
    # Average network throughput vs different network size
    BETA = 0.25
    ALPHA = 0.25

    spt = {}
    st = {}
    wspt = {}

    for network_size in range(100, 500, 100):
        spt[network_size] = 0
        st[network_size] = 0
        wspt[network_size] = 0

    for network_size in range(100, 500, 100):
        g, pos = generate_topology(network_size, BETA, ALPHA)

        flows = generate_flow_requests(g, 20, network_size // 4)

        graph, allocated_flows, allocated_graph = generate_shortest_path_tree(g, flows)
        spt[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_steiner_tree(g, flows)
        st[network_size] += compute_throughput(allocated_flows)

        graph, allocated_flows, allocated_graph = generate_widest_shortest_path_tree(g, flows)
        wspt[network_size] += compute_throughput(allocated_flows)

    lock.acquire()
    datas.append({'SPT': spt, 'ST': st, 'WSPT': wspt})
    lock.release()


if __name__ == '__main__':
    main()
