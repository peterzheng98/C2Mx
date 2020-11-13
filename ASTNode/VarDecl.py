from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType


class VarDecl(AbstractASTNode):
    spelling = ''
    declType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType):
        self.originalPosition = position
        self.spelling = spelling
        self.declType = AbstractType(returnType)
        self.nodeType = nodeType

    def generateMx(self) -> str:
        return ''