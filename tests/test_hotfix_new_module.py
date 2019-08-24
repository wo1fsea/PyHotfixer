# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong
    gzhuangquanyong@corp.netease.com
Date:
    2019/8/19
Description:
    test_hotfix_module.py
----------------------------------------------------------------------------"""

import unittest
import sys

from pyhotfixer import hotfix


class HotfixNewModuleTestCase(unittest.TestCase):

    def test_hotfix_new_module(self):
        hotfix(["new_module_test"])
        self.assertEqual(sys.modules["new_module_test"].data, 1)
