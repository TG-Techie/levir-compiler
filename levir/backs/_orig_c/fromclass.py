from envly import *
from strictly import *

from levir import front
from levir.front import Module, Class
from .tools import *


@strictly
def toprototype(mod: front.Module, cls: front.Class):
    srcname = cls.name
    Self = Type_(cls)
    Content = f"{content_(cls)}"

    return (
        f"typedef struct {Content} /*prototype*/ {Content};\n"
        f"typedef struct {srcname} /*prototype*/ *{Self};\n"
    ) + "".join(
        proto + " __attribute__ ((always_inline));\n"
        for proto in (
            f"{Self} {new_(cls)}({Content} content)",
            f"{Self} {dflt_(cls)}()",
            f"{Self} {get_(cls)}({Self} self)",
            f"void {drop_(cls)}({Self} self)",
            f"void {rtn_(cls)}({Self} self)",
            f"void {rel_(cls)}({Self} self)",
            f"{Content}* {cntnptr_(cls)}({Self}* selfptr)",
        )
    )


def tobody(mod: Module, cls: Class) -> str:

    srcname = cls.name
    Self = Type_(cls)
    Content = f"{content_(cls)}"

    content_body = ";\n    ".join(
        f"{Type_(mbrtype)} {mbr_(mbrname, mbrtype)}"
        for mbrname, mbrtype in cls.mbrs.items()
    )

    relblock = ";\n        ".join(
        f"{rel_(mbrtype.type)}(self->content.{mbr_(mbrname, mbrtype)})"
        for mbrname, mbrtype in cls.mbrs.items()
    )

    return (
        (  # body define
            f"typedef struct {Content}"
            "{\n"
            f"    {content_body};\n"
            "} "
            f"{Content};\n"
            f"struct {srcname} "
            "{\n"
            "    RefCount rc;\n"
            f"    {Content} content;\n"
            "};\n"
        )
        + (  # new
            f"{Self} {new_(cls)}({Content} content)"
            "{\n"
            f"    {Self} self = ({Self})malloc(sizeof(struct {srcname}));\n"
            "    self->rc = 1;\n"
            "    self->content = content;\n"
            "    return self;\n"
            "}\n"
        )
        + (  # default value for unused locals
            f"{Self} {dflt_(cls)}()" "{\n    return NULL;\n}\n"
        )
        + (  # get a instance
            f"{Self} {get_(cls)}({Self} self)"
            "{\n"
            f"    {rtn_(cls)}(self);\n"
            "    return self;\n"
            "}\n"
        )
        + (
            f"void {drop_(cls)}({Self} self)"
            "{\n"
            f"    {rel_(cls)}(self);\n"
            "    return;\n"
            "}\n"
        )
        + (  # retain a class instance
            f"void {rtn_(cls)}({Self} self)"
            "{\n"
            # "    if (self == NULL) {\n"
            # "        printf(\"variable used before assignment\");\n"
            # "        exit(-1);\n"
            # "    }\n"
            "    self->rc +=1;\n"
            "    return;\n"
            "}\n"
        )
        + (  # release a class instance
            f"void {rel_(cls)}({Self} self)"
            "{\n"
            "    if (self == NULL){return;}\n"
            "    self->rc -= 1;\n"
            "    if (self->rc == 0){\n"
            f"        {relblock};\n"
            "        free(self);\n"
            "    }\n"
            "    return;\n"
            "}\n"
        )
        + (  # expose content
            f"{Content}* {cntnptr_(cls)}({Self}* selfptr)"
            "{\n"
            f"    {Self} self = *selfptr;\n"
            f"    return &(self->content);\n"
            "}\n"
        )
    )
