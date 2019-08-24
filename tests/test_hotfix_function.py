# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong
    gzhuangquanyong@corp.netease.com
Date:
    2019/8/19
Description:
    test_hotfix_class.py
----------------------------------------------------------------------------"""

import unittest
import os
import sys
import shutil

from pyhotfixer import hotfix

FILE_NAME = "function_test.py"
FILE_NAME_V1 = "function_test_v1.py"
FILE_NAME_V2 = "function_test_v2.py"


class HotfixFunctionTestCase(unittest.TestCase):

    def setUp(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.module_file = os.path.join(cur_dir, FILE_NAME)
        self.module_file_v1 = os.path.join(cur_dir, FILE_NAME_V1)
        self.module_file_v2 = os.path.join(cur_dir, FILE_NAME_V2)
        if os.path.exists(self.module_file):
            os.remove(self.module_file)

    def tearDown(self):
        if os.path.exists(self.module_file):
            os.remove(self.module_file)

    def test_hotfix_function(self):
        shutil.copy(self.module_file_v1, self.module_file)
        sys.modules.pop("function_test", None)

        import function_test

        obj_default1 = function_test.hotfix_func_with_obj_default()
        self.assertEqual(function_test.closure_func1(), 1)
        self.assertEqual(function_test.closure_func2(), 1)

        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["function_test"])

        obj_default2 = function_test.hotfix_func_with_obj_default()
        self.assertEqual(function_test.closure_func1(), 2)
        self.assertEqual(function_test.closure_func2(), 4)

        self.assertEqual(obj_default1.__class__,  obj_default2.__class__)

