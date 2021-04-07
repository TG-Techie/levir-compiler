from strictly import *
from envly import *

from .tools import *

from levir1 import front
from levir1.front import Subject
from strictly import *


@strictly
def translate(subj: Subject) -> str:
    return match(subj)[
        Subject.var : lambda *_: translate_var(subj),
        Subject.mbrof : lambda *_: translate_mbrof(subj),
    ]


def translate_var(var: Subject.var) -> str:
    return var_(var.name, var.type)


def translate_mbrof(mbrof: Subject.var) -> str:
    string = var_(mbrof.varname, mbrof.vartype)
    outertype = mbrof.vartype
    for mbrname, cur_mbrtype in mbrof.mbrs.items():
        string = (
            f"{cntnptr_(outertype.type)}(&({string}))->{mbr_(mbrname, cur_mbrtype)}"
        )
        outertype = cur_mbrtype
    return string
