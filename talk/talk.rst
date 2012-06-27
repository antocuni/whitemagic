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


About this talk
================

- a collection of hacks :-)

|pause|

**HOWEVER**

- real-life problems

- real-life solutions

- they improve the rest of the code

- (you might not like them)


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

.. image:: diagrams/LOAD_GLOBAL-p0.pdf
   :align: center
   :scale: 30%

``LOAD_GLOBAL`` explained
==========================

.. image:: diagrams/LOAD_GLOBAL-p1.pdf
   :align: center
   :scale: 30%

``LOAD_GLOBAL`` explained
==========================

.. image:: diagrams/LOAD_GLOBAL-p2.pdf
   :align: center
   :scale: 30%

``LOAD_GLOBAL`` explained
==========================

.. image:: diagrams/LOAD_GLOBAL-p3.pdf
   :align: center
   :scale: 30%

``LOAD_GLOBAL`` explained
==========================

.. image:: diagrams/LOAD_GLOBAL-p4.pdf
   :align: center
   :scale: 30%


``LOAD_GLOBAL`` explained
==========================

.. image:: diagrams/LOAD_GLOBAL-p5.pdf
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

.. image:: diagrams/AST-p0.pdf
   :align: center
   :scale: 25%

Problem #2: the PyPy AST compiler
=================================

.. image:: diagrams/AST-p1.pdf
   :align: center
   :scale: 25%

Problem #2: the PyPy AST compiler
=================================

.. image:: diagrams/AST-p2.pdf
   :align: center
   :scale: 25%

Problem #2: the PyPy AST compiler
=================================

.. image:: diagrams/AST-p3.pdf
   :align: center
   :scale: 25%

Problem #2: the PyPy AST compiler
=================================

.. image:: diagrams/AST-p4.pdf
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

.. image:: diagrams/metaclass-p0.pdf
   :align: center
   :scale: 35%


``class`` statement
===================

.. image:: diagrams/metaclass-p1.pdf
   :align: center
   :scale: 35%


``class`` statement
===================

.. image:: diagrams/metaclass-p2.pdf
   :align: center
   :scale: 35%


``class`` statement
===================

.. image:: diagrams/metaclass-p3.pdf
   :align: center
   :scale: 35%


``class`` statement
===================

.. image:: diagrams/metaclass-p4.pdf
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
