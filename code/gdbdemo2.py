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
