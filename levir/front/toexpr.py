from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, Expr, Subject, ItemSpec

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
def fromtree(mod: Module, tree: Tree) -> Result[Expr, str]:
    loc = Location.fromtree(mod.filename, tree)
    return Okay(
        match(tree.data)[
            "expr",
            "paren_expr" : lambda: ~fromtree(mod, tree.children[0]),
            "get_expr" : lambda: ~_get_fromtree(mod, loc, tree),
            "itemcall_sugar" : lambda: ~_itemcall_fromtree(mod, loc, tree),
            "fncall_expr" : lambda: ~_mthdcall_fromtree(mod, loc, tree),
            "mthdcall_expr" : lambda: ~_mthdcall_fromtree(mod, loc, tree),
            "new_expr" : lambda: ~_new_fromtree(mod, loc, tree),
            "litrl_expr" : lambda: ~_litrl_fromtree(mod, loc, tree),
            "ref_expr" : lambda: ~_ref_fromtree(mod, loc, tree),
            "or_expr" : lambda: ~_or_fromtree(mod, loc, tree),
            "and_expr" : lambda: ~_and_fromtree(mod, loc, tree),
            "not_expr" : lambda: ~_not_fromtree(mod, loc, tree),
            "dropin_expr" : lambda: ~_dropin_fromtree(mod, loc, tree),
            ... : MatchError(f"{loc}: no way to make an '{tree.data}' expression"),
        ]
    )


@strictly
def _itemcall_fromtree(mod: Module, loc: Location, tree: Tree) -> Result[Expr, str]:
    print(loc)
    print(tree)
    FUCK
