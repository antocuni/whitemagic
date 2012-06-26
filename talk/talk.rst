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


Spell #1: ``rebind_globals``
=============================


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

|scriptsize|
|column1|
|example<| |small| dis(pdb.set_trace) |end_small| |>|

.. sourcecode:: python

   0 LOAD_GLOBAL       0 (Pdb)
   3 CALL_FUNCTION     0
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

