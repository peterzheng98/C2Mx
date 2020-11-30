from .AbstractASTNode import AbstractASTNode, AbstractExprNode, AbstractStmtNode

TabSizeValue = 0


class CompoundStmt(AbstractASTNode, AbstractStmtNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    def generateMx(self) -> str:
        global TabSizeValue
        TabSizeValue = TabSizeValue + 1
        split_str = '\n'
        after_tab = '\n{}'.format('\t' * (TabSizeValue - 1))
        res_str = '{\n' + split_str.join(['\t' * TabSizeValue + i.generateMx() + (';' if isinstance(i, AbstractExprNode) else '') for i in self.children]) + after_tab + '}'
        TabSizeValue = TabSizeValue - 1
        return res_str


class ReturnStmt(AbstractASTNode, AbstractExprNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    def generateMx(self) -> str:
        return 'return ' + '\n'.join([i.generateMx() for i in self.children])


class DeclStmt(AbstractASTNode, AbstractStmtNode):
    children = []

    def __init__(self, position, nodeType, children):
        self.children = children
        self.originalPosition = position
        self.nodeType = nodeType

    def addChildren(self, childNode):
        self.children.append(childNode)

    def generateMx(self) -> str:
        global TabSizeValue
        baseTab = '\n{}'.format('\t' * TabSizeValue)
        retStr = baseTab.join([i.generateMx() + ';' for i in self.children])
        return retStr


class ForStmt(AbstractASTNode, AbstractStmtNode):
    forInitial = None
    forCond = None
    forTermination = None
    forStmt = None

    def __init__(self, position, nodeType, initial, cond, term, stmt):
        self.originalPosition = position
        self.nodeType = nodeType
        self.forInitial = initial if not isinstance(initial, DeclStmt) else initial.children[0]
        self.forCond = cond
        self.forTermination = term
        self.forStmt = stmt

    def generateMx(self) -> str:
        global TabSizeValue
        oldTabSizeValue = TabSizeValue
        TabSizeValue = 0
        baseStr = 'for({};{};{})'.format(self.forInitial.generateMx(), self.forCond.generateMx(), self.forTermination.generateMx())
        TabSizeValue = oldTabSizeValue
        baseStr += self.forStmt.generateMx()
        return baseStr


class NoneStmt(AbstractASTNode, AbstractStmtNode):
    def __init__(self):
        self.originalPosition = None
        self.nodeType = None

    def generateMx(self) -> str:
        return ''


class IfStmt(AbstractASTNode, AbstractStmtNode):
    ifCond = None
    ifThen = None
    ifElse = None

    def __init__(self, position, nodeType, cond, thenStmt, elseStmt=NoneStmt()):
        self.originalPosition = position
        self.nodeType = nodeType
        self.ifCond = cond
        if not isinstance(thenStmt, CompoundStmt):
            stmt = CompoundStmt(position, nodeType, [])
            stmt.addChildren(thenStmt)
            self.ifThen = stmt
        else:
            self.ifThen = thenStmt
        if not isinstance(thenStmt, CompoundStmt) and not isinstance(elseStmt, NoneStmt):
            stmt2 = CompoundStmt(position, nodeType, [])
            stmt2.addChildren(elseStmt)
            self.ifElse = stmt2
        else:
            self.ifElse = elseStmt

    def generateMx(self) -> str:
        retStr = 'if({})'.format(self.ifCond.generateMx()) + self.ifThen.generateMx()
        if not isinstance(self.ifElse, NoneStmt):
            retStr += ' else ' + self.ifElse.generateMx()
        return retStr


class ContinueStmt(AbstractASTNode, AbstractExprNode):
    def __init__(self, position, nodeType):
        self.originalPosition = position
        self.nodeType = nodeType

    def generateMx(self) -> str:
        return 'continue'


class BreakStmt(AbstractASTNode, AbstractExprNode):
    def __init__(self, position, nodeType):
        self.originalPosition = position
        self.nodeType = nodeType

    def generateMx(self) -> str:
        return 'break'
