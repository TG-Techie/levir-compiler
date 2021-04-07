from typing import *
from .env import *
from .matching import *


class OverflowError(Exception):
    pass


class SignError(Exception):
    pass


class IntType(int):
    def __new__(cls, base=0):
        global int

        return int.__new__(cls, cls.tryfrom(base).unwrap())

    def __repr__(self):
        return f"{type(self).__name__}({int(self)})"

    @classmethod
    def tryfrom(cls, src: object) -> Result["IntType", Exception]:
        global _raise_errors
        try:
            num = int(src)
            return match(cls._check_int_(num))[
                Okay : lambda _: Okay(num), Error : lambda report: Error(report)
            ]
        except Exception as e:
            return Result(e)

    # array constructor
    def __class_getitem__(
        cls, src: Union[int, Tuple[int, ...], type(...)]
    ) -> "List[IntType]":
        if src is ...:
            return List[cls]
        elif isinstance(src, int):
            src = (int,)
        else:
            pass  # must be a tuple
        # assert all(), f"{cls.__name__}[...] must all be castable to '{cla.__name__}'"

        ls = []
        for num in src:
            if not isinstance(num, int):
                raise TypeError(
                    f"{cls.__name__}[...] must be ints, found a '{type(num).__name__}'"
                )
            elif cls._check_int_(num).unwrap():
                pass
            ls.append(cls(num))
        else:
            return ls

    binops = {
        "__add__",
        "__and__",
        "__divmod__",
        "__float__",
        "__floor__",
        "__floordiv__",
        "__lshift__",
        "__mod__",
        "__mul__",
        "__or__",
        "__pow__",
        "__radd__",
        "__rand__",
        "__rdivmod__",
        "__rfloordiv__",
        "__rlshift__",
        "__rmod__",
        "__rmul__",
        "__ror__",
        "__rpow__",
        "__rrshift__",
        "__rshift__",
        "__rsub__",
        "__rtruediv__",
        "__rxor__",
        "__sub__",
        "__truediv__",
        "__xor__",
        # logical ops:
        "__lt__",
        "__ne__",
        "__ge__",
        "__gt__",
        "__le__",
        "__eq__",
    }

    # need to do: __reduce_ex__, __reduce__, __round__,

    uniops = {
        "__abs__",
        "__ceil__",
        "__invert__",
        "__index__",
        "__neg__",
        "__pos__",
        "__trunc__",
    }

    for op in uniops:
        exec(
            f"""def {op}(self):
                    return type(self)(int(self).{op}())
                    #cls = type(self)
                    #return cls(int(self).{op}())
        """
        )
    else:
        del uniops

    # if __debug__: # if degub raise error on overflow
    for op in binops:
        exec(
            f"""def {op}(self, other):
                    cls = type(self)
                    if not isinstance(other, cls):
                        raise  TypeError(f"cannot {op.strip('_')} a '{{type(other).__name__}}' to '{{cls.__name__}}', "\
                            f"be sure to cast using `{{cls.__name__}}.tryfrom({{other}})`"
                        )
                    return cls(int(self).{op}(int(other)))
        """
        )
    else:
        del binops


class UnsignedInt(IntType):

    _bit_width_ = None

    @classmethod
    def _check_int_(cls, val) -> Result[IntType, Exception]:
        print(val >= 2 ** cls._bit_width_)
        if val >= 2 ** cls._bit_width_:
            return Result(
                OverflowError(
                    f"{cls.__name__} can't be {val}, must be "
                    f"between 0 and {2**cls._bit_width_}"
                )
            )
        elif val < 0:
            return Result(
                SignError(
                    f"{cls.__name__} can't be negative, must be "
                    f"between 0 and {2**cls._bit_width_}"
                )
            )
        else:
            return Result(None)


class SignedInt(IntType):

    _bit_width_ = None

    @classmethod
    def _check_int_(cls, val) -> Result[None, Exception]:
        bound_val = 2 ** (cls._bit_width_ - 1)
        # print(f"{cls=}, {val=}, {-bound_val=}, {bound_val=}, {-bound_val <= val =}, {val < bound_val=}, {not -bound_val <= val < bound_val=}")
        if not -bound_val <= val < bound_val:
            return Result(
                OverflowError(
                    f"{cls.__name__} can't be {val}, must "
                    f"be between {-bound_val} and {bound_val-1}"
                )
            )
        else:
            return Result(None)


for x in range(3, 3 + 10):
    width = 2 ** x
    # exec(f"""class uint{width}(uint{2**(x-1)}):
    exec(
        f"""class uint{width}(UnsignedInt):
                _bit_width_ = {width}
                """
    )
    # exec(f"u{width} = uint{width}")

for x in range(3, 3 + 10):
    width = 2 ** x
    exec(
        f"""class int{width}(SignedInt):
                _bit_width_ = {width}
    """
    )
