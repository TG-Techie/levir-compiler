from strictly import *
from levir import front
from levir.front import Frame, Stmt
from .tools import *
from . import fromstmt


@strictly
def translate(frame: Frame) -> str:
    return "".join(fromstmt.translate(stmt) for stmt in frame.stmts).replace(
        "\n", "\n    "
    )
