from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class CallExpr(AbstractASTNode):
    funcName = ''
    args = []

    def __init__(self, position, nodeType, spelling, args: list):
        self.originalPosition = position
        self.funcName = spelling
        self.args = args
        self.nodeType = nodeType

    def addArgs(self, argNode):
        self.args.append(argNode)

    # TODO: remove stub
    def generateMx(self) -> str:
        return self.funcName + '(' + ','.join([i.generateMx() if i is not None else '-' for i in self.args]) + ')'
