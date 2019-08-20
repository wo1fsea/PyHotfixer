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
__skip_hotfix__ = True

import gc
import sys
import inspect
import importlib
import importlib.abc

OLD_MODULES = None
OLD_SYS_META_PATH = None


class HotfixerFinder(importlib.abc.MetaPathFinder):

	def find_module(self, fullname, path=None):
		print('find_module {}'.format(fullname))
		return MetaPathLoader()


class MetaPathLoader(importlib.abc.Loader):

	def load_module(self, fullname):
		print('load_module {}'.format(fullname))
		# ``sys.modules`` 中保存的是已经导入过的 module
		if fullname in sys.modules:
			return sys.modules[fullname]

		# 先从 sys.meta_path 中删除自定义的 finder
		# 防止下面执行 import_module 的时候再次触发此 finder
		# 从而出现递归调用的问题
		finder = sys.meta_path.pop(0)
		# 导入 module
		module = importlib.import_module(fullname)

		module_hook(fullname, module)

		sys.meta_path.insert(0, finder)
		return module


def load_module(self, fullname):
	print('load_module {}'.format(fullname))
	sys.modules[fullname] = sys
	return sys


def hotfix(module_names=[]):
	global OLD_MODULES
	global OLD_SYS_META_PATH

	gc.disable()

	OLD_MODULES = sys.modules.copy()
	OLD_SYS_META_PATH = sys.meta_path
	sys.meta_path = [HotfixerFinder()]

	gc.enable()
	gc.collect()


def hotfix_module(old_module, new_module):
	if is_skip_hotfix(new_module):
		return old_module

	hotfix_data_list = get_hotfix_data_list(new_module)
	hotfix_skip_list = get_hotfix_skip_list(new_module)

	for name, new_attr in inspect.getmembers(new_module):
		if name in hotfix_skip_list:
			if hasattr(old_module, name):
				old_attr = getattr(old_module, name, None)
				setattr(new_module, name, old_attr)
			else:
				delattr(new_module, name)
			continue

		if name in hotfix_data_list:
			continue

		if not hasattr(old_module, name):
			if isinstance(new_attr, type) and new_attr is not type or \
					inspect.isfunction(new_attr):
				continue
			else:
				delattr(new_module, name)

		if isinstance(new_attr, type) and new_attr is not type:
			if isinstance(old_attr, type) and old_attr is not type:
				setattr(new_module, name, hotfix_class(old_attr, new_attr))
		elif inspect.isfunction(new_attr):
			if inspect.isfunction(old_attr):
				setattr(new_module, name, hotfix_function(old_attr, new_module))

	return new_module


def hotfix_function(old_function, new_function):
	old_cell_num = len(old_function.__closure__) if old_function.__closure__ else 0
	new_cell_num = len(new_function.__closure__) if new_function.__closure__ else 0

	if old_cell_num != new_cell_num:
		return False

	setattr(old_function, '__code__', new_function.__code__)
	setattr(old_function, '__doc__', new_function.__doc__)
	setattr(old_function, '__dict__', new_function.__dict__)

	if new_function.__defaults__:
		new_defaults = tuple([hotfixed_obj(obj) for obj in new_function.__defaults__])
	else:
		new_defaults = ()

	setattr(old_function, '__defaults__', new_defaults)

	if old_cell_num:
		for index, old_cell in enumerate(old_function.__closure__):
			new_cell = new_function.__closure__[index].cell_contents
			if inspect.isfunction(old_cell.cell_contents) and inspect.isfunction(new_cell.cell_contents):
				hotfix_function(old_cell.cell_contents, new_cell.cell_contents)

	return True


def hotfixed_obj(obj):
	return obj

	new_class = getattr(obj, "__class__", None)

	if not new_class:
		return obj

	# Py_TPFLAGS_HEAPTYPE
	if not (getattr(new_class, "__flags__", 0) & 0x200):
		return obj

	old_infos = _module_infos.get(new_class.__module__)
	if not old_infos:
		return obj

	old_class = old_infos.get(new_class.__name__)
	if old_class:
		obj.__class__ = old_class

	return obj


def is_skip_hotfix(obj):
	return getattr(obj, "__skip_hotfix__", False)


def get_hotfix_data_list(obj):
	return getattr(obj, "__hotfix_data_list__", [])


def get_hotfix_skip_list(obj):
	skip_list = getattr(obj, "__hotfix_skip_list__", [])
	skip_list.extend(['__module__', '__dict__', '__weakref__'])
	return skip_list


def hotfix_class(old_class, new_class):
	# Py_TPFLAGS_HEAPTYPE
	if not (getattr(new_class, "__flags__", 0) & 0x200):
		return old_class

	if is_skip_hotfix(new_class):
		return old_class

	hotfix_data_list = get_hotfix_data_list(new_class)
	hotfix_skip_list = get_hotfix_skip_list(new_class)

	for name, old_attr in dict(old_class.__dict__.items()):
		if name not in new_class.__dict__:
			delattr(old_class, name)

	for name, new_attr in dict(new_class.__dict__.items()):
		if name in hotfix_skip_list:
			continue

		if name in hotfix_data_list:
			setattr(old_class, name, new_attr)
			continue

		old_attr = old_class.__dict__[name]

		if isinstance(new_attr, property):
			setattr(old_class, name, new_attr)

		elif isinstance(new_attr, staticmethod) or isinstance(new_attr, classmethod):
			if hasattr(old_attr, "__func__") and hasattr(new_attr, "__func__"):
				old_attr.__func__ = hotfix_function(old_attr.__func__, new_attr.__func__)
			else:
				setattr(old_class, name, new_attr)

		elif inspect.isfunction(new_attr):
			if inspect.isfunction(old_attr):
				setattr(old_class, name, hotfix_function(old_attr, new_attr))
			else:
				setattr(old_class, name, new_attr)

		elif inspect.isclass(new_attr):
			if new_attr.__name__ == old_attr.__name__:
				setattr(old_class, name, hotfix_class(old_attr, new_attr))
			else:
				setattr(old_class, name, new_attr)

# elif inspect.ismemberdescriptor(old_attr):
# 	pass
# elif inspect.ismemberdescriptor(new_attr):
# 	pass
# elif inspect.isgetsetdescriptor(new_attr):
# 	pass
