from pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "HOTFIX_DATA",
    "OBJECT_CREATE_WHEN_HOTFIXING",
    "HOTFIX_CLASS_REF",
]

HOTFIX_DATA = 1
NO_HOTFIX_DATA = 1


def hotfix_func():
    return 1


@skip_hotfix
def no_hotfix_func():
    return 1


class ObjCreatedWhenHotfixing(object):
    @staticmethod
    def func():
        return 1


OBJECT_CREATED_WHEN_HOTFIXING = ObjCreatedWhenHotfixing()


class HotfixClass(object):
    @staticmethod
    def func():
        return 1


HOTFIX_CLASS_REF = HotfixClass

