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

FILE_NAME = "class_test.py"
FILE_NAME_V1 = "class_test_v1.py"
FILE_NAME_V2 = "class_test_v2.py"


class HotfixClassTestCase(unittest.TestCase):

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

    def test_hotfix_module(self):
        shutil.copy(self.module_file_v1, self.module_file)
        sys.modules.pop("class_test", None)

        import class_test

        hotfix_class_obj = class_test.HotfixClass()
        self.assertEqual(hotfix_class_obj.no_hotfix_data, 1)
        self.assertEqual(hotfix_class_obj.hotfix_data, 1)

        self.assertEqual(hotfix_class_obj.no_hotfix_method(), 1)
        self.assertEqual(hotfix_class_obj.hotfix_method(), 1)

        self.assertEqual(hotfix_class_obj.no_hotfix_classmethod(), 1)
        self.assertEqual(hotfix_class_obj.hotfix_classmethod(), 1)

        self.assertEqual(hotfix_class_obj.hotfix_property, 1)
        self.assertEqual(hotfix_class_obj.no_hotfix_property, 1)


        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["class_test"])

        self.assertEqual(hotfix_class_obj.no_hotfix_data, 1)
        self.assertEqual(hotfix_class_obj.hotfix_data, 2)

        self.assertEqual(hotfix_class_obj.no_hotfix_method(), 1)
        self.assertEqual(hotfix_class_obj.hotfix_method(), 2)

        self.assertEqual(hotfix_class_obj.no_hotfix_classmethod(), 1)
        self.assertEqual(hotfix_class_obj.hotfix_classmethod(), 2)

        self.assertEqual(hotfix_class_obj.no_hotfix_property, 1)
        self.assertEqual(hotfix_class_obj.hotfix_property, 2)
