from .AbstractASTNode import AbstractASTNode


class CompoundStmt(AbstractASTNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType
