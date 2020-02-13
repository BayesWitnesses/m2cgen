import pytest
import numpy as np
from sklearn import linear_model
from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor

from m2cgen import assemblers, ast
from tests import utils


def test_single_feature():
    estimator = linear_model.LinearRegression()
    estimator.coef_ = [1]
    estimator.intercept_ = 3

    assembler = assemblers.LinearModelAssembler(estimator)
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

    assembler = assemblers.LinearModelAssembler(estimator)
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


def test_multi_class():
    estimator = linear_model.LogisticRegression()
    estimator.coef_ = np.array([[1, 2], [3, 4], [5, 6]])
    estimator.intercept_ = np.array([7, 8, 9])

    assembler = assemblers.LinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.VectorVal([
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(7),
                    ast.BinNumExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(1),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(1),
                    ast.NumVal(2),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD)),
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(8),
                    ast.BinNumExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(3),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(1),
                    ast.NumVal(4),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD)),
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(9),
                    ast.BinNumExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(5),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(1),
                    ast.NumVal(6),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD))])

    assert utils.cmp_exprs(actual, expected)


def test_binary_class():
    estimator = linear_model.LogisticRegression()
    estimator.coef_ = np.array([[1, 2]])
    estimator.intercept_ = np.array([3])

    assembler = assemblers.LinearModelAssembler(estimator)
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


def test_ransac_custom_base_estimator():
    base_estimator = DecisionTreeRegressor()
    estimator = linear_model.RANSACRegressor(
        base_estimator=base_estimator,
        random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.RANSACModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(2.5),
            ast.CompOpType.LTE),
        ast.NumVal(2.0),
        ast.NumVal(3.0))

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=NotImplementedError, strict=True)
def test_ransac_unknown_base_estimator():
    base_estimator = DummyRegressor()
    estimator = linear_model.RANSACRegressor(
        base_estimator=base_estimator,
        random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.RANSACModelAssembler(estimator)
    assembler.assemble()
