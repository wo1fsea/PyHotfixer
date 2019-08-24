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
import traceback
from importlib.abc import SourceLoader
from importlib.machinery import FileFinder
from weakref import WeakSet

Py_TPFLAGS_HEAPTYPE = 0x200
OLD_MODULES = {}
BUILTINS_OBJ = object
NEW_OBJECTS = WeakSet()


class HotfixerObject(object):

    def __new__(cls):
        obj = BUILTINS_OBJ.__new__(cls)

        if cls.__module__ in OLD_MODULES:
            NEW_OBJECTS.add(obj)

        return obj


class MetaPathLoader(SourceLoader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path

    def get_filename(self, fullname):
        return self.path

    def get_data(self, filename):
        with open(filename) as f:
            data = f.read()
        return data

    def exec_module(self, module):
        super(MetaPathLoader, self).exec_module(module)

        old_module = OLD_MODULES.get(module.__name__)

        if old_module:
            hotfix_module(old_module, module)


def hotfix(module_names):
    global OLD_MODULES
    global BUILTINS_OBJ

    OLD_MODULES.clear()
    for name in module_names:
        if name in sys.modules:
            OLD_MODULES[name] = sys.modules[name]

    gc.disable()
    OLD_MODULES = sys.modules.copy()
    BUILTINS_OBJ = object
    sys.modules["builtins"].object = HotfixerObject

    sys.path_hooks.insert(0, FileFinder.path_hook((MetaPathLoader, [".py"])))
    # clear any loaders that might already be in use by the FileFinder
    sys.path_importer_cache.clear()
    importlib.invalidate_caches()

    for name in module_names:
        try:
            old_module = sys.modules.pop(name, None)
            new_module = importlib.import_module(name)
            if old_module and not is_skip_hotfix(new_module):
                for attr_name, new_attr in inspect.getmembers(new_module):
                    setattr(old_module, attr_name, new_attr)
        except Exception as ex:
            traceback.print_exc()
        finally:
            if name in OLD_MODULES:
                sys.modules[name] = OLD_MODULES[name]

    sys.path_hooks.pop(0)
    sys.modules["builtins"].object = BUILTINS_OBJ
    BUILTINS_OBJ = None

    for obj in NEW_OBJECTS:
        hotfix_obj(obj)

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
            if isinstance(new_attr, type) and new_attr is not type or inspect.isfunction(new_attr):
                continue
            else:
                delattr(new_module, name)
                continue

        old_attr = getattr(old_module, name, None)

        if isinstance(new_attr, type) and new_attr is not type:
            if isinstance(old_attr, type) and old_attr is not type:
                setattr(new_module, name, hotfix_class(old_attr, new_attr))
        elif inspect.isfunction(new_attr):
            if inspect.isfunction(old_attr):
                setattr(new_module, name, hotfix_function(old_attr, new_attr))
        else:
            setattr(new_module, name, old_attr)

    return new_module


def hotfix_function(old_function, new_function):
    old_cell_num = len(old_function.__closure__) if old_function.__closure__ else 0
    new_cell_num = len(new_function.__closure__) if new_function.__closure__ else 0

    if old_cell_num != new_cell_num:
        return new_function

    setattr(old_function, '__code__', new_function.__code__)
    setattr(old_function, '__doc__', new_function.__doc__)
    setattr(old_function, '__dict__', new_function.__dict__)
    setattr(old_function, '__defaults__', new_function.__defaults__)

    if old_cell_num:
        for index, old_cell in enumerate(old_function.__closure__):
            new_cell = new_function.__closure__[index]
            if inspect.isfunction(old_cell.cell_contents) and inspect.isfunction(new_cell.cell_contents):
                hotfix_function(old_cell.cell_contents, new_cell.cell_contents)

    return old_function


def hotfix_obj(obj):
    new_class = getattr(obj, "__class__", None)

    if not new_class:
        return obj

    if not (getattr(new_class, "__flags__", 0) & Py_TPFLAGS_HEAPTYPE):
        return obj

    module_name = new_class.__module__

    module = OLD_MODULES.get(module_name)
    if not module:
        return obj

    class_name = new_class.__name__
    old_class = getattr(module, class_name)
    if old_class:
        obj.__class__ = old_class

    return obj


def hotfix_class(old_class, new_class):
    if not (getattr(new_class, "__flags__", 0) & Py_TPFLAGS_HEAPTYPE):
        return old_class

    if is_skip_hotfix(new_class):
        return old_class

    hotfix_data_list = get_hotfix_data_list(new_class)
    hotfix_skip_list = get_hotfix_skip_list(new_class)

    for name, old_attr in dict(old_class.__dict__).items():
        if name not in hotfix_skip_list and name not in new_class.__dict__:
            delattr(old_class, name)

    for name, new_attr in dict(new_class.__dict__).items():
        if name in hotfix_skip_list:
            continue

        if name in hotfix_data_list:
            setattr(old_class, name, new_attr)
            continue

        if name not in old_class.__dict__:
            if (
                    isinstance(new_attr, property) or
                    isinstance(new_attr, staticmethod) or
                    isinstance(new_attr, classmethod) or
                    inspect.isfunction(new_attr) or
                    inspect.isclass(new_attr) or
                    inspect.isclass(old_attr) or
                    inspect.ismemberdescriptor(new_attr) or
                    inspect.isgetsetdescriptor(new_attr)
            ):
                setattr(old_class, name, new_attr)
            continue

        old_attr = old_class.__dict__[name]

        if isinstance(new_attr, property):
            setattr(old_class, name, new_attr)

        elif isinstance(new_attr, staticmethod) or isinstance(new_attr, classmethod):
            if (
                    hasattr(old_attr, "__func__") and hasattr(new_attr, "__func__") and
                    hotfix_function(old_attr.__func__, new_attr.__func__) is old_attr.__func__
            ):
                pass
            else:
                setattr(old_class, name, new_attr)

        elif inspect.isfunction(new_attr):
            if inspect.isfunction(old_attr):
                setattr(old_class, name, hotfix_function(old_attr, new_attr))
            else:
                setattr(old_class, name, new_attr)

        elif inspect.isclass(new_attr):
            if inspect.isclass(old_attr) and new_attr.__name__ == old_attr.__name__:
                setattr(old_class, name, hotfix_class(old_attr, new_attr))
            else:
                setattr(old_class, name, new_attr)
        elif inspect.ismemberdescriptor(new_attr):
            setattr(old_class, name, new_attr)
        elif inspect.isgetsetdescriptor(new_attr):
            setattr(old_class, name, new_attr)

    return old_class


def is_skip_hotfix(obj):
    return getattr(obj, "__skip_hotfix__", False)


def get_hotfix_data_list(obj):
    return getattr(obj, "__hotfix_data_list__", [])


def get_hotfix_skip_list(obj):
    skip_list = getattr(obj, "__hotfix_skip_list__", [])
    skip_list.extend(['__module__', '__dict__', '__weakref__', '__dict__', '__dir__'])
    return skip_list


def skip_hotfix(obj):
    if inspect.isfunction(obj):
        frame = inspect.currentframe()
        method_name = obj.__code__.co_name
        hotfix_skip_list = frame.f_back.f_locals.setdefault("__hotfix_skip_list__", [])
        hotfix_skip_list.append(method_name)
    elif inspect.isclass(obj):
        frame = inspect.currentframe()
        hotfix_skip_list = frame.f_back.f_locals.setdefault("__hotfix_skip_list__", [])
        hotfix_skip_list.append(obj.__name__)
    else:
        print("@skip_hotfix should only be used to dedicate functions or classes.")

    return obj
