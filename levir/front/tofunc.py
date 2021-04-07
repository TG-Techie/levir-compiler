from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, Func, Mthd, Block

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
from . import tostmt


@strictly
def fromtree(mod: Module, tree: Tree) -> Result[Func, str]:
    assert tree.data in ("fndef", "mthddef"), unsupported(
        mod.filename,
        tree,
        f"no knowledge of how to make function or method '{tree.data}'",
    )

    nametree, argstree, retspectree, frametree = tree.children

    name = namefrom(nametree)
    rettype = ~treetools.itemspec(mod.filename, retspectree)

    enteredargs = {}
    for argtree in argstree.children:
        nametree, spectree = argtree.children
        argname = namefrom(tree)
        spec = ~treetools.itemspec(mod.filename, spectree)
        if argname not in enteredargs:
            enteredargs[argname] = spec
        else:
            raise AttributeError(f"{spec.loc}: argument '{argname}' repeated")

    frame = block_fromtree(mod, frametree)


@strictly
def block_fromtree(mod: Module, tree: Tree) -> Result[Block, str]:
    assert "block" in tree.data, f"cannot make a frame from '{tree.data}'"

    return Okay(
        Block(
            loc=Location.fromtree(mod.filename, tree),
            stmts=tuple(~tostmt.fromtree(mod, stmt) for stmt in tree.children),
        )
    )
