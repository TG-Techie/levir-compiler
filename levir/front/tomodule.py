from strictly import *
from envly import *
from typing import *

from levir import tout

from levir.lexer_parser import (
    Location,
    Tree,
    Token,
    parse_str,
    namefrom,
    unsupported,
    reconstruct,
)


from . import totype
from . import tofunc


@strictly
def fromtree(filename: str, tree: Tree) -> Result[tout.Module, str]:

    # TODO: chagne name on modules based on file layout
    name = filename.split("/")[-1].split(".")[0]

    mod = tout.Module(
        filename=filename,
        name=name,
    )

    deftrees = [itemtree.children[0] for itemtree in tree.children]
    for deftree in deftrees:
        item = match(deftree.data)[
            "classdef",
            "structdef",
            "traitdef" : lambda: ~totype.fromtree(mod, deftree),
            "fndef" : lambda: ~tofunc.fromtree(mod, deftree),
            ... : MatchError(
                unsupported(filename, deftree, f"unknown item '{deftree.data}'")
            ),
        ]
        if item.name in mod.items:
            raise AttributeError(
                f"{item.loc}: redefinition of {type(item).__name__} "
                f"'{item.name}', previously defined at []"
            )

    return Okay(mod)
