from enum import Enum


class Expr:
    output_size = 1
    # Setting this value to true serves as an indication that the result
    # of evaluation of this expression is being used in other expressions
    # and it's recommended to persist or cache it in some way.
    # The actual caching mechanism (if any) is left up to a specific
    # interpreter implementation to provide.
    to_reuse = False


class FeatureRef(Expr):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "FeatureRef(" + str(self.index) + ")"


class BinExpr(Expr):
    pass


# Numeric Expressions.

class NumExpr(Expr):
    pass


class NumVal(NumExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "NumVal(" + str(self.value) + ")"


class ExpExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        args = ",".join([str(self.expr), "to_reuse=" + str(self.to_reuse)])
        return "ExpExpr(" + args + ")"


class TanhExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        args = ",".join([str(self.expr), "to_reuse=" + str(self.to_reuse)])
        return "TanhExpr(" + args + ")"


class PowExpr(NumExpr):
    def __init__(self, base_expr, exp_expr, to_reuse=False):
        assert base_expr.output_size == 1, "Only scalars are supported"
        assert exp_expr.output_size == 1, "Only scalars are supported"

        self.base_expr = base_expr
        self.exp_expr = exp_expr
        self.to_reuse = to_reuse

    def __str__(self):
        args = ",".join([
            str(self.base_expr),
            str(self.exp_expr),
            "to_reuse=" + str(self.to_reuse)
        ])
        return "PowExpr(" + args + ")"


class BinNumOpType(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'


class BinNumExpr(NumExpr, BinExpr):
    def __init__(self, left, right, op, to_reuse=False):
        assert left.output_size == 1, "Only scalars are supported"
        assert right.output_size == 1, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op
        self.to_reuse = to_reuse

    def __str__(self):
        args = ",".join([
            str(self.left),
            str(self.right),
            self.op.name,
            "to_reuse=" + str(self.to_reuse)
        ])
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


class BinVectorExpr(VectorExpr, BinExpr):

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


class BinVectorNumExpr(VectorExpr, BinExpr):

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

    @staticmethod
    def from_str_op(op):
        return COMP_OP_TYPE_MAPPING[op]


COMP_OP_TYPE_MAPPING = {e.value: e for e in CompOpType}


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
    def __init__(self, expr, to_reuse=False):
        super().__init__(expr)
        self.to_reuse = to_reuse

    def __str__(self):
        args = ",".join([str(self.expr), "to_reuse=" + str(self.to_reuse)])
        return "SubroutineExpr(" + args + ")"


NESTED_EXPRS_MAPPINGS = [
    ((BinExpr, CompExpr), lambda e: [e.left, e.right]),
    (PowExpr, lambda e: [e.base_expr, e.exp_expr]),
    (VectorVal, lambda e: e.exprs),
    (IfExpr, lambda e: [e.test, e.body, e.orelse]),
    ((ExpExpr, TanhExpr, TransparentExpr), lambda e: [e.expr]),
]


def count_exprs(expr, exclude_list=None):
    expr_type = type(expr)
    excluded = tuple(exclude_list) if exclude_list else ()

    init = 1
    if issubclass(expr_type, excluded) or \
            issubclass(expr_type, TransparentExpr):
        init = 0

    if isinstance(expr, (NumVal, FeatureRef)):
        return init

    for tpes, nested_f in NESTED_EXPRS_MAPPINGS:
        if issubclass(expr_type, tpes):
            return init + sum(map(
                lambda e: count_exprs(e, exclude_list),
                nested_f(expr)))

    expr_type_name = expr_type.__name__
    raise ValueError("Unexpected expression type {}".format(expr_type_name))
