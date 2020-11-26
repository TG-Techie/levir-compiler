from envly import *
from levir import front
from . import tools, fromstmt
from . import fromfunc, fromclass, fromstruct#, frommthd


def intofile(mod:front.Module, output):
    itemlist = [*mod.items.values()]
    itemlist.sort(key=lambda item:match(item)[
        front.Class  : lambda: 1,
        front.Struct : lambda: 2,
        front.Func   : lambda: 3, 
        front.Mthd   : lambda: 4,
        ... : MatchError(f"unknown item '{type(item).__name__}'")
    ])
    # output prototypes
    for item in itemlist:
        output.write(toprototype(mod, item))
    # output bodies
    for item in itemlist:
        output.write(tobody(mod, item))


def toprototype(mod:front.Module, item:front.Item) -> str:
    return match(item)[
        front.Func   : lambda: fromfunc.toprototype(mod, item),
        front.Class  : lambda: fromclass.toprototype(mod, item),
        front.Struct : lambda: fromstruct.toprototype(mod, item),
        ... : MatchError(
            f"{item.loc}: unrecognized item, '{type(item).__name__}'"
        )
    ]

def tobody(mod:front.Module, item:front.Item) -> str:
    return match(item)[
        front.Func   : lambda: fromfunc.tobody(mod, item),
        front.Class  : lambda: fromclass.tobody(mod, item),
        front.Struct : lambda: fromstruct.tobody(mod, item),
        ... : MatchError(
            f"{item.loc}: unrecognized item, '{type(item).__name__}'"
        )
    ]
