import sys
from typing import *
from typing import _GenericAlias as GenericAlias

from .enumly import enum
from ._data_variable import DataVariable

from functools import wraps
from types import FunctionType

__all__ = ("Option", "Result", "UnwrapError", "resulting")


def raise_(exc):
    raise exc


T, S = TypeVar("T"), TypeVar("S")

# this module cannot rely on envirmont loaded inot builtins
# some fo these are defined it eh _env_bootstrap


class UnwrapError(Exception):
    pass


# linke NoneType
@enum
class DefaultType:
    class Default:
        def __repr__(self):
            return "Default"


# useful funcs
@enum
class Option(Generic[T]):
    class Nothing:
        def __repr__(self):
            return f"Nothing"

    class Some:
        thing: T

        def __repr__(self):
            return f"Some({repr(self.thing)})"

    def __new__(cls, thing: Optional[object] = None) -> "Option":
        global Option
        # if the input value is None or not provided then return Nothing,
        # this was choosen to make it super easy to turn an onld python object
        # into a enum one easily just Option(obj) and if it in None it will be converted
        # they can explicitly Some(None) is that is desired
        if thing is None or thing is Option.Nothing:
            return Option.Nothing
        else:
            return Option.Some(thing)

    @classmethod
    def _cls_title_(cls):
        return cls.__name__

    def __invert__(self) -> T:
        return self.unwrap()

    def unwrap(self, msg: str = "nothing to unwrap") -> T:
        global Option, UnwrapError
        if isinstance(self, Option.Some):
            return self.thing
        else:
            raise UnwrapError(msg)

    def isfull(self) -> bool:
        global Option, isinstance
        return isinstance(self, Option.Some)


@enum
class Result(Generic[T, S]):
    class Okay:
        value: T

    class Error:
        report: Union[S, str, Exception]
        # _file: Optional[str] = None
        # report: Union[S, Exception] # string suggested

        def raise_error(self) -> None:
            report = self.report
            if isinstance(report, Exception):
                raise report
            else:
                raise ValueError(self.report)

        """def __init__(self, report):
            frame = sys._getframe(1)
            #print(dir(frame))
            super(Result.Error, self).__init__(report, frame.f_globals['__name__'])"""

    def __new__(cls, thing) -> "Result":
        global Result, Exception

        if isinstance(thing, Result.Okay):
            return Result.Okay(thing.value)
        elif isinstance(thing, Result.Error):
            return Result.Error(thing.report)
        elif isinstance(thing, Exception):
            return Result.Error(thing)
        else:
            return Result.Okay(thing)

    def __invert__(self) -> T:
        return self.unwrap()

    def isokay(self) -> bool:
        global Result, isinstance
        return isinstance(self, Result.Okay)

    def unwrap(self, msg: str = "nothing to unwrap") -> T:
        if self.isokay():
            return self.value
        else:
            reporterr = self.report
            if not isinstance(reporterr, Exception):
                if len(msg):
                    reporterr = UnwrapError(reporterr, "\nand:", msg)
                else:
                    reporterr = UnwrapError(reporterr)
            raise reporterr  # this line from Result


def resulting(fn: FunctionType) -> FunctionType:
    if not hasattr(fn, "__annotations__") or "return" not in fn.__annotations__:
        raise ValueError(
            f"function {fn} does not have a return type annotation,"
            " required for result"
        )
    else:
        anotes = fn.__annotations__
        ret = anotes["return"]

    assert isinstance(ret, GenericAlias), (
        "the return type annotation for @resulting must be a generic Result, "
        f"found an object of type {type(ret)}"
    )

    assert ret.__origin__ is Result, (
        "the return type annotation for @resulting must be Result[...], " f"found {ret}"
    )

    T, E = ret.__args__
    assert isinstance(T, type), (
        "currently @resulting can only check Result[T, E] "
        f"where T is a non generic type, found {T}"
    )

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            ret = fn(*args, **kwargs)
            if isinstance(ret, Result):
                result = ret
            else:
                result = Result.Okay(ret)

            if not result.isokay():
                return result
            elif not isinstance(result.value, T):
                # print(result.value, T, isinstance(result.value, T))
                raise TypeError(
                    f"function '{fn.__module__}.{fn.__qualname__}' "
                    f"returned the wrong type,\nexpected {T} got "
                    f"{type(result.value)} from value...\n`{repr(result.value)}`"
                )
            else:
                return result
        except Exception as e:
            return Result.Error(e)

    return wrapper


def test(print):

    Nothing = Option.Nothing
    Some = Option.Some

    empty = Option.Nothing
    thing = Some(5)

    assert isinstance(empty, Option)
    assert empty is Option.Nothing
    assert not isinstance(empty, Option.Some)

    assert isinstance(thing, Option)
    assert not thing is Option.Nothing
    assert isinstance(thing, Option.Some)
    print("all base asserts passed")

    print("checking unwrapping Nothing...")
    try:
        Nothing.unwrap()
    except UnwrapError:
        assert True, "test passed"

    print("checking unwrapping Some(_)...")
    assert 5 == Some(5).unwrap(), (
        f"Some(5).unwrap() != 5 for soem reason, got" f"{Some(5).unwrap()=}"
    )

    print("checking auto init of Option...")
    assert Option() == Nothing, f"got {Option()=}"
    assert Option(None) == Nothing, f"got {Option(None)=}"
    assert Option(5) == Some(5), f"got {Option(5)=}"
