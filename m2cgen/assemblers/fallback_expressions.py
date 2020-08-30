"""This module provides an implementation for a variety of functions
expressed in library's AST.

These AST-based implementations are used as fallbacks in case
when the target language lacks native support for respective functions
provided in this module.
"""
import math

from m2cgen import ast
from m2cgen.assemblers import utils


def abs(expr):
    expr = ast.IdExpr(expr, to_reuse=True)
    return ast.IfExpr(
        utils.lt(expr, ast.NumVal(0.0)),
        utils.sub(ast.NumVal(0.0), expr),
        expr)


def tanh(expr):
    expr = ast.IdExpr(expr, to_reuse=True)
    tanh_expr = utils.sub(
        ast.NumVal(1.0),
        utils.div(
            ast.NumVal(2.0),
            utils.add(
                ast.ExpExpr(
                    utils.mul(
                        ast.NumVal(2.0),
                        expr)),
                ast.NumVal(1.0))))
    return ast.IfExpr(
        utils.gt(expr, ast.NumVal(44.0)),  # exp(2*x) <= 2^127
        ast.NumVal(1.0),
        ast.IfExpr(
            utils.lt(expr, ast.NumVal(-44.0)),
            ast.NumVal(-1.0),
            tanh_expr))


def sqrt(expr):
    return ast.PowExpr(
        base_expr=expr,
        exp_expr=ast.NumVal(0.5))


def exp(expr):
    return ast.PowExpr(
        base_expr=ast.NumVal(math.e),
        exp_expr=expr)


def log1p(expr):
    # Use trick to compute log1p for small values more accurate
    # https://www.johndcook.com/blog/2012/07/25/trick-for-computing-log1x/
    expr = ast.IdExpr(expr, to_reuse=True)
    expr1p = utils.add(ast.NumVal(1.0), expr, to_reuse=True)
    expr1pm1 = utils.sub(expr1p, ast.NumVal(1.0), to_reuse=True)
    return ast.IfExpr(
        utils.eq(expr1pm1, ast.NumVal(0.0)),
        expr,
        utils.div(utils.mul(expr, ast.LogExpr(expr1p)), expr1pm1))


def atan(expr):
    expr = ast.IdExpr(expr, to_reuse=True)
    expr_abs = ast.AbsExpr(expr, to_reuse=True)

    expr_reduced = ast.IdExpr(
        ast.IfExpr(
            utils.gt(expr_abs, ast.NumVal(2.4142135623730950488)),
            utils.div(ast.NumVal(1.0), expr_abs),
            ast.IfExpr(
                utils.gt(expr_abs, ast.NumVal(0.66)),
                utils.div(
                    utils.sub(expr_abs, ast.NumVal(1.0)),
                    utils.add(expr_abs, ast.NumVal(1.0))),
                expr_abs)),
        to_reuse=True)

    P0 = ast.NumVal(-8.750608600031904122785e-01)
    P1 = ast.NumVal(1.615753718733365076637e+01)
    P2 = ast.NumVal(7.500855792314704667340e+01)
    P3 = ast.NumVal(1.228866684490136173410e+02)
    P4 = ast.NumVal(6.485021904942025371773e+01)
    Q0 = ast.NumVal(2.485846490142306297962e+01)
    Q1 = ast.NumVal(1.650270098316988542046e+02)
    Q2 = ast.NumVal(4.328810604912902668951e+02)
    Q3 = ast.NumVal(4.853903996359136964868e+02)
    Q4 = ast.NumVal(1.945506571482613964425e+02)
    expr2 = utils.mul(expr_reduced, expr_reduced, to_reuse=True)
    z = utils.mul(
        expr2,
        utils.div(
            utils.sub(
                utils.mul(
                    expr2,
                    utils.sub(
                        utils.mul(
                            expr2,
                            utils.sub(
                                utils.mul(
                                    expr2,
                                    utils.sub(
                                        utils.mul(
                                            expr2,
                                            P0
                                        ),
                                        P1
                                    )
                                ),
                                P2
                            )
                        ),
                        P3
                    )
                ),
                P4
            ),
            utils.add(
                Q4,
                utils.mul(
                    expr2,
                    utils.add(
                        Q3,
                        utils.mul(
                            expr2,
                            utils.add(
                                Q2,
                                utils.mul(
                                    expr2,
                                    utils.add(
                                        Q1,
                                        utils.mul(
                                            expr2,
                                            utils.add(
                                                Q0,
                                                expr2
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    z = utils.add(utils.mul(expr_reduced, z), expr_reduced)

    ret = utils.mul(
        z,
        ast.IfExpr(
            utils.gt(expr_abs, ast.NumVal(2.4142135623730950488)),
            ast.NumVal(-1.0),
            ast.NumVal(1.0)))
    ret = utils.add(
        ret,
        ast.IfExpr(
            utils.lte(expr_abs, ast.NumVal(0.66)),
            ast.NumVal(0.0),
            ast.IfExpr(
                utils.gt(expr_abs, ast.NumVal(2.4142135623730950488)),
                ast.NumVal(1.570796326794896680463661649),
                ast.NumVal(0.7853981633974483402318308245))))
    ret = utils.mul(
        ret,
        ast.IfExpr(
            utils.lt(expr, ast.NumVal(0.0)),
            ast.NumVal(-1.0),
            ast.NumVal(1.0)))

    return ret


def sigmoid(expr, to_reuse=False):
    neg_expr = ast.BinNumExpr(ast.NumVal(0.0), expr, ast.BinNumOpType.SUB)
    exp_expr = ast.ExpExpr(neg_expr)
    return ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.BinNumExpr(ast.NumVal(1.0), exp_expr, ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV,
        to_reuse=to_reuse)


def softmax(exprs):
    exp_exprs = [ast.ExpExpr(e, to_reuse=True) for e in exprs]
    exp_sum_expr = utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD, *exp_exprs, to_reuse=True)
    return [
        ast.BinNumExpr(e, exp_sum_expr, ast.BinNumOpType.DIV)
        for e in exp_exprs
    ]
