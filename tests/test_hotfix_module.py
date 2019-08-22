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
import os
import sys
import shutil

from pyhotfixer import hotfix

FILE_NAME = "module_test.py"
FILE_NAME_V1 = "module_test.v1.py"
FILE_NAME_V2 = "module_test.v2.py"


class HotfixModuleTestCase(unittest.TestCase):

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

        sys.modules.pop("module_test", None)
        import module_test

        obj = module_test.OBJECT_CREATED_WHEN_HOTFIXING
        obj_class = module_test.ObjCreatedWhenHotfixing
        hotfix_class = module_test.HotfixClass()
        self.assertEqual(hotfix_class.hotfix_method(), 1)
        print(id(obj.__class__))

        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["module_test"])

        print(id(module_test.OBJECT_CREATED_WHEN_HOTFIXING.__class__), id(obj.__class__))
        self.assertFalse(module_test.OBJECT_CREATED_WHEN_HOTFIXING is obj_class)
        self.assertTrue(isinstance(module_test.OBJECT_CREATED_WHEN_HOTFIXING, obj_class))

        self.assertEqual(hotfix_class.hotfix_method(), 2)

