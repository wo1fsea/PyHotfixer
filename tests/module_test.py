__skip_hotfix__ = False
__hotfix_data_list__ = [

]
__hotfix_skip_list__ = [

]


def skip_hotfix(cls):
    return cls


class HotfixClass(object):
    hotfix_class_data = 1
    no_hotfix_class_data = 1

    def hotfix_method(self):
        return 1

    @skip_hotfix
    def no_hotfix_method(self):
        return 1

    @property
    def hotfix_property(self):
        return

    @hotfix_property.setter
    def hotfix_property(self, value):
        pass

    @hotfix_property.deleter
    def hotfix_property(self):
        pass

    @skip_hotfix
    @property
    def not_hotfix_property(self):
        return

    @skip_hotfix
    @not_hotfix_property.setter
    def not_hotfix_property(self, value):
        pass

    @skip_hotfix
    @not_hotfix_property.deleter
    def not_hotfix_property(self):
        pass

    __hotfix_data_list__ = [
        "hotfix_class_data"
    ]


@skip_hotfix
class NoHotfixClass(object):
    no_hotfix_class_data = 1

    def no_hotfix_method(self):
        return 1
