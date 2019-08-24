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

        self.assertEqual(module_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_test.HOTFIX_DATA, 1)

        self.assertEqual(module_test.no_hotfix_func(), 1)
        self.assertEqual(module_test.hotfix_func(), 1)

        self.assertFalse(hasattr(module_test, "new_func"))
        self.assertFalse(hasattr(module_test, "new_func_and_skip"))

        self.assertFalse(hasattr(module_test, "NEW_DATA"))
        self.assertFalse(hasattr(module_test, "NEW_HOTFIX_DATA"))

        obj_id = id(module_test.OBJECT_CREATED_WHEN_HOTFIXING)

        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["module_test"])

        self.assertEqual(module_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_test.HOTFIX_DATA, 2)

        self.assertEqual(module_test.no_hotfix_func(), 1)
        self.assertEqual(module_test.hotfix_func(), 2)

        self.assertEqual(module_test.new_func(), 2)
        self.assertFalse(hasattr(module_test, "new_func_and_skip"))

        self.assertFalse(hasattr(module_test, "NEW_DATA"))
        self.assertEqual(module_test.NEW_HOTFIX_DATA, 2)

        self.assertEqual(obj_id, id(module_test.OBJECT_CREATED_WHEN_HOTFIXING))

    def test_hotfix_module_exception(self):
        shutil.copy(self.module_file_v1, self.module_file)

        sys.modules.pop("module_test", None)
        import module_test

        self.assertEqual(module_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_test.HOTFIX_DATA, 1)

        self.assertEqual(module_test.no_hotfix_func(), 1)
        self.assertEqual(module_test.hotfix_func(), 1)

        self.assertFalse(hasattr(module_test, "new_func"))
        self.assertFalse(hasattr(module_test, "new_func_and_skip"))

        self.assertFalse(hasattr(module_test, "NEW_DATA"))
        self.assertFalse(hasattr(module_test, "NEW_HOTFIX_DATA"))

        self.assertEqual(module_test.OBJECT_CREATED_WHEN_HOTFIXING.func(), 1)
        obj_id = id(module_test.OBJECT_CREATED_WHEN_HOTFIXING)

        shutil.copy(self.module_file_v2, self.module_file)
        hotfix(["module_exception_test", "module_test"])

        self.assertEqual(module_test.NO_HOTFIX_DATA, 1)
        self.assertEqual(module_test.HOTFIX_DATA, 2)

        self.assertEqual(module_test.no_hotfix_func(), 1)
        self.assertEqual(module_test.hotfix_func(), 2)

        self.assertEqual(module_test.new_func(), 2)
        self.assertFalse(hasattr(module_test, "new_func_and_skip"))

        self.assertFalse(hasattr(module_test, "NEW_DATA"))
        self.assertEqual(module_test.NEW_HOTFIX_DATA, 2)

        self.assertEqual(module_test.OBJECT_CREATED_WHEN_HOTFIXING.func(), 2)
        self.assertEqual(obj_id, id(module_test.OBJECT_CREATED_WHEN_HOTFIXING))
