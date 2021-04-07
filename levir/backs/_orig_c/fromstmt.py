from envly import *
from strictly import *
from levir import front
from levir.front import Stmt, Subject, Clause
from .tools import *
from . import fromsubj, fromexpr, fromframe


def translate(stmt: front.Stmt) -> str:
    return match(stmt)[
        Stmt.ret : lambda *_: translate_ret(stmt),
        Stmt.asn : lambda *_: translate_asn(stmt),
        Stmt.dropin : lambda *_: translate_dropin(stmt),
        Stmt.cond : lambda *_: translate_cond(stmt),
        ... : MatchError(f"unknown statement '{type(stmt).__name__}'"),
    ]


@strictly
def translate_ret(ret: front.Stmt.ret) -> str:
    return (
        "/* return statement */\n"
        f"{Type_(ret.rettype)} _return_tmp_ = {fromexpr.translate(ret.expr)};\n"
        f"goto _return_label_;"
    )


@strictly
def translate_asn(asn: Stmt.asn) -> str:
    return (
        f"{{ /* assignment {asn.loc} */\n"
        f"    {Type_(asn.asntype)}* target_ptr = &({fromsubj.translate(asn.subj)});\n"
        f"    {Type_(asn.asntype)} prev_value = *target_ptr;\n"
        f"    *target_ptr = {fromexpr.translate(asn.expr)};\n"
        f"    {drop_(asn.asntype)}(prev_value);\n"
        "}\n"
    )


@strictly
def translate_dropin(dropin: Stmt.dropin) -> str:
    if dropin.lang != "c":
        print(
            f"Skipping {dropin.loc}: skipping dopping in {repr(dropin.lang)}, "
            f"this backend only supports 'c' dropins"
        )
        return "c"
    else:
        return dropin.src


@strictly
def translate_cond(cond: Stmt.cond) -> str:
    return "".join(translate_clause(clause) for clause in cond.clauses)


@strictly
def translate_clause(clause: Clause) -> str:
    kind = match(clause)[
        Clause.if_ : lambda *_: "if",
        Clause.elif_ : lambda *_: "else if",
        Clause.else_ : lambda *_: "else",
    ]

    # make condition
    csrc_cond = match(clause)[
        Clause.if_,
        Clause.elif_ : lambda _, cond, __: (f"(({fromexpr.translate(cond)}).native)"),
        Clause.else_ : lambda *_: "",
    ]

    return (
        f"{kind} {csrc_cond} " "{\n" f"    {fromframe.translate(clause.frame)};\n" "}\n"
    )
