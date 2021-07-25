from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from m2cgen import ast
from m2cgen.assemblers import TreeModelAssembler

from tests.utils import cmp_exprs


def test_single_condition():
    estimator = DecisionTreeRegressor()

    estimator.fit([[1], [2]], [1, 2])

    assembler = TreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.NumVal(1.0),
        ast.NumVal(2.0))

    assert cmp_exprs(actual, expected)


def test_two_conditions():
    estimator = DecisionTreeRegressor()

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = TreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.NumVal(1.0),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(0),
                ast.NumVal(2.5),
                ast.CompOpType.LTE),
            ast.NumVal(2.0),
            ast.NumVal(3.0)))

    assert cmp_exprs(actual, expected)


def test_multi_class():
    estimator = DecisionTreeClassifier()

    estimator.fit([[1], [2], [3]], [0, 1, 2])

    assembler = TreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.VectorVal([
            ast.NumVal(1.0),
            ast.NumVal(0.0),
            ast.NumVal(0.0)]),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(0),
                ast.NumVal(2.5),
                ast.CompOpType.LTE),
            ast.VectorVal([
                ast.NumVal(0.0),
                ast.NumVal(1.0),
                ast.NumVal(0.0)]),
            ast.VectorVal([
                ast.NumVal(0.0),
                ast.NumVal(0.0),
                ast.NumVal(1.0)])))

    assert cmp_exprs(actual, expected)
