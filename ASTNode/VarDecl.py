from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class VarDecl(AbstractASTNode):
    spelling = ''
    declType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType):
        self.originalPosition = position
        self.spelling = spelling
        self.declType = AbstractType(returnType)
        self.nodeType = nodeType

    def generateMx(self) -> str:
        if isinstance(self.declType.nodeType, ArrayType):
            return '\t{} {} = new {};'.format(
                self.declType.nodeType.generateNoLength(), self.spelling, self.declType.nodeType.generateWithLength()
            )
        else:
            return '\t{} {};'.format(repr(self.declType.nodeType), self.spelling)
