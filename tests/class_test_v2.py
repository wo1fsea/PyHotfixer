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
class NoHotfixClass(object):
    no_hotfix_data = 2

    def no_hotfix_method(self):
        return 2
