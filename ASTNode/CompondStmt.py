from .AbstractASTNode import AbstractASTNode


class CompoundStmt(AbstractASTNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    # TODO: remove stub
    def generateMx(self) -> str:
        return '{\n' + '\n'.join([i.generateMx() if i is not None else '-'  for i in self.children]) + '\n}'


class ReturnStmt(AbstractASTNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    def generateMx(self) -> str:
        return 'return' + '\n'.join([i.generateMx() for i in self.children])


class DeclStmt(AbstractASTNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    def generateMx(self) -> str:
        return '\n'.join([i.generateMx() for i in self.children])
