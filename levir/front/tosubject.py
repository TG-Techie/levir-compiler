from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, Subject, ItemSpec

from levir.lexer_parser import (
    Location,
    Tree,
    Token,
    parse_str,
    namefrom,
    unsupported,
    reconstruct,
    firsttoken,
)

from . import treetools


@strictly
def fromtree(mod: Module, tree: Tree) -> Result[Subject, str]:
    loc = Location.fromtree(mod.filename, tree)
    return Okay(
        match(tree.data)[
            "mbrof" : lambda: _mbr_fromtree(mod, loc, tree),
            "var" : lambda: _var_fromtree(mod, loc, tree),
            ... : MatchError(
                f"{loc}: no known subject of kind '{tree.data}'\n\t`{reconstruct(tree)}`"
            ),
        ]
    )


@strictly
def _mbr_fromtree(mod: Module, loc: Location, tree: Tree) -> Result[Subject.mbr, str]:

    vartree, mbrstree = tree.children

    return Okay(
        Subject.mbr(
            loc=loc,
            mod=mod,
            var=~fromtree(mod, vartree),
            mbrs=tuple(str(name) for name in mbrstree.children),
            type=ItemSpec.infer,
        )
    )


@strictly
def _var_fromtree(mod: Module, loc: Location, tree: Tree) -> Result[Subject.var, str]:
    assert len(tree.children) in (1, 2), (
        f"{loc}: no rule to make a var subject from " f"{len(tree.children)} attributes"
    )

    typespec = match(len(tree.children))[
        1 : lambda: ItemSpec.infer,
        2 : lambda: ~treetools.itemspec(mod.filename, tree.children[1]),
        ... : MatchError("unreachable due to above assert"),
    ]

    return Okay(Subject.var(loc, mod, name=namefrom(tree.children[0]), type=typespec))
