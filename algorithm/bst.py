"""
@project: RoutingAlgorithm
@author: sam
@file bst.py
@ide: PyCharm
@time: 2019-03-01 14:52:59
@blog: https://jiahaoplus.com
"""
from network import *
from copy import deepcopy

__all__ = [
    'generate_branch_aware_steiner_trees'
]


def generate_branch_aware_steiner_trees(G, flows):
    graph = deepcopy(G)
    allocated_flows = deepcopy(flows)

    branch_aware_steiner_trees = []


if __name__ == '__main__':
    pass
