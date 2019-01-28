from enum import Enum


class Expr:
    is_multi_output = False


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


class ArrayExpr(NumExpr):
    is_multi_output = True

    def __init__(self, exprs):
        assert all(map(lambda e: not e.is_multi_output, exprs)), (
            "All expressions for ArrayExpr must be scalar")

        self.exprs = exprs

    def __str__(self):
        args = ",".join([str(e) for e in self.exprs])
        return "ArrayExpr([" + args + "])"


# Boolean Expressions.

class BoolExpr(Expr):
    pass


class CompOpType(Enum):
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    EQ = '=='
    NOT_EQ = '!='


class CompExpr(BoolExpr):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "CompExpr(" + args + ")"


# Control Expressions.

class CtrlExpr(Expr):
    pass


class IfExpr(CtrlExpr):
    def __init__(self, test, body, orelse):
        assert not (body.is_multi_output ^ orelse.is_multi_output), (
            "body and orelse expressions should have same is_multi_output")

        self.test = test
        self.body = body
        self.orelse = orelse

        self.is_multi_output = body.is_multi_output

    def __str__(self):
        args = ",".join([str(self.test), str(self.body), str(self.orelse)])
        return "IfExpr(" + args + ")"


class TransparentExpr(CtrlExpr):
    def __init__(self, expr):
        self.expr = expr
        self.is_multi_output = expr.is_multi_output


class SubroutineExpr(TransparentExpr):

    def __str__(self):
        return "SubroutineExpr(" + str(self.expr) + ")"
