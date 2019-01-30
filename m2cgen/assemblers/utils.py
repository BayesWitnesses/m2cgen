import numpy as np
from m2cgen import ast


def mul(l, r):
    return ast.BinNumExpr(l, r, ast.BinNumOpType.MUL)


def lte(l, r):
    return ast.CompExpr(l, r, ast.CompOpType.LTE)


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
        (left.is_vector_output, right.is_vector_output))
    if exr_class is None:
        # change the positions of left and right
        left, right = right, left
        exr_class = ast.BinVectorNumExpr

    return exr_class(left, right, op)


def apply_op_to_expressions(op, *exprs):
    if len(exprs) < 2:
        raise ValueError("At least two expressions are required")

    def _inner(current_expr, *rest_exprs):
        if not rest_exprs:
            return current_expr

        return _inner(
            apply_bin_op(current_expr, rest_exprs[0], op), *rest_exprs[1:])

    return _inner(apply_bin_op(exprs[0], exprs[1], op), *exprs[2:])


def to_1d_array(var):
    return np.reshape(np.asarray(var), (np.size(var)))


def to_2d_array(var):
    if len(np.shape(var)) == 2:
        x, y = var.shape
    else:
        x, y = 1, np.size(var)
    return np.reshape(np.asarray(var), (x, y))
