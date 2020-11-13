from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType


class FuncDecl(AbstractASTNode):
    spelling = ''
    params = []
    returnType = AbstractType(nodeType=None)
    statement = None

    def __init__(self, position, nodeType, spelling, returnType: ValidType, params: list):
        self.originalPosition = position
        self.spelling = spelling
        self.returnType = AbstractType(returnType)
        self.params = params
        self.nodeType = nodeType

    def addParm(self, parm_node):
        self.params.append(parm_node)

    def addStmt(self, stmt):
        self.statement = stmt

    def __repr__(self):
        return '<Function: {}, return: {}>'.format(self.spelling, self.returnType)

    def generateMx(self):
        st = '{} {}({})'.format(
                repr(self.returnType.nodeType), self.spelling,
                ','.join([i.generateMx() for i in self.params])
            )
        if self.statement is None:
            return st + ';'
        st = st + self.statement.generateMx()
        return st


class ParmDecl(AbstractASTNode):
    spelling = ''
    returnType = AbstractType(nodeType=None)

    def __init__(self, position, nodeType, spelling, returnType: ValidType):
        self.originalPosition = position
        self.spelling = spelling
        self.returnType = AbstractType(returnType)
        self.nodeType = nodeType

    def generateMx(self):
        return '{} {}'.format(repr(self.returnType.nodeType), self.spelling)
