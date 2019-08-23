from pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "HOTFIX_DATA",
    "OBJECT_CREATE_WHEN_HOTFIXING"
]

HOTFIX_DATA = 2
NO_HOTFIX_DATA = 2


def hotfix_func():
    return 2


@skip_hotfix
def no_hotfix_func():
    return 2


class ObjCreatedWhenHotfixing(object):
    data = 2


OBJECT_CREATED_WHEN_HOTFIXING = ObjCreatedWhenHotfixing()


def hotfix_func_with_obj_default(obj=ObjCreatedWhenHotfixing()):
    return obj


def hotfix_func_with_closure():
    def cell_func():
        return 2

    def closure_func():
        return cell_func()

    return closure_func


func = hotfix_func_with_closure()
