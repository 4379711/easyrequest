# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 16:47
# @Author  : Liu Yalong
# @File    : __init__.py.py


def average_number_of_groups(m, n):
    """
    把一个数据分割为近似大小的N份

    :param m: 待分割的数据总长度
    :param n: 需要分为几份
    :return: 返回列表,代表应该分割的下标+1
    """

    base_num = m // n
    over_num = m % n

    result = [base_num for _ in range(n)]

    for i in range(over_num):
        result[i] = result[i] + 1

    for i in range(n - 1):
        result[i + 1] = result[i] + result[i + 1]

    return result


def split_urls_by_group(urls, n):
    aa = average_number_of_groups(len(urls), n)

    for i in range(len(aa)):
        if i == 0:
            yield (urls[:aa[i]])
        else:
            yield (urls[aa[i - 1]:aa[i]])
