from .AbstractASTNode import AbstractASTNode, AbstractExprNode
from .AbstractType import AbstractType, ValidType, ArrayType


class CallExpr(AbstractASTNode, AbstractExprNode):
    funcName = ''
    args = []

    def __init__(self, position, nodeType, spelling, args: list):
        self.originalPosition = position
        self.funcName = spelling
        self.args = args
        self.nodeType = nodeType

    def addArgs(self, argNode):
        self.args.append(argNode)

    def generateMx(self) -> str:
        return self.funcName + '(' + ','.join([i.generateMx() for i in self.args]) + ')'
