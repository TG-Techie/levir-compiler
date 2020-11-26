from typing import *

__all__ = ('isiterable', 'isclass', 'areall')

def isiterable(obj: object) -> bool:
    global isinstance
    return not isinstance(obj, type) and hasattr(obj, '__iter__')

def isclass(obj: object) -> bool:
    global isinstance
    return isinstance(obj, type)

def areall(itrbl, types):
    global isiterable
    assert isiterable(itrbl), f"for areall(thing, (...)), 'thing' must be iterable"
    return all(isinstance(item, types) for item in itrbl)


def _proto_pipethru(val:object, *fns) -> object:
    if not isinstance(val, tuple):
        val = (val,)

    for fn in fns:
        val = fn(*val)

    return val


def test(print):
    pass # TODO: add tests
