from magic import rebind_globals

A = 'hello'

def foo():
    print A

foo2 = rebind_globals(foo, {'A': 'ciao'})

print A
foo()
foo2()
