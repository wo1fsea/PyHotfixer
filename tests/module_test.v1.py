from pyhotfixer.pyhotfixer import skip_hotfix

__skip_hotfix__ = False
__hotfix_data_list__ = [

]



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
        return 1

    @hotfix_property.setter
    def hotfix_property(self, value):
        pass

    @hotfix_property.deleter
    def hotfix_property(self):
        pass

    @property
    @skip_hotfix
    def not_hotfix_property(self):
        return 1

    @not_hotfix_property.setter
    def not_hotfix_property(self, value):
        pass

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
