from strictly import *
from levir1 import front
from levir1.front import Frame, Stmt
from .tools import *
from . import fromstmt


@strictly
def translate(frame: Frame) -> str:
    return "".join(fromstmt.translate(stmt) for stmt in frame.stmts).replace(
        "\n", "\n    "
    )
