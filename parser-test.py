# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import clang


# %%
import sys
import clang.cindex

from clang.cindex import Config
from clang.cindex import Cursor
from clang.cindex import CursorKind


# %%
# if linux
Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")


# %%
# if mac
Config.set_library_file('/Library/Developer/CommandLineTools/usr/lib/libclang.dylib')


# %%
index = clang.cindex.Index.create()
tu = index.parse('./ParsingSample/cf-96100658.c')


# %%
def find_typerefs(node, typename):
    """ Find all references to the type named 'typename'
    """
    if node.kind.is_reference():
        ref_node = clang.cindex.Cursor_ref(node)
        if ref_node.spelling == typename:
            print('Found %s [line=%s, col=%s]' % (
                typename, node.location.line, node.location.column))
    # Recurse for children of this node
    for c in node.get_children():
        find_typerefs(c, typename)


# %%
# A function show(level, *args) would have been simpler but less fun
# and you'd need a separate parameter for the AST walkers if you want it to be exchangeable.
class Level(int):
    '''represent currently visited level of a tree'''

    def show(self, *args):
        '''pretty print an indented line'''
        print('\t' * self + ' '.join(map(str, args)))

    def __add__(self, inc):
        '''increase level'''
        return Level(super(Level, self).__add__(inc))


# %%
def show_ast(cursor, level=Level()):
    '''pretty print cursor AST'''
    if True:
        level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
        for c in cursor.get_children():
            show_ast(c, level + 1)


# %%
def is_valid_type(t):
    '''used to check if a cursor has a type'''
    return t.kind != clang.cindex.TypeKind.INVALID


# %%
def show_type(t, level, title):
    '''pretty print type AST'''
    level.show(title, str(t.kind), ' '.join(qualifiers(t)))
    if is_valid_type(t.get_pointee()):
        show_type(t.get_pointee(), level + 1, 'points to:')


# %%
def qualifiers(t):
    '''set of qualifiers of a type'''
    q = set()
    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    return q


# %%
show_ast(tu.cursor)


# %%
def parsing(cursor: clang.cindex.Cursor):
    if cursor.kind == CursorKind.TRANSLATION_UNIT:
        return
    if cursor.kind == CursorKind.FUNCTION_DECL:
        

