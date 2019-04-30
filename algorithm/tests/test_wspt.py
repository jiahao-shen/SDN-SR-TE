"""
@project: RoutingAlgorithm
@author: sam
@file test_wspt.py
@ide: PyCharm
@time: 2019-03-04 18:13:15
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.shortest_path_tree import *
from algorithm.widest_shortest_path_tree import *
import multiprocessing as mp


@count_time
def test_1():
    """Test Widest Shortest Path algorithm
    Start 4 processes, each process runs 1 << 12 times, each time randomly
    generates a network topology, then randomly generates one pair
    (source, destination), then compute the widest shortest path and all
    shortest paths from source to destination.
    Then, compare the minimum bandwidth of each path. If the minimum bandwidth
    of other paths is bigger than the widest shortest path, then raise error.
    :return:
    """
    def task():
        for _ in range(100):
            G = generate_topology()
            src, dst = random.sample(range(20), 2)

            all_widest_shortest_path = generate_widest_shortest_path(G, src)
            widest_shortest_path = all_widest_shortest_path[dst]
            all_shortest_path = nx.all_shortest_paths(G, src, dst, weight=None)

            for path in all_shortest_path:
                assert \
                    compute_path_minimum_bandwidth(G, widest_shortest_path) \
                    >= compute_path_minimum_bandwidth(G, path)

        print('Success')

    p = []

    for _ in range(4):
        p.append(mp.Process(target=task))

    for item in p:
        item.start()

    for item in p:
        item.join()


@count_time
def test_2():
    """Test no cycle in WSPT
    :return:
    """
    for _ in range(100):
        G = generate_topology()
        flows = generate_flow_requests(G, 10, 40)

        graph, allocated_flows, trees = generate_shortest_path_trees(G, flows)

        for T in trees:
            assert len(nx.cycle_basis(T)) == 0
