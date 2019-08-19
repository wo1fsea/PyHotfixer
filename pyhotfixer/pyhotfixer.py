# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong
    gzhuangquanyong@corp.netease.com
Date:
    2019/8/19
Description:
    pyhotfixer.py
----------------------------------------------------------------------------"""

import gc
import sys
import importlib

class MetaPathFinder(importlib.abc.MetaPathFinder):
	def find_spec(self, fullname, path, target=None):
		pass

	def

def hotfix(module_names=[]):
	gc.disable()

	old_sys_meta_path = sys.meta_path
	sys.meta_path = [builtin_finder()]

	gc.enable()
