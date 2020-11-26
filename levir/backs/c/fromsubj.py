from strictly import *
from envly import *

from levir import front
from levir.front import Subject
from strictly import *

@strictly
def translate(subj:Subject) -> str:
    return match(subj)[
        Subject.var   : lambda *_: translate_var(subj),
        Subject.mbrof : lambda *_: translate_mbrof(subj)
    ]

def translate_var(var:Subject.var) -> str:
    return f"var_{var.name}"

def translate_mbrof(mbrof:Subject.var) -> str:
    string = f"var_{mbrof.varname}"
    outertype = mbrof.vartype
    for mbrname, next_outertype in mbrof.mbrs.items():
        string = f"cntnptr_{outertype.type.name}(&({string}))->mbr_{mbrname}"
        outertype = next_outertype
    return string
