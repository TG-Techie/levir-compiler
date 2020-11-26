from strictly import *
from envly import *
from typing import *
from envly._data_variable import DataVariable, _DerivedField, _FactoryField

from levir.interfaces import Member

from levir.lexer_parser import (
    Location, Tree, Token,
    parse_str, namefrom,
    unsupported_grammar
)


class BuiltinType(DataVariable):
    name : str

    @property
    def mbrs(self) -> Dict[str, Union[Member, object]]:
        return {}

class BuiltinFunc(DataVariable):
    name : str
    # TODO: this

class BuiltinModule(DataVariable):
    items: Dict[str, Union[BuiltinType, BuiltinFunc, 'BuiltinMethod']] = _FactoryField(dict)

    def find(self, name:str) -> Option[Union[BuiltinType, BuiltinFunc]]:
        return Option(self.items.get(name, None))

    def has(self, name:str) -> bool:
        return name in self.items

    def additem(self, item:Union[BuiltinType, BuiltinFunc]) -> Result[None, str]:
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
    BuiltinStruct('bool'),

    BuiltinStruct('int8'),
    BuiltinStruct('int16'),
    BuiltinStruct('int32'),
    BuiltinStruct('int64'),

    BuiltinStruct('uint8'),
    BuiltinStruct('uint16'),
    BuiltinStruct('uint32'),
    BuiltinStruct('uint64'),

    BuiltinStruct('usize'),

    BuiltinStruct('float32'),
    BuiltinStruct('float64'),

    BuiltinStruct('char'),
    BuiltinStruct('Void'),

    BuiltinFunc('add'),
    BuiltinFunc('sub'),
    BuiltinFunc('mul'),
    BuiltinFunc('div'),
    BuiltinFunc('pow'),
)

for item in builtin_items:
    ~module.additem(item)
else:
    pass
