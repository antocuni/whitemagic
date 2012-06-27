from magic import attach_to

class Foo(object):
    pass

@attach_to(Foo)
class Admin(object):
    verbose_name = 'My Foo'

print Foo.Admin.verbose_name
