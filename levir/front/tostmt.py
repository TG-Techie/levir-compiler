from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, Stmt

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

from . import treetools, tosubject, toexpr

# from . import toexpr


@strictly
def fromtree(mod: Module, tree: Tree) -> Result[Stmt, str]:
    loc = Location.fromtree(mod.filename, tree)
    return match(tree.data)[
        "stmt" : lambda: fromtree(mod, tree.children[0]),
        "asn_stmt" : lambda: _fromasn(mod, loc, tree),
        "ret_stmt" : lambda: _fromret(mod, loc, tree),
        "brk_stmt" : lambda: _frombrk(mod, loc, tree),
        "cont_stmt" : lambda: _fromcont(mod, loc, tree),
        "loop_stmt" : lambda: _fromloop(mod, loc, tree),
        "expr_stmt" : lambda: _fromexpr(mod, loc, tree),
        "cond_stmt" : lambda: _fromcond(mod, loc, tree),
        "dropin_stmt" : lambda: _fromdropin(mod, tree),
        "unreachable_stmt" : lambda: _fromunreachable(mod, tree),
        ... : MatchError(
            unsupported(
                mod.filename, tree, f"unable to make a statement from '{tree.data}'"
            )
        ),
    ]


@strictly
def _fromasn(mod: Module, loc: Location, tree: Tree) -> Result[Stmt.asn, str]:

    subjtree, exprtree = tree.children
    loc = Location.fromtree(mod.filename, tree)

    return Okay(
        Stmt.asn(
            loc=loc,
            mod=mod,
            subj=~tosubject.fromtree(mod, subjtree),
            expr=~toexpr.fromtree(mod, exprtree),
        )
    )
