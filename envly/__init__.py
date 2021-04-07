from . import env  # includes enumly
from .env import *

from . import matching
from .matching import *

from . import _tools
from ._tools import *

__all__ = env.__all__ + matching.__all__ + _tools.__all__


def test(print=print):
    printdent = lambda *args: print("    ", *args)

    env.test(printdent)
    matching.test(printdent)
    _tools.test(printdent)
