#from envly import *
from levir import front
from .tools import *
from . import fromstmt

def toprototype(mod:front.Module, fn:front.Func) -> str:
    return f"type_{fn.rettype.type.name} fn_{fn.name} {argsfrom(fn)};\n"

def tobody(mod:front.Module, fn:front.Func) -> str:
    stmtbody = ''.join(fromstmt.translate(stmt) for stmt in fn.frame.stmts)
    stmtbody = stmtbody.replace('\n', '\n    ')
    declarations = '\n    '.join(
        f"{typename(lcltype)} var_{lclname} = dflt_{lcltype.type.name}();"
            for lclname, lcltype in fn.locals.items()
    )
    return_procedure = '\n    '.join(
            f"drop_{lcltype.type.name}(var_{lclname});"
                for lclname, lcltype in fn.locals.items()
        ) + '\n    '.join(
            f"drop_{argtype.type.name}(var_{argname});"
                for argname, argtype in fn.args.items()
        )

    return (
        f"type_{fn.rettype.type.name} fn_{fn.name}{argsfrom(fn)}{{ \n"\
        f"    {declarations}\n"
        f"    {stmtbody}\n"
         "_return_label_:\n"
        f"    {return_procedure}\n"
        f"    return _return_tmp_;\n"
        "}\n"
    )

def argsfrom(fn:front.Func):
    #[print(typename(argtype)) for argtype in fn.args.values()]
    params = [f"{typename(argtype)} var_{name}" for name, argtype in fn.args.items()]
    return f"({', '.join(params)})"
