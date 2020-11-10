from .AbstractASTNode import AbstractASTNode
from enum import Enum
from utils import *


class ValidType(Enum):
    INT = 1
    BOOL = 2
    VOID = 3
    STRING = 4
    INVALID = 5


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


class AbstractType(AbstractASTNode):
    internalType = ValidType.INVALID

    def __init__(self, nodeType=None, baseType=ValidType.INVALID):
        self.internalType = baseType
        self.nodeType = nodeType

    def __eq__(self, other):
        if issubclass(other, self.__class__):
            return other.internalType == self.internalType
        return False