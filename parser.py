import clang
import sys
import clang.cindex

from clang.cindex import Config
from clang.cindex import Cursor
from clang.cindex import CursorKind

Config.set_library_file("/usr/lib/llvm-10/lib/libclang-10.so.1")
index = clang.cindex.Index.create()
tu = index.parse('./ParsingSample/cf-96100658.c')
