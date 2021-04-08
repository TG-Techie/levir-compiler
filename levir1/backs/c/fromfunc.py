from strictly import *

from levir1 import front
from .tools import *

# from . import fromstmt
from . import fromframe


@strictly
def toprototype(mod: front.Module, fn: front.Func) -> str:
    return f"{Type_(fn.rettype)} fn_{fn.name} {argsfrom(fn)};\n"


@strictly
def tobody(mod: front.Module, fn: front.Func) -> str:
    # stmtbody = ''.join(fromstmt.translate(stmt) for stmt in fn.frame.stmts)
    # stmtbody = stmtbody.replace('\n', '\n    ')

    declarations = "\n    ".join(
        f"{Type_(lcltype)} {var_(lclname, lcltype)} = {dflt_(lcltype)}();"
        for lclname, lcltype in fn.locals.items()
    )
    return_procedure = "\n    ".join(
        f"{drop_(lcltype)}({var_(lclname, lcltype)});"
        for lclname, lcltype in fn.locals.items()
    ) + "\n    ".join(
        f"{drop_(argtype)}({var_(argname, argtype)});"
        for argname, argtype in fn.args.items()
    )

    return (
        f"{Type_(fn.rettype)} fn_{fn.name}{argsfrom(fn)}{{ \n"
        f"    {declarations}\n"
        f"    {fromframe.translate(fn.frame)}\n"
        "_return_label_:\n"
        f"    {return_procedure}\n"
        f"    return _return_tmp_;\n"
        "}\n"
    )


@strictly
def argsfrom(fn: front.Func):
    # [print(Type_(argtype)) for argtype in fn.args.values()]
    params = [
        f"{Type_(argtype)} {var_(name, argtype)}" for name, argtype in fn.args.items()
    ]
    return f"({', '.join(params)})"
