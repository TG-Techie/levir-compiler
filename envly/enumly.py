#from dataclasses import dataclass # stop gap
import typing
from typing import *

from ._data_variable import DataVariable

__all__ = ('enum', 'isvariant', 'Enum',
    'EnumVariant',
    'EnumSingleVariant', 'EnumDataVariant',
    'EnumClass', 'EnumVariantClass',
)

def isvariant(inst, varnts):
    if not isinstance(varnts, tuple):
        varnts = (varnts,)
    for varnt in varnts:
        if isinstance(varnt, EnumSingleVariant):
            if inst is varnt:
                return True
            else:
                continue
        elif isinstance(inst, varnt):
            return True
    else:
        return False

class Enum():
    def __new__(cls, *_, **__):
        raise TypeError(f"must specify enum variant to init {cls}, like "\
            f"{cls.__name__}.SomeVariant(blah, blah)"
        )

class EnumVariant():

    __new__ = object.__new__

class EnumSingleVariant(EnumVariant):
    # thses are all alwasy singltons, the singleton instance of them are
    #   stored in the ._inst_ class variable, use hasattr to check for it

    def __new__(cls) -> Union['EnumSingleVariant']:
        global EnumSingleVariant
        if cls is EnumSingleVariant:
            raise TypeError(f"'{cls.__name__}' must be subclassed to be inited")
        # if is first time being initied
        if not hasattr(cls, '_inst_'):
            cls._inst_ = inst = super(EnumSingleVariant, cls).__new__(cls)
            return inst

        return cls._inst_

    @classmethod
    def __repr__(cls:type) -> str:
        return cls.__name__

class EnumDataVariant(DataVariable, EnumVariant):

    pass

class EnumClass(type):
    """
    these shoudl always auto inherit from
    ## attrs:
    - ._variants: a sequence of the variants iside of it
    """

    def __repr__(self) -> str:
        # FIXME: decide:
        return f"<class '{self.__name__}'>"

        return f"<enum <class '{self.__name__}'>>"
        return f"<enum-class '{self.__name__}'>"
        return f"<EnumClass '{self.__name__}'>"
        return f"<class enum '{self.__name__}'>"
        return etc, ...

    @property
    def __name__(self):
        return super().__name__

class EnumVariantClass(EnumClass):
    """
    these should alwasy auto inharit from EnumVariant and thier respective
    enum_cls (in that order)
    ## attrs:
    - ._enum_cls_: the surrounding enum
    """
    #__new__ = type.__new__
    # add init to make enum_class required and non searching
    def __repr__(self) -> str:
        # FIXME: also decide here base on EnumClass's style
        return f"<class '{self.__name__}'>"

    def _cls_title_(self) -> str:
        return f"{self._enum_cls_.__name__}.{self.__name__}"

    @property
    def __name__(self):
        if hasattr(self, '_enum_cls_'):
            return f"{self._enum_cls_.__name__}.{super().__name__}"
        else:
            return super().__name__


def enum(cls: type) -> EnumClass:
    enum_cls = enumcls_from_cls(cls)
    for obj in enum_cls.__dict__.values():
        if isinstance(obj, type) and not isinstance(obj, EnumClass):
            cls = obj
            cls = varnt_from_cls(cls, enum_cls)
            cls = link_varnt_into_enumcls(cls, enum_cls)
    return enum_cls

def enumcls_from_cls(src_cls):
    global Enum

    # check for mulitple inheritence, only genreic allowed
    if len(src_cls.__bases__) > 1:
        raise TypeError(f"Enums may only inherit from one Generic class, "\
            f"found multiple {bases}"
        )
    # that it's super class is object or is a genreic
    base, = src_cls.__bases__
    if base is not object and not issubclass(base, typing.Generic):
        raise TypeError(f"Enums cannot inherit from non-Generic Base classes, "\
            f"found {src_cls} inherits from {base}"
        )

    enum_cls = EnumClass(src_cls.__name__, (Enum, base), {**src_cls.__dict__})
    enum_variants = {} # the ._enum_varnts_ dict
    setattr(enum_cls, '_enum_varnts_', enum_variants)
    return enum_cls

def varnt_from_cls(cls: type, enum_cls: EnumClass) -> Union[EnumVariantClass, EnumSingleVariant]:
    assert cls.__bases__ == (object,), f"enum variants can only inherit from "\
        f"object, found {cls.__bases__}"

    name = cls.__name__

    # make a new class (an EnumVariantClass) based on the data from obj
    if not hasattr(cls, '__annotations__'):
        # make new type
        var_cls = EnumVariantClass(
            name, (EnumSingleVariant, enum_cls), {**cls.__dict__}
        )
        #var_obj = var_cls()

    else: # is a DataVariant
        var_cls = EnumVariantClass(
            name, (EnumDataVariant, enum_cls),{**cls.__dict__}
        )
        # since this is a data_var_cls it needs to act like a dataclass
        # var_cls = dataclass(unsafe_hash=True, repr=False, eq=False)(var_cls)


    # if is a single-variant return
    if issubclass(var_cls, EnumSingleVariant):
        var_obj = var_cls()
    else:
        var_obj = var_cls

    return var_obj

def _check_cls_overrides(cls, names):
    # check that __init__ and __new__ are not overidden
    keys = tuple(cls.__dict__.keys())
    for unallowed in names:
        assert unallowed not in keys, f"cannot override "\
            f"'{unallowed}' in enum variants, tried to override in "\
            f"enum variant {cls}"#" in enum '{enum_name}'"

def link_varnt_into_enumcls(var_obj, enum_cls):
    if isinstance(var_obj, EnumSingleVariant):
        var_cls = type(var_obj)
    else:
        var_cls = var_obj

    name = var_cls.__name__

    setattr(var_cls, '_enum_cls_', enum_cls)
    setattr(enum_cls, name, var_obj)
    enum_cls._enum_varnts_[name] = var_obj

def test(print):

    print(f"{EnumClass=}")
    print(f"{EnumVariantClass=}")

    print()

    print('checking raw Enum cannot be intied...')
    try:
        Enum()
    except TypeError as err:
        print(f"passed?: {repr(err)}")

    print('checking raw EnumSingleVariant cannot be intied...')
    try:
        EnumSingleVariant()
    except TypeError as err:
        print(f"passed?: {repr(err)}")

    print('check for enum improper inheritance...')
    try:
        @enum
        class ShouldNotWork(dict):
            class Variant: pass
    except TypeError as err:
        print(f"passed?: {repr(err)}")

    print('check for enum variant improper inheritance...')
    try:
        @enum
        class SomeEnum(dict):
            class improperVariant(dict):
                pass
    except TypeError as err:
        print(f"passed?: {repr(err)}")


    print()



    # test non generic
    @enum
    class OptionInt:

        class Nothing: pass
        class Some:thing: int

    print('checking instance inheritance...')
    cases = {
        OptionInt.Nothing: OptionInt,
        OptionInt.Nothing: type(OptionInt.Nothing),
        OptionInt.Nothing: EnumSingleVariant,
        OptionInt.Some(5): OptionInt,
        OptionInt.Some(5): OptionInt.Some,
        OptionInt.Some(5): EnumDataVariant,
    }
    for inst, cls in cases.items():
        assert isinstance(inst, cls), \
            f"{inst} should an isinstance of {cls}"

    print('checking Double init of EnumSingleVariant...')
    assert type(OptionInt.Nothing)() is OptionInt.Nothing, \
        f"RedType() shoulf have been the same object as Red, got "\
        f"{type(OptionInt.Nothing)()=}, {OptionInt.Nothing=}, "\
        f"{OptionInt.Nothing is type(OptionInt.Nothing)()=}"


    print()
    # test alot

    @enum
    class Color:
        class Red:   code = (255,   0,   0)
        class Green: code = (  0, 255,   0)
        class Blue:  code = (  0,   0, 255)
        class Custom:
            r: int
            g: int
            b: int

            @property
            def code(self):
                return self.r, self.g, self.b

    print(f"{Color.Red=}")
    print(f"{Color.Custom(128, 64, 17)=}")

    print(f"{Color.Custom}")
    print(f"{type(Color.Red)=}")

    a = Color.Custom(128, 64, 17)
    b = Color.Custom(  7,  7,  7)
    c = Color.Custom(128, 64, 17)

    print(f"{a=}")
    print(f"{b=}")
    print(f"{c=}")

    print('checking DataVariant equivalence')
    assert a == a, "hands on debugging required, see the __eq__ method"
    assert a != b, "hands on debugging required, see the __eq__ method"
    assert a == c, "hands on debugging required, see the __eq__ method"

    assert b != a, "hands on debugging required, see the __eq__ method"
    assert b == b, "hands on debugging required, see the __eq__ method"
    assert b != c, "hands on debugging required, see the __eq__ method"

    assert c == a, "hands on debugging required, see the __eq__ method"
    assert c != b, "hands on debugging required, see the __eq__ method"
    assert c == c, "hands on debugging required, see the __eq__ method"

    print()

    # check identifying Enum
    print('check identifying Enum')

    # breakout fro ease
    Red = Color.Red
    Custom = Color.Custom
    RedType = type(Red)

    print(f"{Red=}")
    print(f"{Custom=}")
    print(f"{RedType=}")

    print()

    print('cheking inheritance...')
    cases = {
        Color: Enum,

        RedType: Enum,
        RedType: EnumVariant,
        RedType: EnumSingleVariant,
        RedType: Color,

        Custom: Enum,
        Custom: EnumVariant,
        Custom: EnumDataVariant,
        Custom: Color,
    }
    for cls, supercls in cases.items():
        assert issubclass(cls, supercls), \
            f"{cls} should inherit from {supercls}"

    print('checking class composure...')
    cases = {
        Color: type,
        Color: EnumClass,

        RedType: type,
        RedType: EnumClass,
        RedType: EnumVariantClass,

        Custom: type,
        Custom: EnumClass,
        Custom: EnumVariantClass,
    }
    for inst, cls in cases.items():
        assert isinstance(inst, cls), \
            f"{inst} should an isinstance of {cls}"

    print('checking instance inheritance...')
    cases = {
        Red: Color,
        Red: RedType,

        Custom(255, 255, 255): Color,
        Custom(255, 255, 255): Custom,
    }
    for inst, cls in cases.items():
        assert isinstance(inst, cls), \
            f"{inst} should an isinstance of {cls}"

    print('checking Double init of EnumSingleVariant...')
    assert RedType() is Red, \
        f"RedType() shoulf have been the same object as Red, got "\
        f"{RedType()=}, {Red=}, {RedType() is Red=}"


    print("checking generic:")

    print("checking that a generic enum can be made...")
    T = TypeVar('T')
    @enum
    class OptionAny(Generic[T]):
        class Nothing: pass
        class Some:thng: T
