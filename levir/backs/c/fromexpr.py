from envly import *
from levir import front
from levir.front import Expr, BinOp
from .tools import *
from . import fromsubj

def translate(expr:Expr) -> str:
    return match(expr)[
        Expr.litrl    : lambda *_: translate_litrl(expr),
        Expr.new      : lambda *_: translate_new(expr),
        Expr.get      : lambda *_: translate_get(expr),
        Expr.binop    : lambda *_: translate_binop(expr),
        Expr.fncall   : lambda *_: translate_fncall(expr),
        Expr.mthdcall : lambda *_: translate_mthdcall(expr),
    ]

def translate_litrl(litrl:Expr) -> str:
    return f"litrl_{litrl.type.type.name}({litrl.src})"

def translate_new(new:Expr.new) -> str:
    global translate
    return (
        f"{new_(new.type)}( ({content_(new.type)}) " "{"
        f"{', '.join(translate(subexpr) for subexpr in new.cntn)}"
        "})"
    )

def translate_get(get:Expr.get) -> str:
    global translate
    return (
        f"{get_(get.type)}({fromsubj.translate(get.subj)})"
    )

def translate_binop(binop:Expr.binop) -> str:
    global translate
    return (
        f"{binop.op}_{binop.a.type.type.name}_{binop.b.type.type.name}"
            f"({translate(binop.a)}, {translate(binop.b)})"
    )
