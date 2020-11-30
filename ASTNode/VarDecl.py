from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class VarDecl(AbstractASTNode):
    spelling = ''
    declType = AbstractType(nodeType=None)
    initialValue = None

    def __init__(self, position, nodeType, spelling, returnType: ValidType, initialValue=None):
        self.originalPosition = position
        self.spelling = spelling
        self.declType = AbstractType(returnType)
        self.nodeType = nodeType
        self.initialValue = initialValue

    def generateMx(self) -> str:
        if isinstance(self.declType.nodeType, ArrayType):
            return '{} {} = new {}'.format(
                self.declType.nodeType.generateNoLength(), self.spelling, self.declType.nodeType.generateWithLength()
            )
        elif self.initialValue is None:
            return '{} {}'.format(repr(self.declType.nodeType), self.spelling)
        else:
            return '{} {} = {}'.format(repr(self.declType.nodeType), self.spelling, self.initialValue.generateMx())