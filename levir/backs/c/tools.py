from envly import *
from strictly import *
from typing import *
from levir import front

_TypeSpec = Union[
    front.UserType,
    front.levir_builtins.BuiltinType,
    front.TypeIdent.found
]

_isref = lambda spec: isinstance(spec, front.TypeIdent) and spec.isref()
_ref = lambda spec: 'ref' if _isref(spec) else ''

@strictly
def _find_name(spec:_TypeSpec) -> str:
    if isinstance(spec, (front.UserType, front.levir_builtins.BuiltinType)):
        return spec.name
    elif isinstance(spec, front.TypeIdent):
        return spec.type.name

@strictly
def Type_(spec:_TypeSpec) -> str:
    if _isref(spec):
        return f"ref_{_find_name(spec)}"
    else:
        return f"type_{_find_name(spec)}"


# this allows for the posibility of having catables locals/members later
#   however this may not be compatible with inference
for prefix in ('mbr', 'var'):
    exec(f'''if True:
        @strictly
        def {prefix}_(name:str, type:_TypeSpec) -> str:
            return "{prefix}"+"_"+name
    ''')


for prefix in ('get', 'drop', 'dflt', 'rel', 'rtn', 'cntnptr'):
    exec(f'''if True:
        @strictly
        def {prefix}_(spec:_TypeSpec) -> str:
            return "{prefix}"+_ref(spec)+"_"+_find_name(spec)
    ''')

@strictly
def new_(spec:_TypeSpec) -> str:
    if _isref(spec):
        FUCK
    return "new_"+_find_name(spec)

@strictly
def content_(spec:_TypeSpec) -> str:
    return "content_"+_find_name(spec)
