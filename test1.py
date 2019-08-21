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

class arg(object):
    __hotfix_data_list__ = ["a"]
    a = 101111111

class A(object):
    __skip_hotfix__ = False
    __hotfix_skip_list__ = []
    __hotfix_data_list__ = ["a"]
    a = 2

    def __init__(self):
        a = 100000
        self.method2 = lambda: a

    def method(self, a, b, c=arg()):
        print(isinstance(c, arg))
        print("id", id(c.__class__))
        return c.a


