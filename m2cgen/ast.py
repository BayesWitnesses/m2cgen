from enum import Enum


class Expr:
    is_vector_output = False


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
        assert not left.is_vector_output, "Only scalars are supported"
        assert not right.is_vector_output, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinNumExpr(" + args + ")"


# Vector Expressions.

class VectorExpr(Expr):
    is_vector_output = True


class VectorVal(VectorExpr):

    def __init__(self, exprs):
        assert all(map(lambda e: not e.is_vector_output, exprs)), (
            "All expressions for VectorVal must be scalar")

        self.exprs = exprs
        self.size = len(exprs)

    def __str__(self):
        args = ",".join([str(e) for e in self.exprs])
        return "VectorVal([" + args + "])"


class BinVectorExpr(VectorExpr):

    def __init__(self, left, right, op):
        assert left.is_vector_output, "Only vectors are supported"
        assert right.is_vector_output, "Only vectors are supported"

        self.left = left
        self.right = right
        self.op = op
        self.size = left.size

    def __str__(self):
        args = ",".join([str(self.left), str(self.right), self.op.name])
        return "BinVectorExpr(" + args + ")"


class BinVectorNumExpr(VectorExpr):

    def __init__(self, left, right, op):
        assert left.is_vector_output, "Only vectors are supported"
        assert not right.is_vector_output, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op
        self.size = left.size

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
        assert not left.is_vector_output, "Only scalars are supported"
        assert not right.is_vector_output, "Only scalars are supported"

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
        assert not (body.is_vector_output ^ orelse.is_vector_output), (
            "body and orelse expressions should have same is_vector_output")

        self.test = test
        self.body = body
        self.orelse = orelse

        self.is_vector_output = body.is_vector_output
        if self.is_vector_output:
            self.size = body.size

    def __str__(self):
        args = ",".join([str(self.test), str(self.body), str(self.orelse)])
        return "IfExpr(" + args + ")"


class TransparentExpr(CtrlExpr):
    def __init__(self, expr):
        self.expr = expr
        self.is_vector_output = expr.is_vector_output
        if self.is_vector_output:
            self.size = expr.size


class SubroutineExpr(TransparentExpr):

    def __str__(self):
        return "SubroutineExpr(" + str(self.expr) + ")"
