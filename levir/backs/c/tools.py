from strictly import *
from levir import front

@strictly
def Type_(type:front.UserType, isref=False) -> str:
    if not isref:
        return f"type_{type}"
    else:
        return f"ref_{type}"
