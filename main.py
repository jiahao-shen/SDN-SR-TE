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

    G = NetworkTopo()

    for multi_group_size in trange(10, 60, 10, desc='Lab 1'):
        flows = MulticastFlows(G, 20, multi_group_size, 10, 300)

        res1 = ShortestPathTree(G, flows)
        performance = res1.network_performance()
        spt[multi_group_size] = [spt[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        res2 = SteinerTree(G, flows)
        performance = res2.network_performance()
        st[multi_group_size] = [st[multi_group_size][i] + performance[i] for i
                                in range(len(PERFORMANCE))]

        res3 = WidestShortestPathTree(G, flows)
        performance = res3.network_performance()
        wspt[multi_group_size] = [wspt[multi_group_size][i] + performance[i]
                                  for i in range(len(PERFORMANCE))]

        res4 = WidestSteinerTree(G, flows)
        performance = res4.network_performance()
        wst[multi_group_size] = [wst[multi_group_size][i] + performance[i] for
                                 i in range(len(PERFORMANCE))]

        res5 = BranchawareSteinerTree(G, flows, w=5)
        performance = res5.network_performance()
        bst[multi_group_size] = [bst[multi_group_size][i] + performance[i]
                                 for i in range(len(PERFORMANCE))]

        res6 = BandwidthefficientBranchawareSegmentRoutingTree(G, flows, k=5,
                                                               alpha=0.5,
                                                               beta=0.5,
                                                               w1=1, w2=5)
        performance = res6.network_performance()
        bbsrt[multi_group_size] = [bbsrt[multi_group_size][i] + performance[i]
                                   for i in range(len(PERFORMANCE))]

        res7 = BandwidthefficientBranchawareSteinerTree(G, flows,
                                                        alpha=0.5, beta=0.5,
                                                        w1=1, w2=5)
        performance = res7.network_performance()
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

    G = NetworkTopo()

    for num_requests in trange(10, 80, 10, desc='Lab 2'):
        flows = MulticastFlows(G, num_requests, 10, 10, 300)

        res1 = ShortestPathTree(G, flows)
        performance = res1.network_performance()
        spt[num_requests] = [spt[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res2 = SteinerTree(G, flows)
        performance = res2.network_performance()
        st[num_requests] = [st[num_requests][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        res3 = WidestShortestPathTree(G, flows)
        performance = res3.network_performance()
        wspt[num_requests] = [wspt[num_requests][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        res4 = WidestSteinerTree(G, flows)
        performance = res4.network_performance()
        wst[num_requests] = [wst[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res5 = BranchawareSteinerTree(G, flows, w=5)
        performance = res5.network_performance()
        bst[num_requests] = [bst[num_requests][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res6 = BandwidthefficientBranchawareSegmentRoutingTree(G, flows, k=5,
                                                               alpha=0.5, beta=0.5,
                                                               w1=1, w2=5)
        performance = res6.network_performance()
        bbsrt[num_requests] = [bbsrt[num_requests][i] + performance[i] for i in
                               range(len(PERFORMANCE))]

        res7 = BandwidthefficientBranchawareSteinerTree(G, flows,
                                                        alpha=0.5, beta=0.5,
                                                        w1=1, w2=5)
        performance = res7.network_performance()
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
        G = NetworkTopo(size=network_size)
        flows = MulticastFlows(G, network_size // 10,
                               network_size // 10, 100, 1000)

        res1 = ShortestPathTree(G, flows)
        performance = res1.network_performance()
        spt[network_size] = [spt[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res2 = SteinerTree(G, flows)
        performance = res2.network_performance()
        st[network_size] = [st[network_size][i] + performance[i] for i in
                            range(len(PERFORMANCE))]

        res3 = WidestShortestPathTree(G, flows)
        performance = res3.network_performance()
        wspt[network_size] = [wspt[network_size][i] + performance[i] for i in
                              range(len(PERFORMANCE))]

        res4 = WidestSteinerTree(G, flows)
        performance = res4.network_performance()
        wst[network_size] = [wst[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res5 = BranchawareSteinerTree(G, flows, w=5)
        performance = res5.network_performance()
        bst[network_size] = [bst[network_size][i] + performance[i] for i in
                             range(len(PERFORMANCE))]

        res6 = BandwidthefficientBranchawareSegmentRoutingTree(G, flows, k=5,
                                                               alpha=0.5, beta=0.5,
                                                               w1=1, w2=5)
        performance = res6.network_performance()
        bbsrt[network_size] = [bbsrt[network_size][i] + performance[i] for i in
                               range(len(PERFORMANCE))]

        res7 = BandwidthefficientBranchawareSteinerTree(G, flows,
                                                        alpha=0.5, beta=0.5,
                                                        w1=1, w2=5)
        performance = res7.network_performance()
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
