# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2019/7/31
Description:
    test.py
----------------------------------------------------------------------------"""

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "data"
]
__hotfix_skip_list__ = [
    "func_skip"
]

data = 1
data_skip = 1


def func():
    return 1


def func_skip():
    return 1


class A(object):
    def method(self, a, b):
        return a - b
