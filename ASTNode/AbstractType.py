from .AbstractASTNode import AbstractASTNode
from enum import Enum


class ValidType(Enum):
    INT = 1
    BOOL = 2
    VOID = 3
    STRING = 4
    INVALID = 5


class AbstractType(AbstractASTNode):
    internalType = ValidType.INVALID

    def __init__(self, nodeType=None, baseType=ValidType.INVALID):
        self.internalType = baseType
        self.nodeType = nodeType

    def __eq__(self, other):
        if issubclass(other, self.__class__):
            return other.internalType == self.internalType
        return False
