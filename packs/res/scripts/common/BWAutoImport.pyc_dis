# Embedded file name: scripts/common/BWAutoImport.py
import __builtin__

class _Helper(object):
    """Define the built-in 'help'.
    This is a wrapper around pydoc.help (with a twist).
    
    """

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        import pydoc
        return pydoc.help(*args, **kwds)


def sethelper():
    __builtin__.help = _Helper()


def main():
    sethelper()


main()