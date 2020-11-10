import clang
import sys
import clang.cindex

from clang.cindex import Config
from clang.cindex import Cursor
from clang.cindex import CursorKind
from ASTNode import *


def parse_param_decl(cursor: Cursor):
    assert cursor.kind == Cursor.PARM_DECL, "Node type is {}, not PARM_DECL".format(cursor.kind)
    functionDeclNode = FuncDecl((cursor.extent.start.offset, cursor.extent.end.offset), cursor.kind, cursor.spelling, )
    return


def parse_function_decl(cursor: Cursor):
    assert cursor.kind == cursor.FUNCTION_DECL, "Node type is {}, not FUNCTION_DECL".format(cursor.kind)
    return
