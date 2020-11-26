from envly import *
from strictly import *

from typing import *
from typing import Protocol

from envly._data_variable import DataVariable, _DefaultField, _DerivedField, _FactoryField

from . import front
from . import interfaces



TBD = Any

class Item(DataVariable):
    pass

# StructRefs need to be integraed into this file? once methods are applied

class Module(DataVariable):
    front: front.Module
    _items: Dict[str, 'UserType'] = _FactoryField(dict)


    def isresolved(self):
        return self._resolved

    @strictly
    def resolve(self) -> Result[None, str]:
        for name, item in self._items.items():
            ~item.resolve(self)
        else:
            self._resolved = True
            return Okay(None)

    @strictly
    def find(self, name:str) -> Option[Item]:
        #return Option(self.items.get(name, None))
        if name in self._items:
            return Some(self._items[name])
        # add an elif for other modules
        else:
            return self._bltn_mod.find(name)

    @strictly
    def has(self, name:str) -> bool:
        return name in self._items

    def iteritems(self) -> Iterable[Union['UserType', 'Func']]:
        return self._items.values()

    @classmethod
    def fromfront(cls:type, fmod:front.Module) -> Result['Module', None]:
        self = cls(fmod)
        # construct
        for item in fmod.iteritems():
            self._items[item.name] = ~match(item)[
                front.Class  : lambda: Class.fromfront(item),
                front.Struct : lambda: Struct.fromfront(item),
                front.Func   : lambda: Func.fromfront(item),
                ...          : lambda: raise_(NotImplementedError(
                    f"middle does not support '{type(item).__name__}'"
                ))
            ]

        return Okay(self)

class UserType(Item):
    front: front.UserType
    name: str
    mbrs: Dict[str, TypeIdent]

    @classmethod
    def fromfront(cls:type, ftype:front.UserType) -> Option['UserType']:
        return Okay(cls(
            front = ftype,
            name = ftype.name,
            mbrs = {name: TypeIdent.name(mbr.typename) \
                for name, mbr in ftype.mbrs.items()
            }
        ))

    def resolve(self, mod:Module) -> Result[None, str]:
        mbrs = {} # maintain order
        for name, ident in self.mbrs.items():
            if isvariant(ident, TypeIdent.name): # find teh type
                mbrs[name] = mod.find(ident.name).unwrap(f"nothing found for '{name}'")
            else:
                mbrs[name] = ident
        self.mbrs = mbrs
        return Okay(None)

class Class(UserType):
    pass

class Struct(UserType):
    pass

class Func(Item):
    front   : front.Func
    name    : str
    rettype : TypeIdent
    args    : Dict[str, TypeIdent]
    locals  : Dict[str, TypeIdent]
    frame   : Option[TBD]

    @classmethod
    def fromfront(cls:type, ffunc:front.Func) -> 'Func':
        return Okay(cls(
            front = ffunc,
            name  = ffunc.name,
            rettype = TypeIdent.name(ffunc.rettype),
            args = {name : TypeIdent(mbr.typename)
                for name, mbr in ffunc.args.items()
            },
            locals = {name : TypeIdent(mbr.typename)
                for name, mbr in ffunc.locals.items()
            },
            frame = Nothing
        ))

    @strictly
    def resolve(self, mod:Module) -> Result[None, str]:
        self.args = {
                name : match(ident)[
                    TypeIdent.name : lambda: mod.find(ident.name),
                    TypeIdent.type : ...
                ]
             for name, ident in self.args.items()
        }
        self.locals = {
                name : match(ident)[
                    TypeIdent.name : lambda name: mod.find(name),
                    TypeIdent.type : ...
                ]
             for name, ident in self.locals.items()
        }
        return Okay(None)
