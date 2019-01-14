from m2cgen.ast import *


def mul(l, r):
    return BinNumExpr(l, r, BinNumOpType.MUL)


def apply_op_to_expressions(op, *exprs):
    if len(exprs) < 2:
        raise Exception("At least to expressions required")

    def _inner(current_expr, *rest_exprs):
        if not rest_exprs:
            return current_expr

        return _inner(BinNumExpr(current_expr, rest_exprs[0], op), *rest_exprs[1:])

    return _inner(BinNumExpr(exprs[0], exprs[1], op), *exprs[2:])
