from strictly import *
from envly import *
from typing import *
from envly._data_variable import DataVariable, _DerivedField, _FactoryField

from levir.interfaces import Member

from levir.lexer_parser import Location, Tree, Token, parse_str, namefrom, unsupported


class BuiltinType(DataVariable):
    name: str

    @property
    def mbrs(self) -> Dict[str, Union[Member, object]]:
        return {}


class BuiltinFunc(DataVariable):
    name: str
    # TODO: this


class BuiltinModule(DataVariable):
    items: Dict[str, Union[BuiltinType, BuiltinFunc, "BuiltinMethod"]] = _FactoryField(
        dict
    )

    def find(self, name: str) -> Option[Union[BuiltinType, BuiltinFunc]]:
        return Option(self.items.get(name, None))

    def has(self, name: str) -> bool:
        return name in self.items

    def additem(self, item: Union[BuiltinType, BuiltinFunc]) -> Result[None, str]:
        if item.name in self.items:
            return error(f"'{item.name}' already in {self}")
        else:
            self.items[item.name] = item
            return Okay(None)


class BuiltinClass(BuiltinType):
    def isclass(self):
        return True

    def isstruct(self):
        return False


class BuiltinStruct(BuiltinType):
    def isclass(self):
        return False

    def isstruct(self):
        return True


module = BuiltinModule()

builtin_items = (
    BuiltinStruct("usize"),
    BuiltinStruct("RefCount"),
    BuiltinStruct("bool"),
    BuiltinStruct("i8"),
    BuiltinStruct("i16"),
    BuiltinStruct("i32"),
    BuiltinStruct("i64"),
    BuiltinStruct("u8"),
    BuiltinStruct("u16"),
    BuiltinStruct("u23"),
    BuiltinStruct("u64"),
    BuiltinStruct("f32"),
    BuiltinStruct("f128"),
    # BuiltinStruct('char'),
    BuiltinStruct("Nothing"),
    # BuiltinFunc('add'),
    # BuiltinFunc('sub'),
    # BuiltinFunc('mul'),
    # BuiltinFunc('div'),
    # BuiltinFunc('pow'),
)

for item in builtin_items:
    ~module.additem(item)
else:
    pass
