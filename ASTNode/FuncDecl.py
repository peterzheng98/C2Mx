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

    def addParm(self, parm_node):
        self.params.append(parm_node)

    def __repr__(self):
        return 'Function: {}, return: {}'.format(self.spelling, self.returnType)


class ParmDecl(AbstractASTNode):
    spelling = ''
    returnType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType):
        self.originalPosition = position
        self.spelling = spelling
        self.returnType = AbstractType(returnType)
        self.nodeType = nodeType
