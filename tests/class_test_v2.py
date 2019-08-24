from pyhotfixer import skip_hotfix


class HotfixClass(object):
    # data
    __hotfix_data_list__ = [
        "hotfix_data"
    ]

    hotfix_data = 2
    no_hotfix_data = 2

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

    @classmethod
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
    def no_hotfix_property(self):
        return 2

    @no_hotfix_property.setter
    def no_hotfix_property(self, value):
        pass

    @no_hotfix_property.deleter
    def no_hotfix_property(self):
        pass

    @skip_hotfix
    @property
    def skip_hotfix_decorator_in_wrong_position(self):
        return 2

    def replace_data_with_func(self):
        return 2

    @staticmethod
    def replace_data_with_static_method():
        return 2

    @classmethod
    def replace_data_with_class_method(cls):
        return 2

    class InnerClass1(object):
        @staticmethod
        def func():
            return 2

    class InnerClass2(object):
        @staticmethod
        def func():
            return 2

    InnerClass = InnerClass2


@skip_hotfix
class NoHotfixClass(object):
    no_hotfix_data = 2

    def no_hotfix_method(self):
        return 2

class AnotherNoHotfixClass(object):
    __skip_hotfix__ = True
    no_hotfix_data = 2

    def no_hotfix_method(self):
        return 2