import clang
import sys
import clang.cindex

from clang.cindex import Config
from clang.cindex import Cursor
from clang.cindex import CursorKind

import platform
from parser_set import *


def parse(cursor: Cursor):
    if cursor.kind == CursorKind.PARM_DECL:
        parse_parm_decl(cursor)
    elif cursor.kind == CursorKind.FUNCTION_DECL:
        parse_function_decl(cursor)


if platform.system() == 'Linux':
    Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")
else:
    Config.set_library_file('/Library/Developer/CommandLineTools/usr/lib/libclang.dylib')
index = clang.cindex.Index.create()
tu = index.parse('./ParsingSample/cf-96100658.c')
ast = parse(tu.cursor)