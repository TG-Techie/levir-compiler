from strictly import *
from envly import *
from typing import *
from envly._data_variable import DataVariable, \
    _DefaultField, _DerivedField, _FactoryField

from levir.lexer_parser import (
    Location, Tree, Token,
    parse_str, namefrom,
    unsupported_grammar, reconstruct
)

# once done with checks, sort by line number (and id number)

from . import levir_builtins

@enum
class CheckIssue:

    class error:
        loc: Location
        message: str

    class warning:
        loc: Location
        message: str

CheckResult = Result[Set[CheckIssue], str]

class Item(DataVariable):
    pass

@enum
class TypeIdent:

    class named:
        loc: Location
        name: str
        _by_ref: bool

        def __str__(self) -> str:
            return ''
            return f"`{'&'if self.isref() else ''}{self.name}`"

        def __eq__(self, other):
            return (self.isref() == other.isref()) and self.name == other.name

    class found:
        loc         : Location
        type        : Union['UserType', levir_builtins.BuiltinType]
        _by_ref     : bool
        _resolved   : bool      = _DefaultField(False)
        _checked    : bool      = _DefaultField(False)

        @strictly
        def check(self) -> CheckResult:
            global Class
            reports = set()
            if self.isref() and isinstance(self.type, Class):
                reports.add(CheckIssue.Error(self.loc,
                    f"classes cannot be referenced (they are alredy reference)"
                ))
            return Okay(reports)

        def __str__(self) -> str:
            # return f'X{self.type.name}'
            return f"{'&'if self.isref() else ''}{self.type.name}"

        def __eq__(self, other):
            return (self.isref() == other.isref()) and self.type == other.type

    class infer:
        pass

    @strictly
    def __new__(cls, loc:Location, obj:object, by_ref:bool):# -> 'TypeIdent':
        global str, UserType, match
        return match(obj)[
            str      : lambda: cls.named(obj, loc, by_ref),
            UserType : lambda: cls.found(obj, loc, by_ref),
            ... : TypeError(f"{cls.__name__} cannot make from an object of " \
                f"type '{type(obj).__name__}'"
            )
        ]

    def isref(self):
        return self._by_ref

    def resolvefrom(self, mod:'Module') -> Result['TypeIdent', str]:
        global TypeIdent
        return Okay(match(self)[
            TypeIdent.named  : lambda loc, name, ref: TypeIdent.found(
                loc, ~mod.find(name), ref
            ),
            TypeIdent.found  : lambda *_: self,
            TypeIdent.infer : ...
        ])

    @classmethod
    def fromtree(cls:type, mod:'Module', sometypetree:Tree):
        assert sometypetree.data in ('type', 'mbrtype', 'vartype', 'rettype', 'outtype'), \
            f"unable to make TypeIdent from tree of data '{sometypetree.data}'"
        # filter for raw 'type' data
        typetree = match(sometypetree.data)[
            'type', : lambda: sometypetree,
            'mbrtype', 'vartype', 'rettype', 'outtype' : lambda: sometypetree.children[0],
             ... : MatchError(
                f"unable to find match for tree of data '{sometypetree.data}'"
            )
        ]

        ref, identtok = match(len(typetree.children))[
            1 : lambda: (False, typetree.children[-1]),
            2 : lambda: (True, typetree.children[-1]),
            ... : lambda: unsupported_grammar(
                mod.filename, sometypetree,
                f"the grammar for type '{reconstruct(sometypetree)}'"
            )
        ]

        return Okay(cls(
            Location.fromtree(mod.filename, sometypetree),
            namefrom(identtok),
            ref
        ))

    @classmethod
    def seqfromlisttree(cls:type, mod:'Module', pairstree:Tree) -> Dict[str, 'TypeIdent']:
        # unwrap list if it is wrapped in mbrs or args
        if pairstree.data != 'list':
            assert len(pairstree.children) <= 1, unsupported_grammar(
                mod.filename, pairstree, f"cannot make a TypeIdent "
                f"sequence from a tree of type '{pairstree.data}' with "
                f"{len(pairstree.children)} subtrees, expected 0-1"
            )
            if len(pairstree.children) == 0:
                return Okay({})
            else:
                listtree, = pairstree.children

        return Okay({
            namefrom(nameident) : ~TypeIdent.fromtree(mod, typetree)
            for nameident, typetree in
                (pair.children for pair in listtree.children)
        })

# items, etc
class Module(DataVariable):
    #source: 'TextIO'
    _filename   : str
    _outer      : 'Module'
    items       : Dict[str, 'Union[UserType, Func]']= _FactoryField(dict)
    _resolved   : bool = _DefaultField(False)
    _checked    : bool = _DefaultField(False)

    _bltn_mod = levir_builtins.module

    @property
    def filename(self):
        return self._filename

    def isresolved(self):
        return self._resolved

    @strictly
    def find(self, name:str) -> Option[Item]:
        #return Option(self.items.get(name, None))
        if name in self.items:
            return Some(self.items[name])
        elif self._outer is not None: # add an elif for other modules
            return self._outer.find(name)
        else:
            return self._bltn_mod.find(name)

    @strictly
    def has(self, name:str) -> bool:
        return name in self.items

    def iteritems(self) -> Iterable[Union['UserType', 'Func']]:
        return self.items.values()

    @strictly
    def check(self) -> Result[None, str]:
        reports = set()
        for name, item in self.items.items():
            reports |= ~item.check()
        self._checked = True
        if not len(reports):
            return Okay(None)
        else:
            [print(str(report.loc), report.message) for report in reports]
            CHECK_FAILED

    @strictly
    def resolve(self) -> Result[None, str]:
        for name, item in self.items.items():
            ~item.resolve(self)
        else:
            self._resolved = True
            return Okay(None)

    @classmethod
    @strictly
    def fromfile(cls:type, file) -> Result['Module', None]:
        with file:
            tree = parse_str(file.read())

        deftrees = [itemtree.children[0] for itemtree in tree.children]

        mod = cls(file.name, None)
        items = mod.items

        for deftree in deftrees:
            item = ~match(deftree.data)[
                'classdef'  : lambda: Class.fromtree(mod, deftree),
                'structdef' : lambda: Struct.fromtree(mod, deftree),#Error('structdef not implemented yet'),#translate_classdef(mod, ),
                'fndef'     : lambda: Func.fromtree(mod, deftree),#Error('funcdef not implemented yet'),#translate_classdef(mod, ),
                'mthddef'   : lambda: Mthd.fromtree(mod, deftree),
                ... : MatchError(f"default case hit, unknown feature '{deftree.data}'"),
            ]
            items[item.name] = item
        else:
            return Okay(mod)

# maybe change to enum?
class UserType(Item):
    loc: Location
    name: str
    mbrs: Dict[str, TypeIdent]

    @strictly
    def check(self) -> CheckResult:
        reports = set()
        for name, mbrtype in self.mbrs.items():
            reports |= ~mbrtype.check()
            if mbrtype.isref():
                reports.add(CheckIssue.Error(mbrtype.loc,
                    f"members must be structs or classes, not a reference." \
                    f"found `{self.name}.{mbrtype.type.name}` as a reference, "\
                    "(remove the `&`)"
                ))
            return Okay(reports)

        return Okay(reports)


    def resolve(self, mod:Module) -> Result[None, str]:
        self.mbrs = {
            name : ~ident.resolvefrom(mod) \
            for name, ident in self.mbrs.items()
        }
        return Okay(None)

    @classmethod
    @strictly
    def fromtree(cls: type, mod:Module, typetree:Tree) -> Result['Type', None]:
        assert len(typetree.children) == 2, unsupported(
            mod.filename, typetree, f"this version of levir only supports "\
                f" 2 trees, found {len(typetree.children)}"
        )

        nametree, mbrstree = typetree.children

        return Okay(cls(
            Location.fromtree(mod.filename, typetree),
            namefrom(nametree),
            ~TypeIdent.seqfromlisttree(mod, mbrstree)
        ))

class Class(UserType):

    def isclass(self):
        return True

    def isstruct(self):
        return False

class Struct(UserType):

    @strictly
    def check(self) -> CheckResult:
        reports = ~super().check()
        # check for nested structs
        ~self._check_infinite_struct({})
        return Okay(reports)


    def _check_infinite_struct(self, aboves:Set['Struct']) -> CheckResult:
        # TODO: impl infinate struct check
        return Okay(None)
        '''aboves.reports.add(self)
        # only check members that are structs
        tocheck = (
            (name, mbrtype) for name, mbrtype in \
            self.mbrs.items() if mbrtype.isstruct()
        )
        # check that is not in an above struct
        for name, mbrtype in tocheck:'''




    def isclass(self):
        return False

    def isstruct(self):
        return True

class Func(Item):
    loc     : Location
    name    : str
    rettype : TypeIdent
    args    : Dict[str, TypeIdent]
    locals  : Dict[str, TypeIdent]
    frame   : 'Frame'

    @strictly
    def getvartype(self, name:str) -> Option['LevirType']:
        if name in self.args:
            return Some(self.args[name])
        elif name in self.locals:
            return Some(self.locals[name])
        else:
            return Nothing


    @strictly
    def check(self) -> CheckResult:
        reports = set()
        if self.rettype.isref():
            reports.add(CheckIssue.error(self.rettype.loc,
                f"struct references cannot be returned"
            ))
        # TODO: func, check return termination

        # check that args and locals do not share the same vars
        for argname in self.args:
            if argname in self.locals:
                reports.append( self.loc,
                    f"duplicate variable '{arganme}' in args and locals for " \
                    f"function '{self.name}'. Variables may be locals or " \
                    f"arguemnts, not both."
                )
        for name, argtype in self.args.items():
            reports |= ~argtype.check()
        for name, lcltype in self.locals.items():
            reports |= ~lcltype.check()
        reports |= ~self.frame.check(self)
        return Okay(reports)

    @strictly
    def resolve(self, mod:Module) -> Result[None, str]:
        self.rettype = ~self.rettype.resolvefrom(mod)
        # SEMANT: functions cannot returnstruct refences
        self.args = {
            name : ~ident.resolvefrom(mod)
            for name, ident in self.args.items()
        }
        self.locals = {
            name : ~ident.resolvefrom(mod)
            for name, ident in self.locals.items()
        }
        ~self.frame.resolve(mod)
        return Okay(None)

    @classmethod
    @strictly
    def fromtree(cls: Type, mod: Module, fntree:Tree) -> Result['Func', None]:
        assert len(fntree.children) == 5, unsupported_grammar(
            mod.filename, fntree, f"this funciton grammar is not yet supported"
        )
        nametree, rettypetree, argstree, lclstree, frametree = fntree.children

        return Okay(cls(
            loc     = Location.fromtree(mod.filename, fntree),
            name    = namefrom(nametree),
            rettype = ~TypeIdent.fromtree(mod, rettypetree),
            args    = ~TypeIdent.seqfromlisttree(mod, argstree),
            locals  = ~TypeIdent.seqfromlisttree(mod, lclstree),
            frame   = ~Frame.fromtree(mod, frametree)
        ))

class Mthd(Func):
    loc     : Location
    outtype : TypeIdent
    name    : str
    rettype : TypeIdent
    args    : Dict[str, TypeIdent]
    locals  : Dict[str, TypeIdent]
    frame   : 'Frame'


    @classmethod
    @strictly
    def fromtree(cls: Type, mod: Module, mthdtree:Tree) -> Result['Mthd', None]:
        assert len(mthdtree.children) == 6, unsupported_grammar(
            mod.filename, fntree, f"this funciton grammar is not yet supported"
        )
        outtype, nametree, rettypetree, argstree, lclstree, frametree = mthdtree.children

        return Okay(cls(
            loc     = Location.fromtree(mod.filename, mthdtree),
            outtype = ~TypeIdent.fromtree(mod, outtype),
            name    = namefrom(nametree),
            rettype = ~TypeIdent.fromtree(mod, rettypetree),
            args    = ~TypeIdent.seqfromlisttree(mod, argstree),
            locals  = ~TypeIdent.seqfromlisttree(mod, lclstree),
            frame   = ~Frame.fromtree(mod, frametree)
        ))

    @strictly
    def resolve(self, mod:Module) -> Result[None, str]:
        ~super().resolve(mod)
        self.outtype = match(self.outtype)[
            TypeIdent.name : lambda _, name, *__: mod.find(name),
            TypeIdent.type : ... # passthorught
        ]
        return Okay(None)

class Frame(DataVariable):
    loc     : Location
    stmts   : Tuple['Stmt']

    @strictly
    def check(self, func:Func) -> CheckResult:
        reports = set()
        for stmt in self.stmts:
            reports |= ~stmt.check(func)
        return Okay(reports)

    def resolve(self, mod:Module) -> Result[None, str]:
        for stmt in self.stmts:
            ~stmt.resolve(mod)
        else:
            return Okay(None)

    @classmethod
    @strictly
    def fromtree(cls:type, mod:Module, frametree:Tree) -> Result['Frame', str]:
        assert frametree.data == 'frame', \
            f"incorrect tree type, found '{frametree.data}'"
        ls = tuple(~Stmt.fromtree(mod, tree) for tree in frametree.children)
        return Okay(cls(
            loc   = Location.fromtree(mod.filename, frametree),
            stmts = ls
        ))

@enum
class Subject:
    class var:
        loc  : Location
        name : str
        type : TypeIdent

        def check(self, func:Func) -> CheckResult:
            results = set()

            opt_vartype = func.getvartype(self.name)

            if isvariant(opt_vartype, Some): # we know it is
                vartype = ~opt_vartype
                if self.type != vartype:
                    results.add(CheckIssue.error(self.loc,
                        f"type of variable '{self.name}' declared as type "\
                        f"'{vartype.name}' but used as '{self.type.name}'"
                    ))
            else:
                results.add(CheckIssue.error(self.loc,
                    f"variable '{self.name}' used without declaration, must " \
                    f"be an argument or local."
                ))
            return Okay(results)

        @strictly
        def resolve(self, mod:Module) -> Result[None, str]:
            self.type = ~self.type.resolvefrom(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, vartree:Tree) -> Result['Subject.var', str]:
            assert vartree.data == 'var', unsupported_grammar(
                mod.filename, vartree,
                f"expected a var(...) tree, found a '{vartree.data}'"
            )
            nametree, typetree = vartree.children
            return Okay(cls(
                loc  = Location.fromtree(mod.filename, vartree),
                name = namefrom(nametree),
                type = ~TypeIdent.fromtree(mod, typetree)
            ))

    class mbrof:
        loc: Location
        varname: str
        vartype: TypeIdent
        mbrs: Dict[str, TypeIdent]

        @property
        def type(self): # -> LevirType:
            return tuple(self.mbrs.values())[-1]

        @strictly
        def check(self, func:Func) -> CheckResult:
            results = set()
            results |= ~self.type.check()
            for mbrname, ident in self.mbrs.items():
                results |= ~ident.check()
            # check that each type has availble members
            outertype = self.vartype
            for mbrname, foundtype in self.mbrs.items():
                if mbrname not in outertype.type.mbrs:
                    results.add(CheckIssue.error(foundtype.loc,
                        f"type '{outertype}' has no member '{mbrname}'"
                    ))
                    return Okay(results)
                mbrtype = outertype.type.mbrs[mbrname]
                if mbrtype != foundtype:
                    results.add(CheckIssue.error(foundtype.loc,
                        f"member '{mbrname}' of type '{outertype}' is of type " \
                        f"'{mbrtype}' not '{foundtype}'"
                    ))
                    return Okay(results)
                outertype = mbrtype
            return Okay(results)

        def resolve(self, mod:Module) -> Result[None, str]:
            self.vartype = ~self.vartype.resolvefrom(mod)
            self.mbrs = {
                name : ~ident.resolvefrom(mod)
                for name, ident in self.mbrs.items()
            }
            return Okay(None)

        @classmethod
        def _fromtree(cls:type, mod:Module, mbroftree:Tree):
            assert len(mbroftree.children) == 3, unsupported_grammar(
                mod.filename, mbroftree,
                f"expected 3 attribues, found {len(mbroftree.children)}"
            )

            varnametree, typetree, mbrspectree = mbroftree.children
            children = mbrspectree.children

            mbrs = match(mbrspectree.data)[
                'mbr'   : lambda: {
                    namefrom(children[0]) : ~TypeIdent.fromtree(mod, children[-1])
                },
                'mbrs'  : lambda: ~TypeIdent.seqfromlisttree(mod, mbrspectree),
                ...     : MatchError(
                    f"unable to match '{mbrspectree.data}'"
                )

            ]
            vt = ~TypeIdent.fromtree(mod, typetree)
            loc = Location.fromtree(mod.filename, mbroftree)
            return Okay(cls(
                loc     = loc,
                varname = namefrom(varnametree),
                vartype = vt,
                mbrs    = mbrs,
            ))

    @classmethod
    @strictly
    def fromtree(cls:type, mod:Module, subjtree:Tree) -> Result['Subject', str]:
        return Okay(match(subjtree.data)[
            'subject' : lambda: ~Subject.fromtree(mod, subjtree.children[0]),
            'var'     : lambda: ~Subject.var._fromtree(mod, subjtree),
            'mbrof'   : lambda: ~Subject.mbrof._fromtree(mod, subjtree),
            ...       : MatchError(unsupported_grammar(
                mod.filename, subjtree,
                f"unknown kind of subject '{subjtree.data}'"
            ))
        ])

@enum
class BinOp:
    class add: pass
    class sub: pass
    class mul: pass
    class div: pass
    class pow: pass

    @classmethod
    def fromtree(cls:type, mod:Module, tree:Tree) -> Result['BinOp', None]:
        global BinOp
        return Okay(match(tree.data)[
            'add' : lambda: BinOp.add,
            'sub' : lambda: BinOp.sub,
            'mul' : lambda: BinOp.mul,
            'div' : lambda: BinOp.div,
            'pow' : lambda: BinOp.pow,
             ...  : MatchError(
                f"no known operation for '{tree.data}'"
             )
        ])

    def __str__(self) -> str:
        global BinOp
        return match(self)[
            BinOp.add : lambda: 'add',
            BinOp.sub : lambda: 'sub',
            BinOp.mul : lambda: 'mul',
            BinOp.div : lambda: 'div',
            BinOp.pow : lambda: 'pow',
        ]

@enum
class Expr:
    # all share .type property

    class get:
        loc  : Location
        subj : Subject
        type : str

        @strictly
        def check(self, func:Func) -> CheckResult:
            return Okay(~self.subj.check(func))
            #results = set()
            #results |= ~self.subj.check(func)
            #return Okay(results)

        def resolve(self, mod:Module) -> Result[None, str]:
            ~self.subj.resolve(mod)
            self.type = ~self.type.resolvefrom(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, gettree:Tree):
            assert len(gettree.children) in (1, 2), unsupported_grammar(
                mod.filename, gettree,
                f"found {len(gettree.children)} attribues, expected 1 or 2"
            )

            # INFER
            if len(gettree.children) == 2:
                subjtree, typetree = gettree.children
                ident = ~TypeIdent.fromtree(mod, typetree)
            else:
                subjtree,  = gettree.children
                ident = TypeIdent.infer

            subj = ~Subject.fromtree(mod, subjtree)
            if isvariant(ident, TypeIdent.infer):
                ident = subj.type

            return Okay(cls(
                loc  = Location.fromtree(mod.filename, gettree),
                subj = subj,
                type = ident,
            ))

    class fncall: pass
    class mthdcall: pass
    class new:
        loc  : Location
        type : TypeIdent
        cntn : Tuple['Expr']

        @strictly
        def check(self, func:Func) -> CheckResult:
            results = set()
            for expr in self.cntn:
                results |= ~expr.check(func)
            return Okay(results)

        def resolve(self, mod:Module) -> Result[None, str]:
            self.type = ~self.type.resolvefrom(mod)
            for expr in self.cntn:
                ~expr.resolve(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, newtree:Tree):
            assert len(newtree.children) == 2, unsupported_grammar(
                mod.filename, newtree,
                f"found {len(newtree.children)} attribues, expected 2"
            )

            typetree, cntntree = newtree.children
            cntnlist = cntntree.children[0]
            return Okay(cls(
                loc  = Location.fromtree(mod.filename, newtree),
                type = ~TypeIdent.fromtree(mod, typetree),
                cntn = tuple(
                    ~Expr.fromtree(mod, tree) for tree in cntnlist.children
                )
            ))

    class litrl:
        loc: Location
        type: TypeIdent
        src: str

        @strictly
        def check(self, func:Func) -> CheckResult:
            return Okay(set())

        def resolve(self, mod:Module) -> Result[None, str]:
            self.type = ~self.type.resolvefrom(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, litrltree:Tree) -> Result['Expr.litrl', None]:
            assert len(litrltree.children) == 2, unsupported_grammar(
                mod.filename, litrltree,
                f"found {len(litrltree.children)} attribues, expected 2"
            )

            typetree, srctree = litrltree.children
            return Okay(cls(
                loc  = Location.fromtree(mod.filename, litrltree),
                type = ~TypeIdent.fromtree(mod, typetree),
                src  = reconstruct(srctree)
            ))

    class binop:
        loc: Location
        op: BinOp
        a: 'Expr'
        b: 'Expr'
        type: TypeIdent

        @strictly
        def check(self, func:Func) -> CheckResult:
            results = ~self.a.check(func)
            results |= ~self.b.check(func)
            results |= ~self.type.check()
            # TODO: add check that the expr types comply w/ adding, etc
            return Okay(results)

        def resolve(self, mod:Module) -> Result[None, str]:
            self.type = ~self.type.resolvefrom(mod)
            ~self.a.resolve(mod)
            ~self.b.resolve(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, litrltree:Tree):
            assert len(litrltree.children) == 4, unsupported_grammar(
                mod.filename, litrltree,
                f"found {len(litrltree.children)} attribues, expected 4"
            )

            optree, atree, btree, typetree = litrltree.children
            return Okay(cls(
                loc  = Location.fromtree(mod.filename, litrltree),
                op = ~BinOp.fromtree(mod, optree),
                a = ~Expr.fromtree(mod, atree),
                b = ~Expr.fromtree(mod, btree),
                type = ~TypeIdent.fromtree(mod, typetree),
            ))

    @classmethod
    @strictly
    def fromtree(cls:type, mod:Module, exprtree:Tree):
        return match(exprtree.data)[
            'expr'          : lambda: Expr.fromtree(mod, exprtree.children[0]),
            'get_expr'      : lambda: Expr.get._fromtree(mod, exprtree),
            'fncall_expr'   : lambda: Expr.fncall._fromtree(mod, exprtree),
            'mthdcall_expr' : lambda: Expr.mthdcall._fromtree(mod, exprtree),
            'new_expr'      : lambda: Expr.new._fromtree(mod, exprtree),
            'litrl_expr'    : lambda: Expr.litrl._fromtree(mod, exprtree),
            'arith_expr'    : lambda: Expr.binop._fromtree(mod, exprtree),
            ...             : MatchError(unsupported_grammar(
                mod.filename, exprtree,
                f"cannot compile unknown kind of expression"
            ))
        ]

@enum
class Clause:
    class _if:
        loc: Location
        cond: Expr
        frame: Frame
    class _elif:
        loc: Location
        cond: Expr
        frame: Frame
    class _else:
        loc: Location
        frame: Frame

    @strictly
    def check(self, func:Func) -> CheckResult:
        global Clause
        reports = set()

        if isvariant(self, (Clause._if, Clause._elif)):
            if self.cond.type.type is not levir_builtins.module.items['bool']:
                reports.add(CheckIssue.error( self.cond.type.loc,
                    f"if/elif condition must of type 'bool', found '{self.cond.type.type.name}'"
                ))

        # check sub objs
        reports |= match(self)[
            Clause._if, Clause._elif : lambda _, cond, frame: (
                ~cond.check(func) | ~frame.check(func)
            ),
            Clause._else: lambda _, frame: ~frame.check(func)
        ]

        return Okay(reports)


    @strictly
    def resolve(self, mod:Module) -> Result[None, str]:
        global Clause
        match(self)[
            Clause._if, Clause._elif : lambda _, cond, frame:(
                ~cond.resolve(mod), ~frame.resolve(mod)
            ),
            Clause._else : lambda _, frame: ~frame.resolve(mod)
        ]
        return Okay(None)

    @classmethod
    @strictly
    def fromtree(cls:type, mod:Module, tree:Tree) -> Result['Clause', str]:
        global Clause
        assert tree.data in ('if', 'elif', 'else'), unsupported_grammar(
            mod.filename, tree,
            f"unknown conditional clause kind '{tree.data}' "
        )

        loc = Location.fromtree(mod.filename, tree)

        if len(tree.children) == 2:
            condtree, frametree = tree.children
            cond = ~Expr.fromtree(mod, condtree)
            frame = ~Frame.fromtree(mod, frametree)
        elif len(tree.children) == 1:
            frametree, = tree.children
            frame = ~Frame.fromtree(mod, frametree)
        else:
            FUCK # unreachable

        return Okay(match(tree.data)[
            'if', 'elif' : lambda: Clause._if(loc, cond, frame),
            #'elif' : lambda: Clause._elif(loc, cond, frame),
            'else' : lambda: Clause._else(loc, frame),
            ... : MatchError(
                f"how did cond clause '{tree.data}' get past the above asser"
            )
        ])

@enum
class Stmt:
    class asn:
        loc     : Location
        subj    : Subject
        expr    : Expr
        asntype : TypeIdent

        @strictly
        def check(self, func:Func) -> CheckResult:
            reports = set()
            reports |= ~self.subj.check(func)
            reports |= ~self.expr.check(func)
            reports |= ~self.asntype.check()
            # check that all three types match
            #p_rint(
            #     repr(self.asntype.type), '\n',
            #     repr(self.expr.type.type), '\n',
            #     repr(self.subj.type.type)
            #)

            # p_rint(f"{self.asntype == self.expr.type=}")

            if self.asntype != self.expr.type or self.asntype != self.subj.type:
                reports.add(CheckIssue.error(self.asntype.loc,
                    f"assignment types do not match, found '{self.asntype}', "\
                    f"'{self.subj.type}', and '{self.expr.type}'"
                ))

            # consider if struct refs can be assigned
            '''if self.asntype.isref():
                reports.add(CheckIssue.error(self.loc,
                    f"cannot assign struct references"
                ))'''
            return Okay(reports)

        @strictly
        def resolve(self, mod:Module) -> Result[None, str]:
            ~self.subj.resolve(mod)
            ~self.expr.resolve(mod)
            self.asntype = ~self.asntype.resolvefrom(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, asntree:Tree):
            assert len(asntree.children) in (2, 3), unsupported_grammar(
                mod.filename, asntree,
                f"got {len(asntree.children)} attribues, expected 2 or3"
            )
            if len(asntree.children) == 3:
                subjtree, exprtree, typetree = asntree.children
                typeident = ~TypeIdent.fromtree(mod, typetree)
            elif len(asntree.children) == 2:
                subjtree, exprtree = asntree.children
                typeident = TypeIdent.infer

            # INFER
            subj = ~Subject.fromtree(mod, subjtree)
            if isvariant(typeident, TypeIdent.infer):
                typeident = subj.type

            return cls(
                loc  = Location.fromtree(mod.filename, asntree),
                subj = subj,
                expr = ~Expr.fromtree(mod, exprtree),
                asntype = typeident
            )

    class ret:
        loc     : Location
        expr    : Expr
        rettype : TypeIdent

        @strictly
        def check(self, func:Func) -> CheckResult:
            return Okay(~self.rettype.check() | ~self.expr.check(func))

        @strictly
        def resolve(self, mod:Module) -> Result[None, str]:
            ~self.expr.resolve(mod)
            self.rettype = ~self.rettype.resolvefrom(mod)
            return Okay(None)

        @classmethod
        @strictly
        def _fromtree(cls:type, mod:Module, rettree:Tree):
            assert len(rettree.children) in (1, 2), unsupported_grammar(
                mod.filename, rettree,
                f"got {len(rettree.children)} attribues, expected 1 or2"
            )

            # INFER
            if len(rettree.children) == 2:
                exprtree, typetree = rettree.children
                ident = ~TypeIdent.fromtree(mod, typetree)
            elif len(rettree.children) == 1:
                exprtree, = rettree.children
                ident = TypeIdent.infer
            else:
                FUCK

            expr = ~Expr.fromtree(mod, exprtree)
            if isvariant(ident, TypeIdent.infer):
                ident = expr.type

            return cls(
                loc  = Location.fromtree(mod.filename, rettree),
                expr = expr,
                rettype = ident,
            )

    class brk:
        loc: Location
    class cont:
        loc: Location
    class loop:
        loc: Location
    #class dbg:
    #    loc: Location
    #class btw:
    #    loc: Location

    class dropin:
        # dropin is only a bootstrapping tool
        loc: Location
        lang: str
        src: str

        @strictly
        def check(self, func:Func) -> CheckResult:
            return Okay(set())

        @strictly
        def resolve(self, mod:Module) -> Result[None, str]:
            return Okay(None)

        @classmethod
        @strictly
        def fromtree(cls:type, mod:Module, tree:Tree) -> Result['Stmt.dropin', str]:
            assert len(tree.children) == 2, unsupported_grammar(
                mod.filename, tree,
                f"found '{len(tree.children)}' attributes, expected 2"
            )

            langtok, srctok = tree.children

            return Okay(cls(
                loc  = Location.fromtree(mod.filename, tree),
                lang = str(langtok).strip('"' + "'"),
                src  = str(srctok).strip("`")
            ))

    class cond:
        loc: Location
        clauses: Tuple[Clause]

        @strictly
        def check(self, func:Func) -> CheckResult:
            reports = set()
            for clause in self.clauses:
                reports |= ~clause.check(func)
            return Okay(reports)

        @strictly
        def resolve(self, mod:Module) -> Result[None, str]:
            [~clause.resolve(mod) for clause in self.clauses]
            return Okay(None)

        @classmethod
        @strictly
        def fromtree(cls:type, mod:Module, tree:Tree) -> Result['Stmt.cond', str]:
            assert len(tree.children), unsupported_grammar(
                mod.filename, tree,
                f"expected 1 or more clauses in conditional, found {len(tree.children)}"
            )

            return Okay(cls(
                loc = Location.fromtree(mod.filename, tree),
                clauses = tuple(
                    ~Clause.fromtree(mod, clausetree)
                        for clausetree in tree.children
                )
            ))

    @classmethod
    @strictly
    def fromtree(cls:type, mod:Module, tree:Tree) -> Result['Stmt', str]:
        global Stmt
        return Okay(match(tree.data)[
            'stmt'        : lambda: ~Stmt.fromtree(mod, tree.children[0]),
            'asn_stmt'    : lambda: Stmt.asn._fromtree(mod, tree),
            'ret_stmt'    : lambda: Stmt.ret._fromtree(mod, tree),
            'brk_stmt'    : lambda: Stmt.brk._fromtree(mod, tree),
            'cont_stmt'   : lambda: Stmt.cont._fromtree(mod, tree),
            'loop_stmt'   : lambda: Stmt.loop._fromtree(mod, tree),
            'dropin_stmt' : lambda: ~Stmt.dropin.fromtree(mod, tree),
            #'btw_stmt'    : lambda: Stmt.btw._fromtree(mod, tree),
            'cond_stmt'   : lambda: ~Stmt.cond.fromtree(mod, tree),
            ...           : MatchError(
                f"no case for '{tree.data}' in constructing a stmt"
            )
        ])
