
from levir import front

def typename(type:front.UserType) -> str:
    if not type.isref():
        return f"type_{type}"
    else:
        return f"ref_{type}"
