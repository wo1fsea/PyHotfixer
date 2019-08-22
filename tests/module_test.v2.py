from pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [
    "HOTFIX_DATA",
    "OBJECT_CREATE_WHEN_HOTFIXING"
]

HOTFIX_DATA = 2
NO_HOTFIX_DATA = 2


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


def hotfix_func():
    return 2


@skip_hotfix
def no_hotfix_func():
    return 2


class HotfixClass(object):
    # data
    __hotfix_data_list__ = [
        "hotfix_class_data"
    ]

    hotfix_class_data = 2
    no_hotfix_class_data = 2

    # method
    def hotfix_method(self):
        return 2

    @skip_hotfix
    def no_hotfix_method(self):
        return 2

    # staticmethod
    @staticmethod
    def hotfix_staticmethod():
        return 2

    @staticmethod
    @skip_hotfix
    def no_hotfix_staticmethod():
        return 2

    # classmethod
    @classmethod
    def hotfix_classmethod(cls):
        return 2

    @staticmethod
    @skip_hotfix
    def no_hotfix_classmethod(cls):
        return 2

    # property
    @property
    def hotfix_property(self):
        return 2

    @hotfix_property.setter
    def hotfix_property(self, value):
        pass

    @hotfix_property.deleter
    def hotfix_property(self):
        pass

    @property
    @skip_hotfix
    def not_hotfix_property(self):
        return 2

    @not_hotfix_property.setter
    def not_hotfix_property(self, value):
        pass

    @not_hotfix_property.deleter
    def not_hotfix_property(self):
        pass

    # inner class
    class HotfixInnerClass(object):
        def hotfix_method(self):
            return 2

    @skip_hotfix
    class NoHotfixInnerClass(object):
        def hotfix_method(self):
            return 2


@skip_hotfix
class NoHotfixClass(object):
    no_hotfix_class_data = 2

    def no_hotfix_method(self):
        return 2
