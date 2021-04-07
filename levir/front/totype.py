from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, UserType

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

from . import tofunc, treetools


@strictly
def fromtree(mod: Module, tree: Tree) -> Result[UserType, str]:
    assert tree.data in ("classdef", "structdef", "traitdef"), unsupported(
        mod.filename, tree, "no rule to translate this kind of type"
    )
    kind = tree.data
    nametree, supertrees, mbrstreeseq, mthdstreeseq = tree.children

    name = str(~firsttoken(nametree))
    supers = tuple(
        ~treetools.itemspec(mod.filename, supertree)
        for supertree in supertrees.children
    )

    mbrs = {}
    if len(mbrstreeseq.children):
        for mbrdeftree in mbrstreeseq.children[0].children:
            # print(Location.fromtree(mod.filename, mbrdeftree))
            nametree, spectree = mbrdeftree.children
            mbrname = str(~firsttoken(nametree))
            spec = ~treetools.itemspec(mod.filename, spectree)
            if mbrname not in mbrs:
                mbrs[mbrname] = spec
            else:
                raise AttributeError(
                    f"{spec.loc}: redefinition of member '{name}.{mbrname}:{mbrs[name]}' "
                    f"redefined, (to {spec})"
                )
        else:
            pass

    mthds = {}
    if len(mthdstreeseq.children):
        for mthddeftree in mthdstreeseq.children[0].children:
            # print(Location.fromtree(mod.filename, mbrdeftree))
            mthd = ~tofunc.fromtree(mod, mthddeftree)
            mthdname = mthd.name
            if mthdname not in mthds:
                mthds[mthdname] = mthd
            else:
                raise AttributeError(
                    f"{spec.loc}: redefinition of method '{name}.{mthdname}' redefined"
                )
        else:
            pass

    cls, maybe_mbrs = match(tree.data)[
        "classdef" : lambda: (UserType.Class, {"mbrs": ComposedAttrs.new(mbrs)}),
        "structdef" : lambda: (UserType.Struct, {"mbrs": ComposedAttrs.new(mbrs)}),
        "traitdef" : lambda: (UserType.Trait, {}),
        ... : MatchError(
            unsupported(
                mod.filename,
                tree,
                f"unreachable, this should have been caught by an assert above",
            )
        ),
    ]

    if cls is UserType.Trait:
        assert len(mbrs) == 0, (
            f"{[*mbrs.values()][0].loc}: trait's cannot have members"
            "this may eventually be repalced getters"
        )

    return Okay(
        cls(
            loc=Location.fromtree(mod.filename, tree),
            mod=mod,
            name=str,
            mthds=ComposedAttrs.new(mthds),
            **maybe_mbrs,
        )
    )
