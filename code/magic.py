import types

# stole from pdb++
def rebind_globals(func, newglobals=None):
    """
    Clone the function object ``func`` and create another one, but with a
    different ``func_globals``.

    The returned function behaves as ``func`` but it will lookup its global
    variables in the given dictionary.
    """    
    if newglobals is None:
        newglobals = globals()
    newfunc = types.FunctionType(func.func_code, newglobals, func.func_name,
                                 func.func_defaults)
    return newfunc


# stolen from pypy
class extendabletype(type):
    """
    Enable the ``__extend__`` pattern.

    Classes whose metaclass is ``extendabletype`` can be extended by doing this::

        class __extend__(MyClass):
            foo = 42

    attributes and methods defined inside the ``__extend__`` class will be
    attached directly to ``MyClass`` (given that ``type(MyClass) is
    extendabletype``).
    """
    
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
    """
    Return a class decorator which attaches the given class to ``obj``.
    """
    
    def attach(cls):
        name = cls.__name__
        setattr(obj, name, cls)
    return attach



# =============================
# Database
# =============================

import py
import new
import sys
import sqlalchemy
import elixir

class Database(object):

    def __init__(self, url, modelfile, echo=False):
        self.url = url
        self.session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())
        self.metadata = sqlalchemy.MetaData(bind=url)
        self.collection = elixir.GlobalEntityCollection()
        self.metadata.bind.echo = echo
        self.import_model(modelfile)
        elixir.setup_entities(self.collection)

    def import_model(self, filename):
        # a bit of black magic: we cannot use a plain "import", because we
        # want the global __session__ and __metadata__ variables defined.
        # Instead, we simulate step-by-step what Python does when importing
        # the module:
        #
        # 1. create the module object
        self.model = new.module('model')
        self.model.__file__ = filename
        # 2. put the module in sys.modules (elixir's relies on it :-()
        assert 'model' not in sys.modules
        sys.modules['model'] = self.model
        try:
            # 3. compile and execute the code (after setting the desired globals)
            src = py.code.Source(py.path.local(filename).read())
            code = src.compile(filename=filename)
            self.model.__session__ = self.session
            self.model.__metadata__ = self.metadata
            self.model.__collection__ = self.collection
            exec code in self.model.__dict__
            del self.model.__session__
            del self.model.__metadata__
            del self.model.__collection__
        finally:
            # 4. remove it from sys.module (well, Python doesn't do it usually :-))
            del sys.modules['model']

    def create_all(self, *args, **kwds):
        self.metadata.create_all(*args, **kwds)

    def commit(self):
        self.session.commit()

    
