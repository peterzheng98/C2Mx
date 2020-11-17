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
from clang.cindex import CursorKind, TypeKind

from clang.cindex import Cursor
from ASTNode import *
from ASTNode.AbstractType import _type_kind_to_validType


def parse_var_decl(cursor: Cursor):
    return VarDecl(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling, _type_kind_to_validType(cursor.type.kind, cursor.type)
    )


def parse_parm_decl(cursor: Cursor):
    assert cursor.kind == CursorKind.PARM_DECL, "Node type is {}, not PARM_DECL".format(cursor.kind)
    return ParmDecl(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling, _type_kind_to_validType(cursor.type.kind)
    )


def parse_compound_stmt(cursor: Cursor):
    assert cursor.kind == CursorKind.COMPOUND_STMT, "Node type is {}, not COMPOUND_STMT".format(cursor.kind)
    return CompoundStmt(
        (cursor.extent.start, cursor.extent.end),
        cursor.kind, [parse(i) for i in cursor.get_children()]
    )


def parse_decl_stmt(cursor: Cursor):
    assert cursor.kind == CursorKind.DECL_STMT, "Node type is {}, not DECL_STMT".format(cursor.kind)
    return DeclStmt(
        (cursor.extent.start, cursor.extent.end),
        cursor.kind, [parse(i) for i in cursor.get_children()]
    )


def parse_return_stmt(cursor: Cursor):
    assert cursor.kind == CursorKind.RETURN_STMT, "Node type is {}, not RETURN_STMT".format(cursor.kind)
    return ReturnStmt(
        (cursor.extent.start, cursor.extent.end),
        cursor.kind, [parse(i) for i in cursor.get_children()]
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
        if isinstance(node, CompoundStmt):
            function_decl.addStmt(node)
    return function_decl


def parse_translation_unit(cursor: Cursor):
    assert cursor.kind == CursorKind.TRANSLATION_UNIT, "Node type is {}, not TRANSLATION_UNIT".format(cursor.kind)
    return [parse(i) for i in cursor.get_children()]


def parse_unexposed_expr(cursor: Cursor):
    assert cursor.kind == CursorKind.UNEXPOSED_EXPR, "Node type is {}, not UNEXPOSED_EXPR".format(cursor.kind)
    children = [i for i in cursor.get_children()]
    assert len(children) == 1, 'Length error with more than 1 child in unexposed expression'
    return parse(children[0])


def parse_string_literal(cursor: Cursor):
    assert cursor.kind == CursorKind.STRING_LITERAL, "Node type is {}, not STRING_LITERAL".format(cursor.kind)
    return StringLiteral(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling
    )


def parse_call_expr(cursor: Cursor):
    assert cursor.kind == CursorKind.CALL_EXPR, "Node type is {}, not CALL_EXPR".format(cursor.kind)
    return CallExpr(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, cursor.spelling, [parse(i) for i in cursor.get_arguments()]
    )


def parse_unary_op(cursor: Cursor):
    assert cursor.kind == CursorKind.UNARY_OPERATOR, "Node type is {}, not UNARY_OPERATOR".format(cursor.kind)
    # parsing by token
    l = [i.spelling for i in cursor.get_tokens()]
    operation = l[0] if l[0] in UnaryOp('-').search_list else l[-1]
    children_list = [i for i in cursor.get_children()]
    assert len(children_list) == 1, 'Children list for unary expr should be 1-element.'
    return UnaryExpr(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, operation, parse(children_list[0])
    )


def parse_array_sub_expr(cursor: Cursor):
    assert cursor.kind == CursorKind.ARRAY_SUBSCRIPT_EXPR, "Node type is {}, not ARRAY_SUBSCRIPT_EXPR".format(cursor.kind)
    children_list = [i for i in cursor.get_children()]
    assert len(children_list) == 2, 'Children list for array subscribe expr should be 2-elements.'
    return ArraySubscribeExpr(
        (cursor.extent.start.offset, cursor.extent.end.offset),
        cursor.kind, parse(children_list[0]), parse(children_list[1])
    )


# Todo: fix here: decl reference expression should check the type and set independent node type
def parse_decl_ref_expr(cursor: Cursor):
    assert cursor.kind == CursorKind.DECL_REF_EXPR, "Node type is {}, not DECL_REF_EXPR".format(cursor.kind)
    children_list = [i for i in cursor.get_children()]
    return StringLiteral(
        (cursor.extent.start.offset, cursor.extent.end.offset), cursor.kind, cursor.displayname
    )


def parse_for_stmt(cursor: Cursor):
    assert cursor.kind == CursorKind.FOR_STMT, "Node type is {}, not FOR_STMT".format(cursor.kind)
    children_list = [i for i in cursor.get_children()]
    return ForStmt(
        (cursor.extent.start.offset, cursor.extent.end.offset), cursor.kind,
        parse(children_list[0]), parse(children_list[1]), parse(children_list[2]), parse(children_list[3])
    )


def parse_binary_op(cursor: Cursor):
    assert cursor.kind == CursorKind.BINARY_OPERATOR
    children_list = [i for i in cursor.get_children()]
    assert len(children_list) == 2, 'Children list for binary operation should be 2-elements.'
    left_offset = len([i for i in children_list[0].get_tokens()])
    op = [i for i in cursor.get_tokens()][left_offset].spelling
    return BinaryExpr(
        (cursor.extent.start.offset, cursor.extent.end.offset), cursor.kind,
        op, parse(children_list[0]), parse(children_list[1])
    )


def parse(cursor: Cursor):
    if cursor.kind == CursorKind.TRANSLATION_UNIT:
        return parse_translation_unit(cursor)
    elif cursor.kind == CursorKind.PARM_DECL:
        return parse_parm_decl(cursor)
    elif cursor.kind == CursorKind.FUNCTION_DECL:
        return parse_function_decl(cursor)
    elif cursor.kind == CursorKind.COMPOUND_STMT:
        return parse_compound_stmt(cursor)
    elif cursor.kind == CursorKind.RETURN_STMT:
        return parse_return_stmt(cursor)
    elif cursor.kind == CursorKind.DECL_STMT:
        return parse_decl_stmt(cursor)
    elif cursor.kind == CursorKind.VAR_DECL:
        return parse_var_decl(cursor)
    elif cursor.kind == CursorKind.UNEXPOSED_EXPR:
        return parse_unexposed_expr(cursor)
    elif cursor.kind == CursorKind.CALL_EXPR:
        return parse_call_expr(cursor)
    elif cursor.kind == CursorKind.STRING_LITERAL:
        return parse_string_literal(cursor)
    elif cursor.kind == CursorKind.UNARY_OPERATOR:
        return parse_unary_op(cursor)
    elif cursor.kind == CursorKind.ARRAY_SUBSCRIPT_EXPR:
        return parse_array_sub_expr(cursor)
    elif cursor.kind == CursorKind.DECL_REF_EXPR:
        return parse_decl_ref_expr(cursor)
    elif cursor.kind == CursorKind.FOR_STMT:
        return parse_for_stmt(cursor)
    elif cursor.kind == CursorKind.BINARY_OPERATOR:
        return parse_binary_op(cursor)
    raise NotImplementedError()


# if platform.system() == 'Linux':
#     Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")
# else:
#     Config.set_library_file('/Library/Developer/CommandLineTools/usr/lib/libclang.dylib')
if __name__ == '__main__':
    index = clang.cindex.Index.create()
    tu = index.parse('./ParsingSample/cf-97319761.c')
    ast = parse(tu.cursor)
    for i in ast:
        print(i.generateMx()) if i is not None else None
    print(ast)
