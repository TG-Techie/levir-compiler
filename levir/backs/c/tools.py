from strictly import *
from levir import front

@strictly
def typename(type) -> str:
    if not type.isref():
        return f"type_{type}"
    else:
        return f"ref_{type}"

@strictly
def Type_(type:front.UserType, isref=False) -> str:
    if not isref:
        return f"type_{type}"
    else:
        return f"ref_{type}"
