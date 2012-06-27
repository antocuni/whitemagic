import types

def rebind_globals(func, newglobals=None):
    if newglobals is None:
        newglobals = globals()
    newfunc = types.FunctionType(func.func_code, newglobals, func.func_name,
                                 func.func_defaults)
    return newfunc


# stolen from pypy
class extendabletype(type):
    """A type with a syntax trick: 'class __extend__(t)' actually extends
    the definition of 't' instead of creating a new subclass."""
    def __new__(cls, name, bases, dict):
        if name == '__extend__':
            for cls in bases:
                for key, value in dict.items():
                    if key == '__module__':
                        continue
                    # XXX do we need to provide something more for pickling?
                    setattr(cls, key, value)
            return None
        else:
            return super(extendabletype, cls).__new__(cls, name, bases, dict)
