import clang
import sys
import clang.cindex
import platform

from clang.cindex import Config

if platform.system() == 'Linux':
    Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")
else:
    Config.set_library_file('/Library/Developer/CommandLineTools/usr/lib/libclang.dylib')

from clang.cindex import Cursor
from clang.cindex import CursorKind

from clang.cindex import Cursor
from ASTNode import *
from ASTNode.AbstractType import _type_kind_to_validType


def parse_parm_decl(cursor: Cursor):
    assert cursor.kind == CursorKind.PARM_DECL, "Node type is {}, not PARM_DECL".format(cursor.kind)
    return ParmDecl(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling, _type_kind_to_validType(cursor.type.kind)
    )


def parse_function_decl(cursor: Cursor):
    assert cursor.kind == CursorKind.FUNCTION_DECL, "Node type is {}, not FUNCTION_DECL".format(cursor.kind)
    function_decl = FuncDecl(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling, _type_kind_to_validType(cursor.type.kind, cursor.type.spelling), []
    )
    for child in cursor.get_children():
        node = parse(child)
        if isinstance(node, ParmDecl):
            function_decl.addParm(node)
    return function_decl


def parse_translation_unit(cursor: Cursor):
    assert cursor.kind == CursorKind.TRANSLATION_UNIT, "Node type is {}, not TRANSLATION_UNIT".format(cursor.kind)
    return [parse(i) for i in cursor.get_children()]


def parse(cursor: Cursor):
    if cursor.kind == CursorKind.TRANSLATION_UNIT:
        return parse_translation_unit(cursor)
    elif cursor.kind == CursorKind.PARM_DECL:
        return parse_parm_decl(cursor)
    elif cursor.kind == CursorKind.FUNCTION_DECL:
        return parse_function_decl(cursor)
    return None


# if platform.system() == 'Linux':
#     Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")
# else:
#     Config.set_library_file('/Library/Developer/CommandLineTools/usr/lib/libclang.dylib')
if __name__ == '__main__':
    index = clang.cindex.Index.create()
    tu = index.parse('./ParsingSample/cf-96100658.c')
    ast = parse(tu.cursor)
    print(ast)
