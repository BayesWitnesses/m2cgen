import numpy as np

from m2cgen import ast


def mul(left, right, to_reuse=False):
    return ast.BinNumExpr(left, right, ast.BinNumOpType.MUL, to_reuse=to_reuse)


def div(left, right, to_reuse=False):
    return ast.BinNumExpr(left, right, ast.BinNumOpType.DIV, to_reuse=to_reuse)


def add(left, right, to_reuse=False):
    return ast.BinNumExpr(left, right, ast.BinNumOpType.ADD, to_reuse=to_reuse)


def sub(left, right, to_reuse=False):
    return ast.BinNumExpr(left, right, ast.BinNumOpType.SUB, to_reuse=to_reuse)


def lt(left, right):
    return ast.CompExpr(left, right, ast.CompOpType.LT)


def lte(left, right):
    return ast.CompExpr(left, right, ast.CompOpType.LTE)


def gt(left, right):
    return ast.CompExpr(left, right, ast.CompOpType.GT)


def eq(left, right):
    return ast.CompExpr(left, right, ast.CompOpType.EQ)


BIN_EXPR_CLASSES = {
    (False, False): ast.BinNumExpr,
    (True, True): ast.BinVectorExpr,
    (True, False): ast.BinVectorNumExpr,
}


def apply_bin_op(left, right, op):
    """
    Finds binary expression class suitable for combination of left and right
    expressions depending on whether their output is scalar or vector and
    creates instance of this expression with specified operation.
    """
    exr_class = BIN_EXPR_CLASSES.get(
        (left.output_size > 1, right.output_size > 1))
    if exr_class is None:
        # change the positions of left and right
        left, right = right, left
        exr_class = ast.BinVectorNumExpr

    return exr_class(left, right, op)


def apply_op_to_expressions(op, *exprs, to_reuse=False):
    if len(exprs) < 1:
        raise ValueError("At least one expression is required")
    if len(exprs) == 1:
        return exprs[0]

    def _inner(current_expr, *rest_exprs):
        if not rest_exprs:
            return current_expr

        return _inner(
            apply_bin_op(current_expr, rest_exprs[0], op), *rest_exprs[1:])

    result = _inner(apply_bin_op(exprs[0], exprs[1], op), *exprs[2:])
    result.to_reuse = to_reuse
    return result


def to_1d_array(var):
    return np.ravel(np.asarray(var))


def to_2d_array(var):
    shape = np.shape(var)
    if len(shape) == 2:
        x, y = shape
    else:
        x, y = 1, np.size(var)
    return np.reshape(np.asarray(var), (x, y))
