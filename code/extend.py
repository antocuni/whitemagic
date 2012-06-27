from magic import extendabletype

class A(object):

    __metaclass__ = extendabletype

    def foo(self):
        print 'foo'


class __extend__(A):

    def bar(self):
        print 'bar'


obj = A()
obj.foo()
obj.bar()
