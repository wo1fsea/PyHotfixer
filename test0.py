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
import time
import test1
import pyhotfixer.pyhotfixer

test1.func()
a = test1.func
func1 = test1.func
func1()
func2 = test1.func_skip
func2()
a = test1.A()
print(a.method.__code__)
print(a.method(1, 2))
print(a.a)
print("f", a.method2())
time.sleep(1)
pyhotfixer.pyhotfixer.hotfix(["test1"])
print("f", a.method2())
print(a.method.__code__)
print(dir(a.method))
print(a.method(1, 2))
print(a.a)
