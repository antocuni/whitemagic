import py
import magic

def test_rebind_globals():
    def foo():
        return A
    py.test.raises(NameError, "foo()")
    foo2 = magic.rebind_globals(foo, {'A': 42})
    assert foo2() == 42
