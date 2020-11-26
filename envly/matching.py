from typing import *

from .env import *
from ._data_variable import DataVariable

import types

__all__ = (
    'match', 'Case', 'Action', 'Pattern',
    'CoverageError', 'InferenceError', 'MatchError'
)

class CoverageError(Exception):
    pass

class InferenceError(Exception):
    pass

class MatchError(Exception):
    pass

# type of thing to match and thing that match returns
M, R = TypeVar('M'), TypeVar('R')

PatternSyntax = Tuple[Union[slice, object], ...]

DEBUG = False
def debug(expr):
    global DEBUG
    if DEBUG:
        if callable(expr):
            vals = expr()
            if not isinstance(vals, Tuple):
                vals = (vals,)
        else:
            vals = (expr,)
        print(*vals)
    else:
        pass
    return

# class F:
#    def __class_getitem__(cls, x): return x
#    def __getitem__(self, x): return x

def cases_to_str(seq: Sequence['Case']):
    global case_to_str
    return '{'+(', '.join(case_to_str(each) for each in seq))+'}'

def case_to_str(some_case) -> str:
    global Case
    if some_case is Case.default:
        return '...'
    elif isinstance(some_case, (Case.is_a, Case.is_in, Case.equals, Case.enum)):
        return repr(some_case._attrs_()[0])
    elif isinstance(some_case, Case.check):
        return f"{some_case.fn.__name__}(...)"
    elif some_case is Case.is_this(True) or some_case is Case.is_this(False):
        return repr(some_case.obj)
    else:
        return repr(some_case)

@enum
class Case:

    class default:

        def matches(self, obj: object) -> bool:
            return True

    class is_a:
        kind: type
        # this is infered from non enum types
        def matches(self, obj: object) -> bool:
            return isinstance(obj, self.kind)

    class is_in:
        sequence: Sequence
        # this is infered from range and list
        def matches(self, obj: object) -> bool:
            return obj in self.sequence

    class equals:
        value: object
        # this is infered from anything taht is not otherwise infered
        def matches(self, obj: object) -> bool:
            return obj == self.value

    class is_this:
        obj: object

        def matches(self, obj: object) -> bool:
            return obj is self.obj

        def __eq__(self, other: 'Case') -> bool:
            global Case
            if isinstance(other, Case.is_this):
                return self.obj is other.obj
            elif isinstance(other, Case.is_this):
                return self.obj is other.value
            else:
                return False

        def __hash__(self):
            global Case
            return super(Case.is_this, self).__hash__()

    class subclasses:
        cls: type

        def match(self, obj: object) -> bool:

            return isinstance(obj, type) and issubclass(obj, self.cls)

    class check:
        fn: Callable[[object], bool]

        def matches(self, obj: object) -> bool:
            return self.fn(obj)

    class enum:
        variant: Union[EnumVariantClass, EnumVariant]

        def matches(self, obj: object) -> bool:
            return isvariant(obj, self.variant)
            '''variant = self.variant
            if isinstance(variant, EnumVariantClass):
                return isinstance(obj, variant)
            elif isinstance(variant, EnumSingleVariant):
                return obj is variant
            else:
                raise TypeError(f"{self} 's enum must be an enum single-"\
                    f"variant (like Option.Nothing) or enum variant (like "\
                    f"Option.Some), found {variant}"
                )'''

    @classmethod # inference constructor
    def infer(cls, obj:object) -> 'Case':
        global Case, isinstance, Ellipsis
        if obj is Default or obj is Ellipsis:
            return Case.default
        elif isinstance(obj, (bool, type(None))):
            return Case.is_this(obj)
        elif isinstance(obj, (EnumVariantClass, EnumSingleVariant)):
            return Case.enum(variant=obj)
        elif isinstance(obj, type):
            return Case.is_a(kind=obj)
        # is a dict/MappingProxyType -> needs own thing?
        elif isinstance(obj, (range, types.GeneratorType)):
            return Case.is_in(sequence=obj)
        elif callable(obj):
            return Case.check(fn=obj)
        else:
            return Case.equals(value=obj)

@enum
class Action:
    class passthrough:

        def take(self, obj: object) -> object:
            return obj

    class expr:
        fn: Callable[..., object]

        def take(self, obj: object) -> object:
            if isinstance(obj, EnumDataVariant):
                return self.fn(*obj._attrs_())
            else:
                return self.fn()

    class error:
        exc: Exception

        def take(self, _):
            raise self.exc


    @classmethod
    def infer(cls, obj: object) -> 'Action':
        global Action
        if isinstance(obj, Action):
            return obj
        elif obj is ...:
            return Action.passthrough
        elif isinstance(obj, Exception) \
            or isinstance(obj, type) and issubclass(obj, Exception):
            return Action.error(obj)
        elif callable(obj):
            return Action.expr(fn=obj)
        else:
            raise InferenceError(f"unable to infer action to take based on "\
                f"`{repr(obj)}`, prefix with `lambda:` to return it as a value"
            )

class Pattern(DataVariable, Generic[M]):
    pairs: Dict[Case, Action]

    _bool_cases = Case.is_this(True), Case.is_this(False)

    def __iter__(self) -> Iterable:
        return iter(self.pairs.items())

    def __repr__(self) -> str:
        patterns = ''.join(f"    {case_to_str(case)}:{action},\n" for case, action in self)
        return f"{type(self).__name__}[\n{patterns}]"

    def covers(self, to:M) -> Result[Union[None, str], str]: # Result.okay = passes,
        global Case, match, Okay, Error, debug
        debug(lambda: 'checking pattern coverage')
        if isinstance(to, Enum) and to._enum_cls_ not in self:
            debug('mathcing to an enum instance')
            # check to see that all of
            if Case.default in self:
                return Okay('enum with default')
            else: # check if full coverage
                covered = set(each for each in self.cases() if isinstance(each, (EnumVariant, EnumVariantClass)))
                varnt_cases = set(Case.infer(varnt) for varnt in to._enum_varnts_.values())
                #debug(lambda: (covered < varnt_cases, covered, varnt_cases))
                if not covered >= varnt_cases:
                    return Error(f"does not cover "
                        f"variants \n    {cases_to_str(varnt_cases - covered)}, \n"\
                        f"does cover \n    {cases_to_str(covered)}\n"
                    )
                else:
                    return Okay(f"enum with all cases coverd: \n {varnt_cases}")
        elif isinstance(to, bool):
            tru, fls = match._bool_cases
            if Case.is_a(bool) in self or Case.is_this(tru) in self and Case.is_this(fls) in self:
                return Okay('bool or True and False')
            else:
                return Error(f"does not cover {repr(to)}, must "\
                    f"match against either 'bool' or both 'True' and 'False'"
                )
        else:
            if Case.default in self:
                return Okay('objects with default')
            else:
                return Error(f"requires a default case, "\
                    "ex: [...: <some value/lambda/action>]"
                )

    def __contains__(self, thing:Case) -> bool:
        return thing in self.pairs.keys()

    def cases(self) -> Iterator[Case]:
        return iter(self.pairs.keys())

    # constructors
    def __class_getitem__(cls, slices:PatternSyntax) -> Result['Pattern', str]:
        if isinstance(slices, tuple):
            return cls.fromslices(slices)
        else:
            raise TypeError(f"must have more than one case, "\
                f"found {repr(slice)}"
            )

    @classmethod
    def fromslices(cls, slices:PatternSyntax) -> Union['Pattern']:
        global slice, Case, Action, types
        pairs = {}
        cases_for_next_action = []
        for thing in slices:
            if isinstance(thing, (list, set, types.GeneratorType)):
                # unpack unhashables
                for subthing in thing:
                    cases_for_next_action.append(thing)
            elif not isinstance(thing, slice):
                cases_for_next_action.append(thing)
            else:
                # make sure is okay
                if thing.step is None:
                    case_hint, action_hint = thing.start, thing.stop
                else:
                    raise TypeError(f"three parameter cases not supported, "\
                        f"found `{thing.start}:{thing.stop}:{thing.step}`, "\
                        "(three parameter cases reserved for future use)"
                    )

                # unpack unhashable
                if isinstance(case_hint, (list, set)):
                    for sub_hint in case_hint:
                        cases_for_next_action.append(sub_hint)
                else:
                    cases_for_next_action.append(case_hint)
                # then process them as a group
                #for case_hint in cases_for_next_action:
                while len(cases_for_next_action):
                    case_hint = cases_for_next_action.pop(0)
                    if case_hint in pairs:
                        pass # the first pattern that matches should trigger the action
                    elif not isinstance(case_hint, Case):
                        pairs[Case.infer(case_hint)] = Action.infer(action_hint)
                    else:
                        pairs[case_hint] = Action.infer(action_hint)
        else:
            return cls(pairs)

class match(DataVariable, Generic[M, R]):
    to: M

    def __getitem__(self, slices:PatternSyntax) -> R:
        global Pattern
        return self.against(Pattern.fromslices(slices))

    def against(self, pattern:Pattern) -> R:
        to = self.to
        pat_res = pattern.covers(to)
        if not pat_res.isokay():
            raise CoverageError(f"\nmatch(<some {type(to).__name__}>)[...] \n"\
                +pat_res.report
            )
        else:
            # print(pat_res.value)
            to = self.to
            for case, action in pattern:
                if case.matches(to): # then perform action
                    return action.take(to)
            else:
                print(f"{type(to)=}, {pattern}")
                print(f"{to=}")
                SHIT # _check_coverage should have made sure it would always match


def test(print):
    # check case inference

    print("check multi-mathces sets, iterables, lists, etc...")
    p = Pattern[
        range(5) : 'a',
        [ 5,  6,  7,  8,  9] : 'b',
         10, 11, 12, 13, 14  : 'c',
        {15, 16, 17, 18, 19} : 'd',
        (i for i in range(20, 25)) : 'e', # generator
        ... : 'default',
    ]

    assert 'a' == match( 2).against(p), f"got {match( 2).against(p)}"
    assert 'b' == match( 7).against(p), f"got {match( 7).against(p)}"
    assert 'c' == match(12).against(p), f"got {match(12).against(p)}"
    assert 'd' == match(17).against(p), f"got {match(17).against(p)}"
    assert 'e' == match(22).against(p), f"got {match(22).against(p)}"
    assert 'default' == match(255).against(p), f"got {match(255).against(p)}"

    @enum
    class color:
        class red: pass
        class green: pass
        class blue: pass
        class custom:
                r: int
                g: int
                b: int


    print("checking that case inferecnce works properly...")
    assert Case.enum(color.red)    == Case.infer(color.red)
    assert Case.enum(color.custom) == Case.infer(color.custom)

    assert Case.equals(5) == Case.infer(5),              "manual intervention required, fix inference"
    assert Case.is_this(True) == Case.infer(True),       "manual intervention required, fix inference"
    assert Case.is_this(False) == Case.infer(False),     "manual intervention required, fix inference"
    assert Case.is_a(bool) == Case.infer(bool),          "manual intervention required, fix inference"
    assert Case.is_in(range(5)) == Case.infer(range(5)), "manual intervention required, fix inference"
    assert Case.default == Case.infer(...),              "manual intervention required, fix inference"
    # case.subclasses(int) has no inference
    assert Case.equals(5) == Case.infer(5),              "manual intervention required, fix inference"

    print("checking case_to_str conversions...")
    assert '...' == case_to_str(Case.default),                                  "manual intervention required"
    assert '...' == case_to_str(Case.infer(...)),                               "manual intervention required"
    assert str(int) == case_to_str(Case.is_a(int)),                             "manual intervention required"
    assert '5' == case_to_str(Case.equals(5)),                                  "manual intervention required"
    assert str(range(5)) == case_to_str(Case.is_in(range(5))),                  "manual intervention required"
    assert 'all(...)' == case_to_str(Case.check(all)),                      f"manual intervention required, got {case_to_str(Case.check(print))}"
    assert f'Case.subclasses(cls={int})' == case_to_str(Case.subclasses(int)),  "manual intervention required"
    assert repr(Nothing) == case_to_str(Case.enum(Option.Nothing)),             "manual intervention required"
    assert repr(Some) == case_to_str(Case.enum(Some)),                          "manual intervention required"

    @enum
    class vars:
        class foo: pass
        class bar:
            x: int
        class baz:
            x: int
            y: int

    print('checking for incomplete match...')
    try:
        m = match(color.red)[
            color.red : 1,
            color.green : 2,
        ]
    except CoverageError as err:
        print("passed: should cover `color.red` and `color.green` but not `color.blue` or `color.custom` is it?:")
        print('    ', repr(err))

    p = Pattern[
        vars.foo: Action.passthrough,
        vars.bar: lambda x: x,
        vars.baz: lambda x, y: (x, y)
    ]

    print("checking the all variants are checked properly...")
    assert match(vars.foo).against(p)       is vars.foo, "match(vars.foo) did not match vars.foo"
    assert match(vars.bar(7)).against(p)    == 7,        "match(vars.foo) did not match vars.foo"
    assert match(vars.baz(8, 9)).against(p) == (8, 9),   "match(vars.foo) did not match vars.foo"

    print("checking number match range...")
    assert match(10)[
        range(5)  : False,
        range(10) : False,
        range(15) : True,
        ... : False,
    ], "number did not match range in match"
