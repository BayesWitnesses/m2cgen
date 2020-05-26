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
        utils.lt(expr, ast.NumVal(0)),
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


def sqrt(expr, to_reuse=False):
    return ast.PowExpr(
        base_expr=expr,
        exp_expr=ast.NumVal(0.5),
        to_reuse=to_reuse)


def exp(expr, to_reuse=False):
    return ast.PowExpr(
        base_expr=ast.NumVal(math.e),
        exp_expr=expr,
        to_reuse=to_reuse)


def sigmoid(expr, to_reuse=False):
    neg_expr = ast.BinNumExpr(ast.NumVal(0), expr, ast.BinNumOpType.SUB)
    exp_expr = ast.ExpExpr(neg_expr)
    return ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(ast.NumVal(1), exp_expr, ast.BinNumOpType.ADD),
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
