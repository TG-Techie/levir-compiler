# tout is a sugarless version of levir

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

from . import levir_builtins

LevirType = Union["UserType", "GenType", levir_builtins.BuiltinType]
LevirFunc = Union["Func", "GenFunc", levir_builtins.BuiltinFunc]

LevirItem = Union[LevirType, LevirFunc]


@enum
class ItemSpec:
    class infer:
        loc: Location

    class named:
        loc: Location

        isref: bool
        modpath: Tuple[str, ...]
        name: str
        gens: Tuple["ItemSpec", ...]

        def __str__(self):
            return (
                f"{'&'if self.isref else ''}"
                f"{'.'.join(self.modpath)+'.'if len(self.modpath) else ''}"
                f"{self.name}"
                f"{'['+','.join(self.gens)+']' if len(self.gens) else ''}"
            )

    class Self:
        loc: Location

    class func:
        # CHECK: isref cannot be true! it's a function (in future )
        loc: Location

        item: LevirFunc
        gens: Tuple["ItemSpec", ...]

    class type:
        loc: Location

        isref: bool
        item: LevirType
        gens: Tuple["ItemSpec", ...]


@enum
class MthdSpec:
    class named:
        loc: Location
        name: str

    class found:
        loc: Location
        mthd: "Method"


# T = TypeVar('T')
# @enum # working title
# class ComposedAttrs(Generic[T]):
#     # this is used for composing inheritance
#     #   the typed out new mbrs and overides go in new
#     #   once resolved the final dict holds a complete
#     #       list of what needs ot be output
#     class new:
#         attrs: Dict[str, T]
#     class final:
#         attrs: Dict[str, T]


bltn_mod = levir_builtins.module


class Module(DataVariable):
    name: str
    filename: str
    items: Dict[str, LevirItem] = _FactoryField(lambda: {})
    outer: Union["Module", levir_builtins.BuiltinModule] = _DefaultField(bltn_mod)


# HACK: until enums support chained data variants
_UserType_anotes = {
    "loc": Location,
    "mod": Module,
    "name": str,
    # found in resolved path
    "mbrs": Option[LevirType],
    "mthds": Option["Method"],
}


@enum
class UserType:
    # Type and Trait are not runtime instantiable
    # class Type:
    #     __annotations__ = _UserType_anotes

    class Trait:
        __annotations__ = {**_UserType_anotes}
        __annotations__.pop("mbrs")
        mthds = _DefaultField(Nothing)

    class Class:
        __annotations__ = {**_UserType_anotes}
        mbrs = _DefaultField(Nothing)
        mthds = _DefaultField(Nothing)

    class Struct:
        __annotations__ = {**_UserType_anotes}
        mbrs = _DefaultField(Nothing)
        mthds = _DefaultField(Nothing)

    # class Self:
    #     loc : Location
    #     mod : Module
    #     base_type: 'UserType' # for structs this is a reference that copies on get

    @classmethod
    @strictly  # working title
    def isstackvalue(cls: type) -> bool:
        global UserType
        return match(cls)[
            UserType.Struct : lambda: True,
            UserType.Type,
            UserType.Trait,
            UserType.Class : lambda: False,
        ]

    @classmethod
    @strictly  # working title
    def isheapvalue(cls: type) -> bool:
        global UserType
        return match(cls)[
            UserType.Class : lambda: True,
            UserType.Type,
            UserType.Trait,
            UserType.Struct : lambda: False,
        ]

    @classmethod
    @strictly  # working title
    def istranslatable(cls: type) -> bool:
        global UserType
        return match(cls)[
            UserType.Class,
            UserType.Struct : lambda: True,
            UserType.Type,
            UserType.Trait : lambda: False,
        ]


class Block(DataVariable):
    loc: Location
    stmts: Tuple["Stmt", ...]
    locals: Option[Dict[str, ItemSpec]] = _DefaultField(Nothing)


# non generic
class Func(DataVariable):
    loc: Location
    mod: Module

    name: str
    args: Dict[str, ItemSpec]
    rettype: ItemSpec
    block: "Block"

    calls: Dict[Tuple[LevirType], "Call"] = _FactoryField(lambda: {})

    # CHECK: frame ends in return
    # CHECK: all returns agree
    # CHECK: rettype is infer or Type


# non generic
class Mthd(Func):
    loc: Location
    mad: Module

    outer: ItemSpec
    name: str
    args: Dict[str, ItemSpec]
    rettype: ItemSpec
    block: "Block"

    calls: Dict[Tuple[LevirType], "Call"] = _FactoryField(lambda: {})

    # CHECK: assert outer is not a function


class Call(DataVariable):
    # must be concrete
    loc: Location  # ?? # locs: Set[Location]
    argtypes: Tuple[LevirType, ...]
    rettype: LevirType


@enum
class Stmt:
    class asn:
        loc: Location
        mod: Module
        subj: "Subject"
        expr: "Expr"

    class ret:
        loc: Location
        mod: Module
        expr: "Expr"

    class brk:
        loc: Location
        mod: Module

    class cont:
        loc: Location
        mod: Module

    class loop:
        loc: Location
        mod: Module
        block: Block

    class cond:
        loc: Location
        mod: Module
        clauses: Tuple["Clause", ...]

    class dropin:
        loc: Location
        mod: Module
        lang: str
        src: str

    class unreachable:
        loc: Location
        mod: Module
        msg: Option[str]

    class expr:
        loc: Location
        mod: Module
        expr: "Expr"

    def exits_block(self):
        # TODO: ret exits fame but should exit block too? i think yes
        #   then ret exitst block (locals) and after that is exits frame (args)
        global Stmt
        return match(self)[
            Stmt.ret,
            Stmt.brk,
            Stmt.cont : lambda: True,
            Stmt.asn,
            Stmt.loop,
            Stmt.cond,
            Stmt.dropin,
            Stmt.unreachable,
            Stmt.expr : lambda: False,
        ]

    def exits_frame(self):
        # TODO: ret exits fame but should exit block too? i think yes
        #   then ret exitst block (locals) and after that is exits frame (args)
        global Stmt
        return match(self)[
            Stmt.ret : lambda: True,
            Stmt.cont,
            Stmt.brk,
            Stmt.asn,
            Stmt.loop,
            Stmt.cond,
            Stmt.dropin,
            Stmt.unreachable,
            Stmt.expr : lambda: False,
        ]


@enum
class Subject:
    # class self:
    #     loc: Location
    #     mod: Module
    #     # base: ItemSpec.type
    #     # type: UserType.Self = _DerivedField(
    #     #     lambda self: UserType.Self.fromspec(self.specified_type)
    #     # )
    #
    #     @property
    #     def type(self):
    #         # later dfault this to infer??
    #         FUCK

    class var:
        loc: Location
        mod: Module
        name: str
        type: ItemSpec
        # CHECK: Itemspec must be type

    class mbr:
        loc: Location
        mod: Module
        var: "Subject.var"
        mbrs: Tuple[str, ...]
        type: ItemSpec


@enum
class Clause:
    # CHECK: conds must be bools
    class if_:
        loc: Location
        mod: Module
        cond: "Expr"
        block: Block

    class elif_:
        loc: Location
        mod: Module
        cond: "Expr"
        block: Block

    class else_:
        loc: Location
        mod: Module
        block: Block


@enum
class Expr:
    class get:
        loc: Location
        mod: Module
        subj: Subject
        type = property(lambda self: self.subj.type)

    class fncall:
        # item calls to type are sugar
        loc: Location
        mod: Module
        item: ItemSpec
        args: Tuple["Expr", ...]
        type: ItemSpec

    class mthdcall:
        loc: Location
        mod: Module
        subj: Subject
        mthd: MthdSpec
        args: Tuple["Expr", ...]
        type: ItemSpec

    class new:
        loc: Location
        mod: Module
        type: ItemSpec
        cntn: Dict[str, "Expr"]

    class litrl:
        loc: Location
        mod: Module
        type: ItemSpec
        src: str

    class not_:
        # logic only
        loc: Location
        mod: Module
        expr: "Expr"

    class _or_:
        # logic only
        loc: Location
        mod: Module
        exprs: Tuple["Expr", "Expr"]

    class _and_:
        # logic only
        loc: Location
        mod: Module
        exprs: Tuple["Expr", "Expr"]

    class dropin:
        loc: Location
        mod: Module
        lang: str
        src: str
