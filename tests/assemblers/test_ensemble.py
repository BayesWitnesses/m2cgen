from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from m2cgen import ast
from m2cgen.assemblers import RandomForestModelAssembler

from tests.utils import cmp_exprs


def test_single_condition():
    estimator = RandomForestRegressor(n_estimators=2, random_state=1)

    estimator.fit([[1], [2]], [1, 2])

    assembler = RandomForestModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(1.0),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(1.5),
                    ast.CompOpType.LTE),
                ast.NumVal(1.0),
                ast.NumVal(2.0)),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert cmp_exprs(actual, expected)


def test_two_conditions():
    estimator = RandomForestRegressor(n_estimators=2, random_state=13)

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = RandomForestModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(1.5),
                    ast.CompOpType.LTE),
                ast.NumVal(1.0),
                ast.NumVal(2.0)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(2.5),
                    ast.CompOpType.LTE),
                ast.NumVal(2.0),
                ast.NumVal(3.0)),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert cmp_exprs(actual, expected)


def test_multi_class():
    estimator = RandomForestClassifier(n_estimators=2, random_state=13)

    estimator.fit([[1], [2], [3]], [1, -1, 1])

    assembler = RandomForestModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinVectorNumExpr(
        ast.BinVectorExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(1.5),
                    ast.CompOpType.LTE),
                ast.VectorVal([
                    ast.NumVal(0.0),
                    ast.NumVal(1.0)]),
                ast.VectorVal([
                    ast.NumVal(1.0),
                    ast.NumVal(0.0)])),
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
                    ast.NumVal(1.0)])),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert cmp_exprs(actual, expected)
