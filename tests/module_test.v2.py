from pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "HOTFIX_DATA",
    "NEW_HOTFIX_DATA",
    "OBJECT_CREATE_WHEN_HOTFIXING"
]

HOTFIX_DATA = 2
NO_HOTFIX_DATA = 2


def hotfix_func():
    return 2


@skip_hotfix
def no_hotfix_func():
    return 2


@skip_hotfix
def new_func_and_skip():
    return 2


def new_func():
    return 2


NEW_DATA = 2
NEW_HOTFIX_DATA = 2


class ObjCreatedWhenHotfixing(object):
    def func(self):
        return 2


OBJECT_CREATED_WHEN_HOTFIXING = ObjCreatedWhenHotfixing()
