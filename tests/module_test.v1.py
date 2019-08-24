from pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "HOTFIX_DATA",
    "OBJECT_CREATE_WHEN_HOTFIXING"
]

HOTFIX_DATA = 1
NO_HOTFIX_DATA = 1


def hotfix_func():
    return 1


@skip_hotfix
def no_hotfix_func():
    return 1


class ObjCreatedWhenHotfixing(object):
    def func(self):
        return 1


OBJECT_CREATED_WHEN_HOTFIXING = ObjCreatedWhenHotfixing()
