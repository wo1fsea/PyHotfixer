from pyhotfixer import skip_hotfix


class HotfixClass(object):
    # data
    __hotfix_data_list__ = [
        "hotfix_data"
    ]

    hotfix_data = 1
    no_hotfix_data = 1

    # method
    def hotfix_method(self):
        return 1

    @skip_hotfix
    def no_hotfix_method(self):
        return 1

    # staticmethod
    @staticmethod
    def hotfix_staticmethod():
        return 1

    @staticmethod
    @skip_hotfix
    def no_hotfix_staticmethod():
        return 1

    # classmethod
    @classmethod
    def hotfix_classmethod(cls):
        return 1

    @classmethod
    @skip_hotfix
    def no_hotfix_classmethod(cls):
        return 1

    # property
    @property
    def hotfix_property(self):
        return 1

    @hotfix_property.setter
    def hotfix_property(self, value):
        pass

    @hotfix_property.deleter
    def hotfix_property(self):
        pass

    @property
    @skip_hotfix
    def no_hotfix_property(self):
        return 1

    @no_hotfix_property.setter
    def no_hotfix_property(self, value):
        pass

    @no_hotfix_property.deleter
    def not_hotfix_property(self):
        pass


@skip_hotfix
class NoHotfixClass(object):
    no_hotfix_data = 1

    def no_hotfix_method(self):
        return 1
