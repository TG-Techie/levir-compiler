from typing import *
from typing import TextIO

from envly import *

from dataclasses import dataclass

from . import lexer_parser
from .lexer_parser import Tree, Token

from . import front
from .backs import c

def translate_file(source:'TextIO', output:'TextIO') -> None:
    #tree = lexer_parser.parse_str(source.read())

    fmod = ~front.Module.fromfile(source)
    #mmod = ~middle.Module.fromfront(fmod)
    ~fmod.resolve()
    ~fmod.check()
    c.intofile(fmod, output)
    return fmod
    #basic_checks(mod)
    #impl.translate_into(mod, output)
