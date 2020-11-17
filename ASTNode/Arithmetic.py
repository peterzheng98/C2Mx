from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class UnaryOp(AbstractASTNode):
    search_list = ['~', '-', '--', '++', '&']
    internal_idx = -1

    def __init__(self, op):
        self.internal_idx = self.search_list.index(op)

    def generateMx(self) -> str:
        return self.search_list[self.internal_idx]


class BinaryOp(AbstractASTNode):
    search_list = ['+', '-', '*', '/', '<', '>', '==', '<=', '>=', '!=']
    internal_idx = -1

    def __init__(self, op):
        self.internal_idx = self.search_list.index(op)

    def generateMx(self) -> str:
        return self.search_list[self.internal_idx]


class UnaryExpr(AbstractASTNode):
    op = None
    target = None

    def __init__(self, position, nodeType, op, target):
        self.originalPosition = position
        self.op = UnaryOp(op)
        self.nodeType = nodeType
        self.target = target

    def generateMx(self) -> str:
        return self.op.generateMx() + self.target.generateMx()


class ArraySubscribeExpr(AbstractASTNode):
    base = None
    idx = None

    def __init__(self, position, nodeType, base, idx):
        self.originalPosition = position
        self.nodeType = nodeType
        self.base = base
        self.idx = idx

    def generateMx(self) -> str:
        return self.base.generateMx() + '[{}]'.format(self.idx.generateMx())


class BinaryExpr(AbstractASTNode):
    leftExpr = None
    rightExpr = None
    op = None

    def __init__(self, position, nodeType, op, left, right):
        self.originalPosition = position
        self.op = BinaryOp(op)
        self.nodeType = nodeType
        self.leftExpr = left
        self.rightExpr = right

    def generateMx(self) -> str:
        return self.leftExpr.generateMx() + self.op.generateMx() + self.rightExpr.generateMx()


class ParenExpr(AbstractASTNode):
    core = None

    def __init__(self, position, nodeType, core):
        self.originalPosition = position
        self.nodeType = nodeType
        self.core = core

    def generateMx(self) -> str:
        return '(' + self.core.generateMx() + ')'
