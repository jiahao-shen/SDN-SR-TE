"""
@project: RoutingAlgorithm
@author: sam
@file test_topology.py
@ide: PyCharm
@time: 2019-03-04 17:57:27
@blog: https://jiahaoplus.com
"""
from network import *


def test_1():
    """Test function generate_topology, generate_flow_requests
    :return:
    """
    for _ in range(100):
        G = generate_topology(100)
        flows = generate_flow_requests(G)

        output_flows(flows)


def test_2():
    """Test the function load_topology_zoo
    :return:
    """
    G = load_topology_zoo()
    pos = graphviz_layout(G)
    draw_topology(G, pos)
