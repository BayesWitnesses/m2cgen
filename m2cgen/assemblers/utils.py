import numpy as np
from m2cgen import ast


def mul(l, r):
    return ast.BinNumExpr(l, r, ast.BinNumOpType.MUL)


def lte(l, r):
    return ast.CompExpr(l, r, ast.CompOpType.LTE)


def apply_op_to_expressions(op, *exprs):
    if len(exprs) < 2:
        raise ValueError("At least two expressions are required")

    def _inner(current_expr, *rest_exprs):
        if not rest_exprs:
            return current_expr

        return _inner(ast.BinNumExpr(current_expr, rest_exprs[0], op),
                      *rest_exprs[1:])

    return _inner(ast.BinNumExpr(exprs[0], exprs[1], op), *exprs[2:])


def to_1d_array(var):
    return np.reshape(np.asarray(var), (np.size(var)))


def to_2d_array(var):
    if len(np.shape(var)) == 2:
        x, y = var.shape
    else:
        x, y = 1, np.size(var)
    return np.reshape(np.asarray(var), (x, y))
