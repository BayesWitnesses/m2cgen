from sklearn import ensemble

from m2cgen import assemblers, ast
from tests import utils


def test_single_condition():
    estimator = ensemble.RandomForestRegressor(n_estimators=2, random_state=1)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.RandomForestModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.SubroutineExpr(
                ast.NumVal(1.0)),
            ast.NumVal(0.5),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(1.5),
                        ast.CompOpType.LTE),
                    ast.NumVal(1.0),
                    ast.NumVal(2.0))),
            ast.NumVal(0.5),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_two_conditions():
    estimator = ensemble.RandomForestRegressor(n_estimators=2, random_state=13)

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.RandomForestModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(1.5),
                        ast.CompOpType.LTE),
                    ast.NumVal(1.0),
                    ast.NumVal(2.0))),
            ast.NumVal(0.5),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(2.5),
                        ast.CompOpType.LTE),
                    ast.NumVal(2.0),
                    ast.NumVal(3.0))),
            ast.NumVal(0.5),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
