.. include:: beamerdefs.txt

================================
Python White Magic
================================

About me
=========

- PyPy core dev

- PyPy py3k tech leader

- ``pdb++``, ``fancycompleter``, ...

- Consultant, trainer

- http://antocuni.eu


About this talk (1)
====================

- a collection of hacks :-)

|pause|

**HOWEVER**

- real-life problems

- real-life solutions

- they improve the rest of the code

- (you might not like them)

About this talk (2)
====================

- Learn about internals and/or advanced Python

  * function and code objects

  * bytecode

  * metaclasses

  * decorators

  * import logic



Python
======

- Powerful language

- Surface of simplicity

- "just works" (TM) as expected

|pause|

- simplicity is an emergent property

- lots of internal rules and layers

- (ab)use them

  * "black magic"


"Black" magic
==============

- harder to read

- harder to maintain

- might break unexpectedly

- might rely on implementation details

- ...


What is magic?
==============

   `Any sufficiently advanced technology is indistinguishable from magic`

   (Arthur C. Clarke)

.. raw:: latex

   \vspace{0.5cm}

|column1|

.. image:: blank.png
   :scale: 40%
   :align: center

|column2|

.. image:: blank.png
   :scale: 40%
   :align: left

|end_columns|

What is magic?
==============

   `Any sufficiently advanced technology is indistinguishable from magic`

   (Arthur C. Clarke)

.. raw:: latex

   \vspace{0.5cm}

|column1|

.. image:: wizard.png
   :scale: 40%
   :align: center

|column2|

.. image:: blank.png
   :scale: 40%
   :align: left

|end_columns|

What is magic?
==============

   `Any sufficiently advanced technology is indistinguishable from magic`

   (Arthur C. Clarke)

.. raw:: latex

   \vspace{0.5cm}

|column1|

.. image:: wizard.png
   :scale: 40%
   :align: center

|column2|

.. image:: programmer.png
   :scale: 40%
   :align: left

|end_columns|


White magic
===========

- Still magic

- can help to have better code

  * more readable

  * more maintainable


- however:

  * lots of cons

  * some pros

- solid understanding of concepts is needed

- use with care


Problem #1: extending pdb.py (1)
================================

- pdb++: drop-in replacement for pdb.py

- keep the same API

- how extend a module?

- subclassing is not enouogh

- module-level functions?


Problem #1: extending pdb.py (2)
=================================

|scriptsize|
|column1|
|example<| |small| pdb.py |end_small| |>|

.. sourcecode:: python

   ...
   class Pdb(bdb.Bdb, cmd.Cmd):
       ...

   def set_trace():
       Pdb().set_trace(...)

   def main():
       ...
       pdb = Pdb()
       pdb._runscript(...)
       ...

|end_example|
|column2|

|example<| |small| pdbpp.py |end_small| |>|

.. sourcecode:: python

   import pdb
   class Pdb(pdb.Pdb):
       ...

|pause|

.. sourcecode:: python


   def set_trace():
       pdb.set_trace() # ???

   def main():
       pdb.main()      # ???


   ...

|end_example|
|end_columns|
|end_scriptsize|


Problem #1: extending pdb.py (3)
================================

- Logic inside ``set_trace`` and ``main`` (and others)

- ``Pdb()`` refers to ``pdb.Pdb()``

- our new class is never instantiated

- copy&paste is not a solution :-)


Spell #1: ``rebind_globals`` (1)
=================================


|scriptsize|
|example<| |small| python |end_small| |>|

.. sourcecode:: python

    >>> A = 'hello'
    >>> def foo():
    ...     print A
    ... 
    >>> foo()
    hello

|pause|

.. sourcecode:: python

    >>> from magic import rebind_globals
    >>> foo2 = rebind_globals(foo, {'A': 'ciao'})
    >>> A
    'hello'
    >>> foo()
    hello
    >>> foo2()
    ciao

|end_example|
|end_scriptsize|


``LOAD_GLOBAL`` explained
==========================

.. animage:: diagrams/LOAD_GLOBAL-p*.pdf
   :align: center
   :scale: 30%



Spell #1: ``rebind_globals`` (2)
=================================

|scriptsize|
|example<| |small| magic.py |end_small| |>|

.. sourcecode:: python

    def rebind_globals(func, newglobals=None):
        if newglobals is None:
            newglobals = globals()
        newfunc = types.FunctionType(func.func_code, 
                                     newglobals, 
                                     func.func_name,
                                     func.func_defaults)
        return newfunc


|end_example|
|end_scriptsize|


Problem #1 solved
==================


|column1|
|scriptsize|
|example<| |small| pdbpp.py |end_small| |>|

.. sourcecode:: python

   import pdb
   class Pdb(pdb.Pdb):
       ...

   set_trace = rebind_globals(
             pdb.set_trace)
   
   main = rebind_globals(pdb.main)
   ...

|end_example|
|end_scriptsize|
|column2|

|pause|
|small|

* Pros

  - code reuse

  - cross-version compatibility

* Cons

  - complexity

  - fragility

  - unexpected bugs (e.g. ``func_defaults``)

|end_small|

|end_columns|


Problem #2: Open Classes
=========================

- Huge hierarchy of classes

- Many (loosely related) features per class

  * e.g. visitor pattern

|pause|

- two-axis split:

  * by feature

  * by class

- Split the class among more files?

  * no way in Python

  * in Ruby: "open classes"


Problem #2: the PyPy AST compiler
=================================

.. animage:: diagrams/AST-p*.pdf
   :align: center
   :scale: 25%


Spell #2: __extend__ (1)
========================

|scriptsize|
|example<| |small| python |end_small| |>|

.. sourcecode:: python

    >>> from magic import extendabletype
    >>> class A(object):
    ...     __metaclass__ = extendabletype
    ...     def foo(self):
    ...         print 'foo'
    ... 
    >>> obj = A()
    >>> obj.foo()
    foo

|pause|

.. sourcecode:: python

    >>> class __extend__(A):
    ...     def bar(self):
    ...         print 'bar'
    ... 
    >>> obj.foo()
    foo
    >>> obj.bar()
    bar

|end_example|
|end_scriptsize|


Metaclasses for dummies (1)
============================

* Everything is an object

* Every object has a type (a class)

* A class is an object

* The class of a class: metaclass

* ``class`` statement --> metaclass instantiation


``class`` statement
===================

.. animage:: diagrams/metaclass-p*.pdf
   :align: center
   :scale: 35%


Metaclasses for dummies (2)
============================

* Find the metaclass (simplified)

  - ``__metaclass__`` in the class body

  - ``type(bases[0])`` (if any)

  - global ``__metaclass__``

|pause|

* Call it!

  - subclass of type (usually)

  - override ``__new__``

  - tweak the parameters?


Spell #2: __extend__ (2)
========================

|scriptsize|
|example<| |small| example |end_small| |>|

.. sourcecode:: python

    class A(object):
        __metaclass__ = extendabletype
    
    class __extend__(A):
        def bar(self): print 'bar'

|end_example|
|end_scriptsize|

|pause|

|scriptsize|
|example<| |small| magic.py |end_small| |>|

.. sourcecode:: python

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

|end_example|
|end_scriptsize|


Problem #2 solved
==================


|column1|
|scriptsize|
|example<| |small| astcompiler/ |end_small| |>|

.. sourcecode:: python

   # ast.py
   class AST(...):
     __metaclass__ = extendabletype
     ...
   class expr(AST): ...
   class stmt(AST): ...

|pause|

.. sourcecode:: python

   # asthelpers.py
   class __extend__(AST):
     def as_node_list(...): ...
     def set_context(...):  ...

   class __extend__(expr): ...
   class __extend__(stmt): ...

   # codegen.py  ...
   # optimize.py ...

|end_example|
|end_scriptsize|
|column2|

|pause|
|small|

* Pros

  - better organization

  - well-contained

  - easy to understand

* Cons

  - naming convention

  - import-time side effects

  - unobvious at first

|end_small|
|end_columns|


Simple is better than complex
===============================

* Use as much much magic as actually needed

|pause|

* Example: Camelot admin classes

  - ``Entity`` subclass for the data model

  - ``Foo.Admin`` for UI stuff

  - mixing business and presentation logic :-(

|scriptsize|
|example<| |small| model.py |end_small| |>|

.. sourcecode:: python

   class User(Entity):
       name = Field(Unicode)
       age = Field(Integer)

       class Admin(EntityAdmin):
           verbose_name = 'User'
           field_list = ['name', 'age']

|end_example|
|end_scriptsize|


Problem #3: wrong solution
===========================

|scriptsize|
|column1|
|example<| |small| model.py |end_small| |>|

.. sourcecode:: python

   class User(Entity):
     __metaclass__ = \
         extendabletype

     name = Field(Unicode)
     age = Field(Integer)

|end_example|
|column2|
|pause|
|example<| |small| admin.py |end_small| |>|

.. sourcecode:: python

   from model import User

   class __extend__(User):
     class Admin(EntityAdmin):
       verbose_name = 'User detail'
       field_list = ['name', 'age']

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* ``Entity`` has its own metaclass

* metaclass conflict

* there is a simpler solution anyway


Spell #3: attach_to (not really magical)
=========================================

|scriptsize|
|example<| |small| python |end_small| |>|

.. sourcecode:: python

    >>> from magic import attach_to
    >>> 
    >>> class Foo(object):
    ...     pass
    ... 
    >>> @attach_to(Foo)
    ... class Admin(object):
    ...     verbose_name = 'My Foo'
    ... 
    >>> print Foo.Admin.verbose_name
    My Foo

|end_example|
|end_scriptsize|


Decorators
==========

* Syntactic sugar

* class decorators only for Python >= 2.6

|scriptsize|
|column1|
|example<| |small| decor1.py |end_small| |>|

.. sourcecode:: python

   @foo
   def myfunc():
       pass

   @bar(42)
   class MyClass(object):
       pass
  
|end_example|
|column2|
|pause|
|example<| |small| decor2.py |end_small| |>|

.. sourcecode:: python

   def myfunc():
       pass
   myfunc = foo(myfunc)

   class MyClass(object):
       pass
   MyClass = bar(42)(MyClass)

|end_example|
|end_columns|
|end_scriptsize|

Spell #3: attach_to (not really magical)
=========================================

|scriptsize|
|example<| |small| magic.py |end_small| |>|

.. sourcecode:: python

    def attach_to(obj):
        def attach(cls):
            name = cls.__name__
            setattr(obj, name, cls)
        return attach

|end_example|
|end_scriptsize|

Problem #3 solved
==================

|scriptsize|
|column1|
|example<| |small| model.py |end_small| |>|

.. sourcecode:: python

   class User(Entity):

       name = Field(Unicode)
       age = Field(Integer)

|end_example|
|column2|
|pause|
|example<| |small| admin.py |end_small| |>|

.. sourcecode:: python

   @attach_to(User):
   class Admin(EntityAdmin):
       verbose_name = 'User detail'
       field_list = ['name', 'age']

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* Pros

  - Simple is better than complex
  - No metaclasses
  - Much less magic

* Cons

  - None :-)


Problem #4: quicker turnaround time (1)
========================================

* Developing new ``gdb`` commands

|scriptsize|
|example<| |small| gdbdemo.py |end_small| |>|

.. sourcecode:: python

    import gdb
    class MyCommand(gdb.Command):
        def __init__(self):
            gdb.Command.__init__(self, "mycmd", gdb.COMMAND_NONE)
        def invoke(self, arg, from_tty):
            print 'Hello from Python'

    MyCommand() # register the command

|end_example|
|pause|
|example<| |small| gdb |end_small| |>|

.. sourcecode:: sh

    $ PYTHONPATH="" gdb
    GNU gdb (Ubuntu/Linaro 7.3-0ubuntu2) 7.3-2011.08
    ...
    (gdb) python import gdbdemo
    (gdb) mycmd
    Hello from Python
    (gdb) 

|end_example|
|end_scriptsize|

Problem #4: quicker turnaround time (2)
========================================

* Annoying to develop

* Several steps to do every time:

  - start gdb

  - start the program

  - run until a certain point

  - try your command


Spell #4: reload & rebind __class__
===================================

|scriptsize|
|example<| |small| gdbdemo.py |end_small| |>|

.. sourcecode:: python

    import gdb

    class MyCommand(gdb.Command):
        def __init__(self):
            gdb.Command.__init__(self, "mycmd", gdb.COMMAND_NONE)

        def invoke(self, arg, from_tty):
            import gdbdemo2
            reload(gdbdemo2)
            self.__class__ = gdbdemo2.MyCommand
            self.do_invoke(arg, from_tty)

        def do_invoke(self, arg, from_tty):
            print 'Hello from Python'

    MyCommand() # register the command

|end_example|
|end_scriptsize|


Method lookup
==========================

.. animage:: diagrams/__class__-p*.pdf
   :align: center
   :scale: 40%


Problem #4 solved
==================

* Only during development

* Pros

  - Quicker turnaround

  - Useful in various situations

* Cons

  - Fragile

  - Confusion++ (two different classes with the same name)

  - Does not work in more complex cases


Bonus spell
===========

* How much time is left?

|pause|

.. raw:: latex

   \vspace{1.2cm}

|example<| |small| bonus.py |end_small| |>|

.. sourcecode:: python

   import time
   time.go_back(minutes=10)

|end_example|

.. raw:: latex

   \vspace{0.5cm}

|pause|

* How much time is left?


Problem #5: implicit global state
===================================

* ``elixir``

  - declarative layer on top of SQLAlchemy

  - (precursor of ``sqlalchemy.declarative``)

|pause|

|scriptsize|
|example<| |small| model.py |end_small| |>|

.. sourcecode:: python

    from elixir import (Entity, Field, Unicode, Integer, 
                        metadata, setup_all, create_all)

    metadata.bind = "sqlite:///db.sqlite"

    class User(Entity):
        name = Field(Unicode)
        age = Field(Integer)


    setup_all()
    create_all()
    # ...

|end_example|
|end_scriptsize|

Global state
=============

* Global state is evil

  - that's it

  - implicit is even worse

|pause|

* Hard to test

  - no isolation for tests

  - persistent side effects (e.g. DB)

|pause|

* Goal

  - multiple, isolated, independent DBs

  - one DB per test (or group of tests)

A step forward (1)
==================

|scriptsize|
|example<| |small| model.py |end_small| |>|

.. sourcecode:: python

    import sqlalchemy
    from elixir import (Entity, Field, Unicode, Integer,
                        setup_entities, GlobalEntityCollection)

    __session__ = sqlalchemy.orm.scoped_session(
                        sqlalchemy.orm.sessionmaker())
    __metadata__ = sqlalchemy.MetaData(bind="sqlite:///db.sqlite")
    __collection__ = GlobalEntityCollection()


    class User(Entity):
        name = Field(Unicode)
        age = Field(Integer)

    if __name__ == '__main__':
        setup_entities(__collection__)
        __metadata__.create_all()

|end_example|
|end_scriptsize|

A step forward (2)
==================

* Still global state

  - but explicit

* Goal: turn global state into local

* `N` indepentent

  - ``__metadata__`` & co.

  - ``model.User``

|pause|

* Multiple copies of the same module

* Modules are singleton

* Cannot rely on ``import``


``import`` logic (simplified)
==============================

* ``import foo``

  - find ``foo.py``

  - this is a whole mess of its own :-)

|pause|
|scriptsize|
|example<| |small| import foo |end_small| |>|

.. sourcecode:: python

    mod = types.ModuleType('foo')          # 1. create the module object
    mod.__file__ = '/path/to/foo.py'

    sys.modules['foo'] = mod               # 2. update sys.modules

    src = open('/path/to/foo.py').read()   # 3. compile&exec the code
    exec src in mod.__dict__

|end_example|
|end_scriptsize|




Spell #5: import_model (1)
==========================

|scriptsize|
|example<| |small| db.py |end_small| |>|

.. sourcecode:: python

    class Database(object):

        def __init__(self, url, modelfile):
            self.url = url
            self.session = sqlalchemy.orm.scoped_session(
                                sqlalchemy.orm.sessionmaker())
            self.metadata = sqlalchemy.MetaData(bind=url)
            self.collection = elixir.GlobalEntityCollection()
            self.import_model(modelfile)
            elixir.setup_entities(self.collection)

        def import_model(self, filename):
            ...

        def create_all(self, *args, **kwds):
            self.metadata.create_all(*args, **kwds)

    db = Database('sqlite:///db.sqlite')
    db.create_all()
    myuser = db.model.User('antocuni', 30)

|end_example|
|end_scriptsize|


Spell #5: import_model (2)
==========================

|scriptsize|
|example<| |small| db.py |end_small| |>|

.. sourcecode:: python

    def import_model(self, filename):
        # 1. create the module object
        self.model = types.ModuleType('model')
        self.model.__file__ = filename
        # 2. update sys.modules
        assert 'model' not in sys.modules
        sys.modules['model'] = self.model

        try:
            # inject the "local" state!
            self.model.__session__ = self.session
            self.model.__metadata__ = self.metadata
            self.model.__collection__ = self.collection

            # 3. compile&exec the code
            src = open(filename).read()
            code = compile(src, filename, 'exec')
            exec src in self.model.__dict__
        finally:
            # (Python doesn't do it usually :-))
            del sys.modules['model']

|end_example|
|end_scriptsize|


Problem #5 solved
==================

|scriptsize|
|example<| |small| test_model.py |end_small| |>|

.. sourcecode:: python

    def test_user():
      url = "sqlite:///tmp/db.tmp"
      db = Database(url, '/path/to/model.py')
      db.create_all()
      myuser = db.model.User( 'antocuni', 30)
      ...

|end_example|
|end_scriptsize|

|pause|

* Pros

  - testable

  - multiple DB

  - ``model.py`` kept simple

  - magic well contained

* Cons

  - complex

  - ``db1.model.User != db2.model.User``



Conclusion
===========

* Magic might be helpful

  - code reuse

  - readability

  - testability

* Use with care

  - only if you **know** what you are doing

  - lots of comments, please :-)

|pause|
|small|
`Debugging is twice as hard as writing the code in the first place. Therefore,
if you write the code as cleverly as possible, you are, by definition, not
smart enough to debug it.`

   (Brian Kernighan)

|end_small|


Contacts, Q&A
==============

- |small| http://bitbucket.org/antocuni/whitemagic |end_small|

- twitter: @antocuni

- Available for consultancy & training:

  * http://antocuni.eu

  * info@antocuni.eu

- Any question?
