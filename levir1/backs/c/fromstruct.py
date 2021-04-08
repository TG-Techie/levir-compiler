from envly import *
from strictly import *

from levir1 import front
from levir1.front import Module, Struct
from .tools import *


@strictly
def toprototype(mod: front.Module, sct: front.Struct):
    srcname = sct.name
    Self = Type_(sct)
    Content = f"{content_(sct)}"

    return (
        f"typedef struct {srcname} /*prototype*/ {Self};\n"
        f"typedef {Self} {content_(sct)};\n"
    ) + "".join(
        proto + " __attribute__ ((always_inline));\n"
        for proto in (
            f"{Self} {new_(sct)}({Content} content)",
            f"{Self} {dflt_(sct)}()",
            f"{Self} {get_(sct)}({Self} self)",
            f"void {drop_(sct)}({Self} self)",
            f"void {rtn_(sct)}({Self} self)",
            f"void {rel_(sct)}({Self} self)",
            f"{Content}* {cntnptr_(sct)}({Self}* selfptr)",
        )
    )


@strictly
def tobody(mod: Module, sct: Struct) -> str:
    srcname = sct.name
    Self = Type_(sct)
    Content = f"{content_(sct)}"

    content_body = ";\n    ".join(
        f"{Type_(mbrtype)} {mbr_(mbrname, mbrtype)}"
        for mbrname, mbrtype in sct.mbrs.items()
    )

    dfltblock = (
        "{\n        "
        + (
            "(),\n        ".join(
                f".{mbr_(mbrname, mbrtype)} = {dflt_(mbrtype)}"
                for mbrname, mbrtype in sct.mbrs.items()
            )
        )
        + "(),\n    }"
    )

    getblock = (
        "{\n        "
        + (
            ",\n        ".join(
                f".{mbr_(mbrname, mbrtype)} = {get_(mbrtype)}(self.{mbr_(mbrname, mbrtype)})"
                for mbrname, mbrtype in sct.mbrs.items()
            )
        )
        + ",\n    }"
    )

    dropblock = ";\n    ".join(
        f"{drop_(mbrtype)}(self.{mbr_(mbrname, mbrtype)})"
        for mbrname, mbrtype in sct.mbrs.items()
    )

    return (
        (
            f"typedef struct {sct.name}"
            "{\n"
            f"    {content_body};\n"
            "}" + f" {content_(sct)};\n"
        )
        + (  #  new
            f"{Self} {new_(sct)}({Content} content)"
            "{\n"
            "    return content; /* a struct and its content is the same thing*/\n"
            "}\n"
        )
        + (  # default value before assignment
            f"{Self} {dflt_(sct)}()" "{\n" f"    return ({Self}) {dfltblock};\n" "}\n"
        )
        + (  # get (ie copy)
            f"{Self} {get_(sct)}({Self} self)"
            "{\n"
            f"    return ({Self}){getblock};\n"
            "}\n"
        )
        + (  # drop (erase local)
            f"void {drop_(sct)}({Self} self)"
            "{\n"
            f"    {dropblock};\n"
            "    return;\n"
            "}\n"
        )
        + (  # retain (does nothing)
            f"void {rtn_(sct)}({Self} self)" "{\n" "    return;\n" "}\n"
        )
        + (  # release (does nothing)
            f"void {rel_(sct)}({Self} self)" "{\n" "    return;\n" "}\n"
        )
        + (
            f"{Content}* {cntnptr_(sct)}({Self}* selfptr)"
            "{\n"
            f"    return ({Content}*) selfptr;\n"
            "}\n"
        )
    )
