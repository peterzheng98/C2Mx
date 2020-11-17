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


class ForStmt(AbstractASTNode):
    forInitial = None
    forCond = None
    forTermination = None
    forStmt = None

    def __init__(self, position, nodeType, initial, cond, term, stmt):
        self.originalPosition = position
        self.nodeType = nodeType
        self.forInitial = initial
        self.forCond = cond
        self.forTermination = term
        self.forStmt = stmt

    def generateMx(self) -> str:
        return 'for({};{};{})'.format(
            self.forInitial.generateMx(), self.forCond.generateMx(), self.forTermination.generateMx()
        ) + self.forStmt.generateMx()


class NoneStmt(AbstractASTNode):
    def __init__(self):
        self.originalPosition = None
        self.nodeType = None

    def generateMx(self) -> str:
        return ''


class IfStmt(AbstractASTNode):
    ifCond = None
    ifThen = None
    ifElse = None

    def __init__(self, position, nodeType, cond, thenStmt, elseStmt=NoneStmt()):
        self.originalPosition = position
        self.nodeType = nodeType
        self.ifCond = cond
        self.ifThen = thenStmt
        self.ifElse = elseStmt

    def generateMx(self) -> str:
        retStr = 'if({})'.format(self.ifCond.generateMx()) + self.ifThen.generateMx()
        if not isinstance(self.ifElse, NoneStmt):
            retStr += 'else' + self.ifElse.generateMx()
        return retStr
