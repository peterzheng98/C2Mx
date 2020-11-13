from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType


class StringLiteral(AbstractASTNode):
    value = ''

    def __init__(self, position, nodeType, spelling):
        self.originalPosition = position
        self.value = spelling
        self.nodeType = nodeType

    def generateMx(self) -> str:
        return self.value


class IntegerLiteral(AbstractASTNode):
    value = 0

    def __init__(self, position, nodeType, spelling):
        self.originalPosition = position
        self.value = spelling
        self.nodeType = nodeType

    def generateMx(self) -> str:
        return '{}'.format(self.value)
