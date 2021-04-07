from strictly import *
from envly import *
from typing import *

from levir import tout
from levir.tout import Module, ItemSpec

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


@strictly
def itemspec(filename: str, tree: Tree) -> Result[ItemSpec, str]:
    assert tree.data == "itemspec", unsupported(
        filename,
        tree,
        f"file parsed incorrectly. Found an itemspec of data '{tree.data}':\n\t"
        f"`{reconstruct(tree)}`",
    )

    if len(tree.children) == 4:
        reftree, modpathtree, nametree, gentree = tree.children
        isref = bool(len(reftree.children))

        modpath = tuple(namefrom(modtree) for modtree in modpathtree.children)

        name = namefrom(nametree)

        if len(gentree.children):
            raise AttributeError(
                unsupported(filename, gentree),
                f"generic type parameters not yet supported",
            )
        else:
            gens = ()

    loc = Location.fromtree(filename, tree)

    return Okay(
        match(len(tree.children))[
            0,
            1 : lambda: ItemSpec.infer(loc),
            4 : lambda: ItemSpec.named(loc, isref, modpath, name, gens),
            ... : MatchError(
                unsupported(
                    filename,
                    tree,
                    f"found {len(tree.children)} attributes, expected 0, 1, or 4.\n\t"
                    f"`{reconstruct(tree)}`",
                )
            ),
        ]
    )
