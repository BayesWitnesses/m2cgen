import lightgbm
import numpy as np
from tests import utils
from m2cgen import assemblers, ast


def test_binary_classification():
    estimator = lightgbm.LGBMClassifier(n_estimators=2, random_state=1,
                                        max_depth=1)
    utils.train_model_classification_binary(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(
            ast.NumVal(1),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.SubroutineExpr(
                        ast.BinNumExpr(
                            ast.BinNumExpr(
                                ast.NumVal(0),
                                ast.IfExpr(
                                    ast.CompExpr(
                                        ast.FeatureRef(23),
                                        ast.NumVal(868.2000000000002),
                                        ast.CompOpType.LTE),
                                    ast.NumVal(0.6399134166614473),
                                    ast.NumVal(0.2762557140263451)),
                                ast.BinNumOpType.ADD),
                            ast.IfExpr(
                                ast.CompExpr(
                                    ast.FeatureRef(27),
                                    ast.NumVal(0.14205000000000004),
                                    ast.CompOpType.LTE),
                                ast.NumVal(0.1151466338793227),
                                ast.NumVal(-0.2139321843285849)),
                            ast.BinNumOpType.ADD)),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV,
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = lightgbm.LGBMClassifier(n_estimators=1, random_state=1,
                                        max_depth=1)
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    exponent = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.NumVal(-1.0986122886681098),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    exponent_sum = ast.BinNumExpr(
        ast.BinNumExpr(exponent, exponent, ast.BinNumOpType.ADD),
        exponent,
        ast.BinNumOpType.ADD,
        to_reuse=True)

    softmax = ast.BinNumExpr(exponent, exponent_sum, ast.BinNumOpType.DIV)

    expected = ast.VectorVal([softmax] * 3)

    assert utils.cmp_exprs(actual, expected)


def test_regression():
    estimator = lightgbm.LGBMRegressor(n_estimators=2, random_state=1,
                                       max_depth=1)
    utils.train_model_regression(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.8455),
                        ast.CompOpType.LTE),
                    ast.NumVal(22.35695742616179),
                    ast.NumVal(24.007392728914056)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.63),
                    ast.CompOpType.LTE),
                ast.NumVal(0.7222498915097475),
                ast.NumVal(-0.4903836928981587)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)
