from strictly import *
from envly import *
from typing import *
from envly._data_variable import (
    DataVariable,
    _DefaultField,
    _DerivedField,
    _FactoryField,
)

from levir.lexer_parser import (
    Location,
    Tree,
    Token,
    parse_str,
    namefrom,
    unsupported,
    reconstruct,
)


from levir import tout

from . import tomodule


@strictly
def fromfile(file) -> Result[tout.Module, str]:
    tree = parse_str(file.read())
    return Okay(~tomodule.fromtree(file.name, tree))
