from envly import *
from typing import _GenericAlias as GenericAlias

from functools import wraps
from types import FunctionType


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
                    f"function '{fn.__module__}.{fn.__qualname__}' returned the wrong type, expected {T} got {type(result.value)}"
                )
            else:
                return result
        except Exception as e:
            return Result.Error(e)

    return wrapper


@resulting
def h(num: int) -> Result[int, str]:
    if num < 0:
        raise ValueError(f"h cannot be less then 0, found {num}")
    else:
        return num


@resulting
def g(num: int) -> Result[int, str]:
    if num < 0:
        raise ValueError(f"g cannot be less then 0, found {num}")
    else:
        return Okay(num)


print(h(4))
print(h(-1))
print(h(0))
print(h(0.0))

print(g(4))
print(g(-1))
print(g(0))
print(g(0.0))
