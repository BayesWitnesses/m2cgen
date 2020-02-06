import lightgbm
import numpy as np
from tests import utils
from m2cgen import assemblers, ast


def test_binary_classification():
    estimator = lightgbm.LGBMClassifier(n_estimators=2, random_state=1,
                                        max_depth=1)
    utils.get_binary_classification_model_trainer()(estimator)

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
                                ast.SubroutineExpr(
                                    ast.IfExpr(
                                        ast.CompExpr(
                                            ast.FeatureRef(23),
                                            ast.NumVal(868.2000000000002),
                                            ast.CompOpType.GT),
                                        ast.NumVal(0.25986931215073095),
                                        ast.NumVal(0.6237178414050242))),
                                ast.BinNumOpType.ADD),
                            ast.SubroutineExpr(
                                ast.IfExpr(
                                    ast.CompExpr(
                                        ast.FeatureRef(7),
                                        ast.NumVal(0.05142),
                                        ast.CompOpType.GT),
                                    ast.NumVal(-0.1909605544006228),
                                    ast.NumVal(0.1293965108676673))),
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
                ast.SubroutineExpr(
                  ast.NumVal(-1.0986122886681098)),
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
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(5),
                            ast.NumVal(6.918),
                            ast.CompOpType.GT),
                        ast.NumVal(24.011454621684155),
                        ast.NumVal(22.289277544391084))),
                ast.BinNumOpType.ADD),
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(9.63),
                        ast.CompOpType.GT),
                    ast.NumVal(-0.49461212269771115),
                    ast.NumVal(0.7174324413014594))),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_regression_random_forest():
    estimator = lightgbm.LGBMRegressor(boosting_type="rf", n_estimators=2,
                                       random_state=1, max_depth=1,
                                       subsample=0.7, subsample_freq=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.SubroutineExpr(
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(5),
                                ast.NumVal(6.954000000000001),
                                ast.CompOpType.GT),
                            ast.NumVal(37.24347877367631),
                            ast.NumVal(19.936999995530854))),
                    ast.BinNumOpType.ADD),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(5),
                            ast.NumVal(6.971500000000001),
                            ast.CompOpType.GT),
                        ast.NumVal(38.48600037864964),
                        ast.NumVal(20.183783757300255))),
                ast.BinNumOpType.ADD),
            ast.NumVal(0.5),
            ast.BinNumOpType.MUL))

    assert utils.cmp_exprs(actual, expected)
