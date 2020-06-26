import lightgbm
import numpy as np

from m2cgen import assemblers, ast
from tests import utils


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
                    ast.BinNumExpr(
                        ast.NumVal(1.0),
                        ast.BinNumExpr(
                            ast.BinNumExpr(
                                ast.NumVal(0),
                                ast.IfExpr(
                                    ast.CompExpr(
                                        ast.FeatureRef(23),
                                        ast.NumVal(868.2),
                                        ast.CompOpType.GT),
                                    ast.NumVal(0.2598693122),
                                    ast.NumVal(0.6237178414)),
                                ast.BinNumOpType.ADD),
                            ast.IfExpr(
                                ast.CompExpr(
                                    ast.FeatureRef(7),
                                    ast.NumVal(0.05142),
                                    ast.CompOpType.GT),
                                ast.NumVal(-0.1909605544),
                                ast.NumVal(0.1293965109)),
                            ast.BinNumOpType.ADD),
                        ast.BinNumOpType.MUL),
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
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.NumVal(-1.0986122886681098),
            ast.BinNumOpType.ADD),
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

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(0),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.918),
                    ast.CompOpType.GT),
                ast.NumVal(24.011454621684155),
                ast.NumVal(22.289277544391084)),
            ast.BinNumOpType.ADD),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(12),
                ast.NumVal(9.63),
                ast.CompOpType.GT),
            ast.NumVal(-0.49461212269771115),
            ast.NumVal(0.7174324413014594)),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_regression_random_forest():
    estimator = lightgbm.LGBMRegressor(boosting_type="rf", n_estimators=2,
                                       random_state=1, max_depth=1,
                                       subsample=0.7, subsample_freq=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.954000000000001),
                        ast.CompOpType.GT),
                    ast.NumVal(37.24347877367631),
                    ast.NumVal(19.936999995530854)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.971500000000001),
                    ast.CompOpType.GT),
                ast.NumVal(38.48600037864964),
                ast.NumVal(20.183783757300255)),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert utils.cmp_exprs(actual, expected)


def test_simple_sigmoid_output_transform():
    estimator = lightgbm.LGBMRegressor(n_estimators=2, random_state=1,
                                       max_depth=1, objective="cross_entropy")
    utils.get_bounded_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(
            ast.NumVal(1),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.BinNumExpr(
                        ast.BinNumExpr(
                            ast.NumVal(0),
                            ast.IfExpr(
                                ast.CompExpr(
                                    ast.FeatureRef(12),
                                    ast.NumVal(19.23),
                                    ast.CompOpType.GT),
                                ast.NumVal(4.0026305187),
                                ast.NumVal(4.0880438137)),
                            ast.BinNumOpType.ADD),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(12),
                                ast.NumVal(14.895),
                                ast.CompOpType.GT),
                            ast.NumVal(-0.0412703078),
                            ast.NumVal(0.0208393767)),
                        ast.BinNumOpType.ADD),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_log1p_exp_output_transform():
    estimator = lightgbm.LGBMRegressor(n_estimators=2, random_state=1,
                                       max_depth=1,
                                       objective="cross_entropy_lambda")
    utils.get_bounded_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.Log1pExpr(
        ast.ExpExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(12),
                            ast.NumVal(19.23),
                            ast.CompOpType.GT),
                        ast.NumVal(0.6623502468),
                        ast.NumVal(0.6683497987)),
                    ast.BinNumOpType.ADD),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(15.145),
                        ast.CompOpType.GT),
                    ast.NumVal(0.1405181490),
                    ast.NumVal(0.1453602134)),
                ast.BinNumOpType.ADD)))

    assert utils.cmp_exprs(actual, expected)


def test_maybe_sqr_output_transform():
    estimator = lightgbm.LGBMRegressor(n_estimators=2, random_state=1,
                                       max_depth=1, reg_sqrt=True,
                                       objective="regression_l1")
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    raw_output = ast.IdExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(9.905),
                        ast.CompOpType.GT),
                    ast.NumVal(4.5658116817),
                    ast.NumVal(4.6620790482)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.77),
                    ast.CompOpType.GT),
                ast.NumVal(-0.0340889740),
                ast.NumVal(0.0543687153)),
            ast.BinNumOpType.ADD),
        to_reuse=True)
    expected = ast.BinNumExpr(
        ast.AbsExpr(raw_output),
        raw_output,
        ast.BinNumOpType.MUL)

    assert utils.cmp_exprs(actual, expected)


def test_exp_output_transform():
    estimator = lightgbm.LGBMRegressor(n_estimators=2, random_state=1,
                                       max_depth=1, objective="poisson")
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.ExpExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.918),
                        ast.CompOpType.GT),
                    ast.NumVal(3.1480683932),
                    ast.NumVal(3.1101554907)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.63),
                    ast.CompOpType.GT),
                ast.NumVal(-0.0111969636),
                ast.NumVal(0.0160298303)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_bin_class_sigmoid_output_transform():
    estimator = lightgbm.LGBMClassifier(n_estimators=1, random_state=1,
                                        max_depth=1, sigmoid=0.5)
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
                    ast.BinNumExpr(
                        ast.NumVal(0.5),
                        ast.BinNumExpr(
                            ast.NumVal(0),
                            ast.IfExpr(
                                ast.CompExpr(
                                    ast.FeatureRef(23),
                                    ast.NumVal(868.2),
                                    ast.CompOpType.GT),
                                ast.NumVal(0.5197386243),
                                ast.NumVal(1.2474356828)),
                            ast.BinNumOpType.ADD),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV,
        to_reuse=True)
    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class_sigmoid_output_transform():
    estimator = lightgbm.LGBMClassifier(n_estimators=1, random_state=1,
                                        max_depth=1, sigmoid=0.5,
                                        objective="ovr")
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(
            ast.NumVal(1),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.BinNumExpr(
                        ast.NumVal(0.5),
                        ast.BinNumExpr(
                            ast.NumVal(0),
                            ast.NumVal(-1.3862943611),
                            ast.BinNumOpType.ADD),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV)
    expected = ast.VectorVal([sigmoid] * 3)
    assert utils.cmp_exprs(actual, expected)
