import sys

from . import enumly
from .enumly import *

from . import _env_bootstrap
from ._env_bootstrap import *

__all__ = (
    ("Default", "Some", "Nothing", "Okay", "Error", "using")
    + enumly.__all__
    + _env_bootstrap.__all__
)

## global constants
DefaultType = _env_bootstrap.DefaultType
Default = DefaultType.Default

# Option
Some = Option.Some
Nothing = Option.Nothing

# Result
Okay = Result.Okay
Error = Result.Error


def using(enum_cls: EnumClass) -> None:
    """
    like c++ using?
    """
    global sys
    assert isinstance(enum_cls, EnumClass) and not isinstance(
        enum_cls, EnumVariantClass
    )
    block = sys._getframe(1).f_locals
    for name, varnt in enum_cls._enum_varnts_.items():
        block[name] = varnt


def test(print):
    enumly.test(print)
    _env_bootstrap.test(print)
