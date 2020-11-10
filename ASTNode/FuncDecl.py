from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType


class FuncDecl(AbstractASTNode):
    spelling = ''
    params = []
    returnType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType, params: list):
        self.originalPosition = position
        self.spelling = spelling
        self.returnType = AbstractType(returnType)
        self.params = params
        self.nodeType = nodeType
