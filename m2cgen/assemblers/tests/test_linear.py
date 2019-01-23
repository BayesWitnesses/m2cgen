from sklearn import linear_model

from m2cgen import assemblers, ast
from m2cgen.assemblers.tests import utils


def test_single_feature():
    estimator = linear_model.LinearRegression()
    estimator.coef_ = [1]
    estimator.intercept_ = 3

    assembler = assemblers.LinearRegressionAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(3),
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(1),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_two_features():
    estimator = linear_model.LinearRegression()
    estimator.coef_ = [1, 2]
    estimator.intercept_ = 3

    assembler = assemblers.LinearRegressionAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(3),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(1),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(2),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
