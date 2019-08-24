# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong
    gzhuangquanyong@corp.netease.com
Date:
    2019/8/19
Description:
    test_skip_hotfix_module.py
----------------------------------------------------------------------------"""

import unittest
import os
import sys
import shutil

from pyhotfixer import hotfix

FILE_NAME = "module_skip_test.py"
FILE_NAME_V1 = "module_skip_test_v1.py"
FILE_NAME_V2 = "module_skip_test_v2.py"


class SkipHotfixModuleTestCase(unittest.TestCase):

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

    def test_skip_hotfix_module(self):
        shutil.copy(self.module_file_v1, self.module_file)

        sys.modules.pop("module_skip_test", None)
        import module_skip_test

        self.assertEqual(module_skip_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_skip_test.HOTFIX_DATA, 1)

        self.assertEqual(module_skip_test.no_hotfix_func(), 1)
        self.assertEqual(module_skip_test.hotfix_func(), 1)

        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["module_skip_test"])

        self.assertEqual(module_skip_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_skip_test.HOTFIX_DATA, 1)

        self.assertEqual(module_skip_test.no_hotfix_func(), 1)
        self.assertEqual(module_skip_test.hotfix_func(), 1)

