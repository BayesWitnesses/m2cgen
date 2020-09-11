from enum import Enum
from inspect import getmembers, isclass
from sys import modules

import numpy as np


class Expr:
    output_size = 1
    # Setting this value to true serves as an indication that the result
    # of evaluation of this expression is being used in other expressions
    # and it's recommended to persist or cache it in some way.
    # The actual caching mechanism (if any) is left up to a specific
    # interpreter implementation to provide.
    to_reuse = False


class IdExpr(Expr):
    def __init__(self, expr, to_reuse=False):
        self.expr = expr
        self.to_reuse = to_reuse
        self.output_size = expr.output_size

    def __str__(self):
        return f"IdExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is IdExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class FeatureRef(Expr):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return f"FeatureRef({self.index})"

    def __eq__(self, other):
        return type(other) is FeatureRef and self.index == other.index

    def __hash__(self):
        return hash(self.index)


class BinExpr(Expr):
    pass


# Numeric Expressions.

class NumExpr(Expr):
    pass


class NumVal(NumExpr):
    def __init__(self, value, dtype=np.float64):
        self.value = dtype(value)

    def __str__(self):
        return f"NumVal({self.value})"

    def __eq__(self, other):
        return type(other) is NumVal and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class AbsExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"AbsExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is AbsExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class AtanExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"AtanExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is AtanExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class ExpExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"ExpExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is ExpExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class LogExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"LogExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is LogExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class Log1pExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"Log1pExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is Log1pExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class SqrtExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"SqrtExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is SqrtExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class TanhExpr(NumExpr):
    def __init__(self, expr, to_reuse=False):
        assert expr.output_size == 1, "Only scalars are supported"

        self.expr = expr
        self.to_reuse = to_reuse

    def __str__(self):
        return f"TanhExpr({self.expr},to_reuse={self.to_reuse})"

    def __eq__(self, other):
        return type(other) is TanhExpr and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)


class PowExpr(NumExpr):
    def __init__(self, base_expr, exp_expr, to_reuse=False):
        assert base_expr.output_size == 1, "Only scalars are supported"
        assert exp_expr.output_size == 1, "Only scalars are supported"

        self.base_expr = base_expr
        self.exp_expr = exp_expr
        self.to_reuse = to_reuse

    def __str__(self):
        return (f"PowExpr({self.base_expr},{self.exp_expr},"
                f"to_reuse={self.to_reuse})")

    def __eq__(self, other):
        return (type(other) is PowExpr and
                self.base_expr == other.base_expr and
                self.exp_expr == other.exp_expr)

    def __hash__(self):
        return hash((self.base_expr, self.exp_expr))


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
        return (f"BinNumExpr({self.left},{self.right},{self.op.name},"
                f"to_reuse={self.to_reuse})")

    def __eq__(self, other):
        return _eq_bin_exprs(self, other, type(self))

    def __hash__(self):
        return hash((self.left, self.right, self.op))


# Vector Expressions.

class VectorExpr(Expr):
    pass


class VectorVal(VectorExpr):

    def __init__(self, exprs):
        assert all(e.output_size == 1 for e in exprs), (
            "All expressions for VectorVal must be scalar")

        self.exprs = exprs
        self.output_size = len(exprs)

    def __str__(self):
        args = ",".join([str(e) for e in self.exprs])
        return f"VectorVal([{args}])"

    def __eq__(self, other):
        return (type(other) is VectorVal and
                self.output_size == other.output_size and
                all(i == j for i, j in zip(self.exprs, other.exprs)))

    def __hash__(self):
        return hash(tuple(self.exprs))


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
        return f"BinVectorExpr({self.left},{self.right},{self.op.name})"

    def __eq__(self, other):
        return _eq_bin_exprs(self, other, type(self))

    def __hash__(self):
        return hash((self.left, self.right, self.op))


class BinVectorNumExpr(VectorExpr, BinExpr):

    def __init__(self, left, right, op):
        assert left.output_size > 1, "Only vectors are supported"
        assert right.output_size == 1, "Only scalars are supported"

        self.left = left
        self.right = right
        self.op = op
        self.output_size = left.output_size

    def __str__(self):
        return f"BinVectorNumExpr({self.left},{self.right},{self.op.name})"

    def __eq__(self, other):
        return _eq_bin_exprs(self, other, type(self))

    def __hash__(self):
        return hash((self.left, self.right, self.op))


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
        return f"CompExpr({self.left},{self.right},{self.op.name})"

    def __eq__(self, other):
        return _eq_bin_exprs(self, other, type(self))

    def __hash__(self):
        return hash((self.left, self.right, self.op))


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
        return f"IfExpr({self.test},{self.body},{self.orelse})"

    def __eq__(self, other):
        return (type(other) is IfExpr and
                self.test == other.test and
                self.body == other.body and
                self.orelse == other.orelse)

    def __hash__(self):
        return hash((self.test, self.body, self.orelse))


TOTAL_NUMBER_OF_EXPRESSIONS = len(getmembers(modules[__name__], isclass))


NESTED_EXPRS_MAPPINGS = [
    ((BinExpr, CompExpr), lambda e: [e.left, e.right]),
    (PowExpr, lambda e: [e.base_expr, e.exp_expr]),
    (VectorVal, lambda e: e.exprs),
    (IfExpr, lambda e: [e.test, e.body, e.orelse]),
    ((AbsExpr, AtanExpr, ExpExpr, IdExpr, LogExpr, Log1pExpr,
      SqrtExpr, TanhExpr),
     lambda e: [e.expr]),
]


def count_exprs(expr, exclude_list=None):
    expr_type = type(expr)
    excluded = tuple(exclude_list) if exclude_list else ()

    init = 1
    if issubclass(expr_type, excluded):
        init = 0

    if isinstance(expr, (NumVal, FeatureRef)):
        return init

    for tpes, nested_f in NESTED_EXPRS_MAPPINGS:
        if issubclass(expr_type, tpes):
            return init + sum(map(
                lambda e: count_exprs(e, exclude_list),
                nested_f(expr)))

    expr_type_name = expr_type.__name__
    raise ValueError(f"Unexpected expression type '{expr_type_name}'")


def _eq_bin_exprs(expr_one, expr_two, expected_type):
    return (type(expr_one) is expected_type and
            type(expr_two) is expected_type and
            expr_one.left == expr_two.left and
            expr_one.right == expr_two.right and
            expr_one.op == expr_two.op)
