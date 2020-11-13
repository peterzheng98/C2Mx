from .AbstractASTNode import AbstractASTNode
from enum import Enum
from utils import *
import sys
import clang.cindex

from clang.cindex import CursorKind, TypeKind


class ValidType(Enum):
    INT = 1
    BOOL = 2
    VOID = 3
    STRING = 4
    INVALID = 5

    def __repr__(self):
        return self.name.lower()


def _base_to_validType(baseType: str):
    if baseType == 'int':
        return ValidType(1)
    if baseType == 'bool':
        return ValidType(2)
    if baseType == 'void':
        return ValidType(3)
    if baseType == 'string':
        return ValidType(4)
    debug('Type not valid, received {}'.format(baseType))
    return ValidType(5)


def _type_kind_to_validType(tk, spelling=''):
    if tk == TypeKind.FUNCTIONPROTO or tk == TypeKind.FUNCTIONNOPROTO:
        return _base_to_validType(spelling.split('(')[0].strip())
    if tk == TypeKind.CONSTANTARRAY:
        return ArrayType(spelling)
    if tk == TypeKind.INT:
        return ValidType(1)
    if tk == TypeKind.BOOL:
        return ValidType(2)
    if tk == TypeKind.VOID:
        return ValidType(3)
    # if tk == 'string':
    #     return ValidType(4)
    # No string currently found
    debug('Type not valid, received {}'.format(tk))
    return ValidType(5)


class AbstractType(AbstractASTNode):
    internalType = ValidType.INVALID

    def __init__(self, nodeType=None):
        self.internalType = nodeType
        self.nodeType = nodeType

    def __eq__(self, other):
        if issubclass(other, self.__class__):
            return other.internalType == self.internalType
        return False

    def __repr__(self):
        return self.nodeType.name


class ArrayType(AbstractType):
    baseType = ValidType.INVALID
    length = []

    def _dfs(self, type: clang.cindex.Type):
        if type.kind == TypeKind.CONSTANTARRAY:
            self._dfs(type.element_type)
            self.length = [type.element_count] + self.length
        else:
            self.baseType = _base_to_validType(type.spelling)

    def __init__(self, type: clang.cindex.Type):
        self._dfs(type)
        print(repr(self))

    def __repr__(self):
        return repr(self.baseType) + repr(self.length)

    def generateNoLength(self):
        return repr(self.baseType) + '[]' * len(self.length)

    def generateWithLength(self):
        st = ''
        for i in self.length:
            st = st + '[{}]'.format(i)
        return repr(self.baseType) + st
