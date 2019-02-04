from enum import Enum


class Expr:
    output_size = 1


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
        assert left.output_size == 1, "Only scalars are supported"
        assert right.output_size == 1, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinNumExpr(" + args + ")"


# Vector Expressions.

class VectorExpr(Expr):
    pass


class VectorVal(VectorExpr):

    def __init__(self, exprs):
        assert all(map(lambda e: e.output_size == 1, exprs)), (
            "All expressions for VectorVal must be scalar")

        self.exprs = exprs
        self.output_size = len(exprs)

    def __str__(self):
        args = ",".join([str(e) for e in self.exprs])
        return "VectorVal([" + args + "])"


class BinVectorExpr(VectorExpr):

    def __init__(self, left, right, op):
        assert left.output_size > 1, "Only vectors are supported"
        assert left.output_size == right.output_size, (
            "Vectors must be of the same size")

        self.left = left
        self.right = right
        self.op = op
        self.output_size = left.output_size

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinVectorExpr(" + args + ")"


class BinVectorNumExpr(VectorExpr):

    def __init__(self, left, right, op):
        assert left.output_size > 1, "Only vectors are supported"
        assert right.output_size == 1, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op
        self.output_size = left.output_size

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinVectorNumExpr(" + args + ")"


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
        assert left.output_size == 1, "Only scalars are supported"
        assert right.output_size == 1, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "CompExpr(" + args + ")"


# Control Expressions.

class CtrlExpr(Expr):
    size = None


class IfExpr(CtrlExpr):
    def __init__(self, test, body, orelse):
        assert body.output_size == orelse.output_size, (
            "body and orelse expressions should have the same output size")

        self.test = test
        self.body = body
        self.orelse = orelse
        self.output_size = body.output_size

    def __str__(self):
        args = ",".join([str(self.test), str(self.body), str(self.orelse)])
        return "IfExpr(" + args + ")"


class TransparentExpr(CtrlExpr):
    def __init__(self, expr):
        self.expr = expr
        self.output_size = expr.output_size


class SubroutineExpr(TransparentExpr):

    def __str__(self):
        return "SubroutineExpr(" + str(self.expr) + ")"
