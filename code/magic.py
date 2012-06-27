import types

# stole from pdb++
def rebind_globals(func, newglobals=None):
    if newglobals is None:
        newglobals = globals()
    newfunc = types.FunctionType(func.func_code, newglobals, func.func_name,
                                 func.func_defaults)
    return newfunc


# stolen from pypy
class extendabletype(type):
    def __new__(cls, name, bases, dict):
        if name == '__extend__':
            for cls in bases:
                for key, value in dict.items():
                    if key == '__module__':
                        continue
                    setattr(cls, key, value)
            return None
        else:
            return type.__new__(cls, name, bases, dict)


# stolen from "bruzzone spedizioni"
def attach_to(obj):
    def attach(cls):
        name = cls.__name__
        setattr(obj, name, cls)
    return attach

