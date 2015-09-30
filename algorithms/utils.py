from functools import partial

class memoize():
    """
    Credit goes to Daniel Miller, Wed, 3 Nov 2010 (MIT).
    http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/


    cache the return value of a method

    This class is meant to be used as a decorator of methods. The return value
    from a given method invocation will be cached on the instance whose method
    was invoked. All arguments passed to a method decorated with memoize must
    be hashable.

    If a memoized method is invoked directly on its class the result will not
    be cached. Instead the method will be invoked like a static method:
    class Obj(object):
        @memoize
        def add_to(self, arg):
            return self + arg
    Obj.add_to(1) # not enough arguments
    Obj.add_to(1, 2) # returns 3, result is not cached
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)

    def __call__(self, *args, **kw):
        obj = args[0]
        try:
            cache = obj.__cache
        except AttributeError:
            cache = obj.__cache = {}
        key = (self.func, args[1:], frozenset(kw.items()))
        try:
            res = cache[key]
        except KeyError:
            res = cache[key] = self.func(*args, **kw)
        return res


"""
Creating some special classes that can be hashed and used as keys in dictionaries:
"""


class HashableList(list):
    """List class that can be used as key in dictionaries. Superficial (not deep equal)"""
    def __init__(self, _list=None):
        list.__init__(self, _list or [])

    def __eq__(self, other):
        return isinstance(other, HashableList) and self.__hash__() == other.__hash__()

    def __hash__(self):
        """Superficial (not deep equal)"""
        return hash(str(self))


class Bunch(dict):
    """Simple class for prototyping and other handy stuff"""
    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __eq__(self, other):
        return isinstance(other, Bunch) and self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(str(self))