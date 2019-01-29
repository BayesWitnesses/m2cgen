from sklearn import tree

from m2cgen import assemblers, ast
from tests import utils


def test_single_condition():
    estimator = tree.DecisionTreeRegressor()

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.TreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.NumVal(1.0),
        ast.NumVal(2.0))

    assert utils.cmp_exprs(actual, expected)


def test_two_conditions():
    estimator = tree.DecisionTreeRegressor()

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.TreeModelAssembler(estimator)
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

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = tree.DecisionTreeClassifier()

    estimator.fit([[1], [2], [3]], [1, -1, 1])

    assembler = assemblers.TreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.VectorVal([
            ast.NumVal(0.0),
            ast.NumVal(1.0)]),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(0),
                ast.NumVal(2.5),
                ast.CompOpType.LTE),
            ast.VectorVal([
                ast.NumVal(1.0),
                ast.NumVal(0.0)]),
            ast.VectorVal([
                ast.NumVal(0.0),
                ast.NumVal(1.0)])))

    assert utils.cmp_exprs(actual, expected)
