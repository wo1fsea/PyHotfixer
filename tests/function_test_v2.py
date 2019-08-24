class ObjCreatedWhenHotfixing(object):
    pass


def hotfix_func_with_obj_default(obj=ObjCreatedWhenHotfixing()):
    return obj


def hotfix_func_with_closure1():
    def cell_func():
        return 2

    def closure_func():
        return cell_func()

    return closure_func


closure_func1 = hotfix_func_with_closure1()


def hotfix_func_with_closure2():
    def cell_func1():
        return 2

    def cell_func2():
        return 2

    def closure_func():
        return cell_func1() + cell_func2()

    return closure_func


closure_func2 = hotfix_func_with_closure2()
