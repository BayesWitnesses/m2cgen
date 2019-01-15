from enum import Enum


class Expr:
    pass


class FeatureRef(Expr):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "FeatureRef(" + str(self.index) + ")"


# Numeric Expressions.

class NumExpr(Expr):
    pass


class NumVal(NumExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "NumVal(" + str(self.value) + ")"


class BinNumOpType(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'


class BinNumExpr(NumExpr):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinNumExpr(" + args + ")"


# Boolean Expressions.

class BoolExpr(Expr):
    pass


class BoolVal(BoolExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "BoolVal(" + str(self.value) + ")"


class BinBoolOpType(Enum):
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    EQ = '=='


class BinBoolExpr(BoolExpr):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinBoolExpr(" + args + ")"


class UnaryBoolOpType(Enum):
    NOT = 0


class UnaryBoolExpr(BoolExpr):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op

    def __str__(self):
        args = ",".join([str(self.expr), self.op.name])
        return "UnaryBoolExpr(" + args + ")"


# Control Expressions.

class CtrlExpr(Expr):
    pass


class IfExpr(CtrlExpr):
    def __init__(self, test, body, orelse):
        self.test = test
        self.body = body
        self.orelse = orelse

    def __str__(self):
        args = ",".join([str(self.test), str(self.body), self.orelse])
        return "IfExpr(" + args + ")"
