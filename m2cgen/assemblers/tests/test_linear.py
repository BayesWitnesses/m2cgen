import numpy as np
from sklearn import linear_model

from m2cgen import assemblers, ast
from m2cgen.assemblers.tests import utils


def test_single_feature():
    estimator = linear_model.LinearRegression()
    utils.train_model(estimator, 1)

    assembler = assemblers.LinearRegressionAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(np.float32(24.123604)),
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(np.float32(-0.4176014)),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_two_features():
    estimator = linear_model.LinearRegression()
    utils.train_model(estimator, 2)

    assembler = assemblers.LinearRegressionAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(np.float32(22.466934)),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(np.float32(-0.35059974)),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(np.float32(0.120529264)),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
