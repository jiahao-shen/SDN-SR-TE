"""
@project: RoutingAlgorithm
@author: sam
@file test_utils.py
@ide: PyCharm
@time: 2019-03-04 17:57:41
@blog: https://jiahaoplus.com
"""
from network.utils import *
import random


def test_1():
    """Test the function draw_result
    :return:
    """
    def generate_test_result():
        result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}}

        for key in result:
            for index in range(10, 70, 10):
                result[key][index] = random.randint(10, 100)

        return result

    results = generate_test_result()
    draw_result(results, type='bar')
