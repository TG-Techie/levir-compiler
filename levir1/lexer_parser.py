from envly import *
from strictly import *
from typing import *
from dataclasses import dataclass

import lark
from lark import Lark
from lark.indenter import Indenter
from lark.reconstruct import Reconstructor

from lark.tree import Tree
from lark import Token

from lark.reconstruct import Reconstructor

### hot patch lark tree repr and token repr
def Tree__repr__(self):
    return "Tree(%r, %r)" % (self.data, self.children)


Tree.__repr__ = Tree__repr__


def Token__repr__(self):
    return "Token(%r, %r)" % (self.type, self.value)


Token.__repr__ = Token__repr__
### hot patch lark tree repr and token repr

_parser = Lark.open(
    "levir_syntax.lark",
    # parser='earley',
    rel_to=__file__,
    # ambiguity='resolve'
    lexer="standard",
)

_reconstrucor = Reconstructor(_parser)


def parse_str(string):
    global _parser
    return _parser.parse(string)


def parse_file(name: str):
    with open(name) as file:
        return parse_str(file.read())


def reconstruct(tree: Tree):
    return _reconstrucor.reconstruct(tree)


@strictly
def namefrom(thing: Union[Tree, Token]) -> str:
    global firsttoken
    return str(~firsttoken(thing))


@strictly
def firsttoken(thing: Union[Tree, Token]) -> Option[Token]:
    if isinstance(thing, Token):
        return Some(thing)
    while isinstance(thing, Tree):
        if len(thing.children):
            thing = thing.children[0]
        else:
            if thing.meta.empty:
                return Some(Token(thing.data.upper(), thing.data))
            else:
                return Nothing
    return Some(thing)  # must be a Token


@dataclass(frozen=True)
class Location:
    path: str
    line: Optional[int]
    col: Optional[int]

    # __slots__ = slots(__annotations__)

    def __str__(self) -> str:
        return f"[file:'{self.path}' line:{self.line} col:{self.col}]"

    def __repr__(self) -> str:
        return f"Location({repr(self.path)}, {repr(self.line)}, {repr(self.col)})"

    @classmethod
    @strictly
    def fromtree(cls: type, path: str, tree: Tree):  # -> Location
        return cls.fromtoken(
            path,
            firsttoken(tree).unwrap(
                f"no first token found in tree of data '{tree.data}'"
            ),
        )

    @classmethod
    @strictly
    def fromtoken(cls: type, path: str, token: Token):  # -> Location:
        return cls(
            path,
            token.line,
            token.column,
        )

    @classmethod
    @strictly
    def unknown(cls: type, path: Optional[str] = None):
        return cls(path, "Unkown", "Unkown")


def unsupported_grammar(
    path: str,
    larkobj: Union[Tree, Token, object],
    message: str,
):

    loc = match(larkobj)[
        Tree : lambda: Location.fromtree(path, larkobj),
        Token : lambda: Location.fromtoken(path, larkobj),
        ... : lambda: Location.unknown(path),
    ]
    larkname = match(larkobj)[
        Tree : lambda: larkobj.data,
        Token : lambda: larkobj.type,
        ... : MatchError(f"expected a lark 'Tree' or 'Token', got a '{type(larkobj)}'"),
    ]

    return f"{str(loc)}: unsupported grammar for {larkname}, {message}"
