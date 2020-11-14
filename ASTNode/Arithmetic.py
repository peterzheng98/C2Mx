from .AbstractASTNode import AbstractASTNode
from .AbstractType import AbstractType, ValidType, ArrayType


class UnaryExpr(AbstractASTNode):
    op = None
    target = None

    def __init__(self, position, nodeType, op, target):
        self.originalPosition = position
        self.op = op
        self.nodeType = nodeType
        self.target = target
