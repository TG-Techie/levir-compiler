from envly import *
from strictly import *
from levir import front
from levir.front import Stmt, Subject
from .tools import *
from . import fromsubj, fromexpr

def translate(stmt:front.Stmt) -> str:
    return match(stmt)[
        Stmt.ret : lambda *_: translate_ret(stmt),
        Stmt.asn : lambda *_: translate_asn(stmt),
        Stmt.asn : lambda *_: translate_asn(stmt),
        ... : MatchError(
            f"unknown statement '{type(stmt).__name__}'"
        )
    ]

@strictly
def translate_ret(ret:front.Stmt.ret) -> str:
    return (
        "/* return statement */\n"
        f"{Type_(ret.rettype)} _return_tmp_ = {fromexpr.translate(ret.expr)};\n"
        f"goto _return_label_;"
    )

@strictly
def translate_asn(asn:front.Stmt.asn) -> str:
    return (
    "{ /* assignment */\n"
        f"    {Type_(asn.asntype)}* target_ptr = &({fromsubj.translate(asn.subj)});\n"
        f"    {Type_(asn.asntype)} prev_value = *target_ptr;\n"
        f"    *target_ptr = {fromexpr.translate(asn.expr)};\n"
        f"    {drop_(asn.asntype)}(prev_value);\n"
    "}\n")

def rel(type) -> str: # takes type compliant options
    return f"{rel_(type)}"
