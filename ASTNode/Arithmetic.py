from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class UnaryOp(AbstractASTNode):
    search_list = ['~', '-', '--', '++', '&']
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
