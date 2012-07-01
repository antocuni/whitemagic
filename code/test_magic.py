import py
import magic

def test_rebind_globals():
    def foo():
        return A
    py.test.raises(NameError, "foo()")
    foo2 = magic.rebind_globals(foo, {'A': 42})
    assert foo2() == 42


def test_extendabletype():
    class A:
        __metaclass__ = magic.extendabletype
    class __extend__(A):
        foo = 42
    #
    assert __extend__ is None
    assert A.foo == 42
    class B:
        pass
    class __extend__(A, B):
        bar = 43
    assert A.bar == B.bar == 43
