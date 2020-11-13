from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType


class VarDecl(AbstractASTNode):
    spelling = ''
    returnType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType):
        self.originalPosition = position
        self.spelling = spelling
        self.returnType = AbstractType(returnType)
        self.nodeType = nodeType
