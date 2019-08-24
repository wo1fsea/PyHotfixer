__skip_hotfix__ = True

from pyhotfixer import skip_hotfix

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

