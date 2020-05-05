from m2cgen import ast
from m2cgen.assemblers import utils


def tanh(expr):
    expr.to_reuse = True
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