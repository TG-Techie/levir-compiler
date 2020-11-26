from envly import *
from strictly import *

from levir import front
from levir.front import Module, Struct
from .tools import *

@strictly
def toprototype(mod:front.Module, sct:front.Struct):
    srcname = sct.name
    Self = f"type_{srcname}"
    Content = f"content_{srcname}"

    return (
        f"typedef struct {srcname} /*prototype*/ {Self};\n"
        f"typedef {Self} content_{sct.name};\n"
    ) + ''.join( proto+' __attribute__ ((always_inline));\n' for proto in (
        f"{Self} new_{srcname}({Content} content)",
        f"{Self} dflt_{srcname}()",
        f"{Self} get_{srcname}({Self} self)",
        f"void drop_{srcname}({Self} self)",
        f"void rtn_{srcname}({Self} self)",
        f"void rel_{srcname}({Self} self)",
        f"{Content}* cntnptr_{srcname}({Self}* selfptr)",
    ))

@strictly
def tobody(mod:Module, sct:Struct) -> str:
    srcname = sct.name
    Self = f"type_{srcname}"
    Content = f"content_{srcname}"

    content_body = ';\n    '.join(
        f"{typename(mbrtype)} mbr_{mbrname}"
            for mbrname, mbrtype in sct.mbrs.items()
    )

    dfltblock = '{\n        ' + (
        '(),\n        '.join( f".mbr_{mbrname} = dflt_{mbrtype.type.name}"
            for mbrname, mbrtype in sct.mbrs.items()
        )
    ) + '(),\n    }'


    getblock = '{\n        ' + (
        ',\n        '.join( f".mbr_{mbrname} = get_{mbrtype.type.name}(self.mbr_{mbrname})"
            for mbrname, mbrtype in sct.mbrs.items()
        )
    ) + ',\n    }'

    dropblock = (
        ';\n    '.join( f"drop_{mbrtype.type.name}(self.mbr_{mbrname})"
            for mbrname, mbrtype in sct.mbrs.items()
        )
    )

    return (
        f"typedef struct {sct.name}""{\n"
        f"    {content_body};\n"
         "}" + f" content_{sct.name};\n"
    ) + ( #  new
        f"{Self} new_{srcname}({Content} content)""{\n"
         "    return content; /* a struct and its content is the same thing*/\n"
         "}\n"
    ) + ( # default value before assignment
        f"{Self} dflt_{srcname}()""{\n"
        f"    return ({Self}) {dfltblock};\n"
         "}\n"
    ) + ( # get (ie copy)
        f"{Self} get_{srcname}({Self} self)""{\n"
        f"    return ({Self}){getblock};\n"
         "}\n"
    ) + (# drop (erase local)
        f"void drop_{srcname}({Self} self)""{\n"
        f"    {dropblock};\n"
         "    return;\n"
         "}\n"
    ) + (# retain (does nothing)
        f"void rtn_{srcname}({Self} self)""{\n"
         "    return;\n"
         "}\n"
    ) + (# release (does nothing)
        f"void rel_{srcname}({Self} self)""{\n"
         "    return;\n"
         "}\n"
    ) + (

        f"{Content}* cntnptr_{srcname}({Self}* selfptr)""{\n"
        f"    return ({Content}*) selfptr;\n"
         "}\n"
    )
