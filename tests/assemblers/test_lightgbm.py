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
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(23),
                                ast.NumVal(868.2000000000002),
                                ast.CompOpType.GT),
                            ast.NumVal(0.26400127816506497),
                            ast.NumVal(0.633133056485969)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(22),
                                ast.NumVal(105.95000000000002),
                                ast.CompOpType.GT),
                            ast.NumVal(-0.18744882409486507),
                            ast.NumVal(0.13458899352064668)),
                        ast.BinNumOpType.ADD),
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
        ast.NumVal(-1.0986122886681098),
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
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(5),
                ast.NumVal(6.837500000000001),
                ast.CompOpType.GT),
            ast.NumVal(23.961356387224317),
            ast.NumVal(22.32858336612959)),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(12),
                ast.NumVal(9.725000000000003),
                ast.CompOpType.GT),
            ast.NumVal(-0.5031712645462916),
            ast.NumVal(0.6885501354513913)),
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
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(5.200000000000001),
                    ast.CompOpType.GT),
                ast.NumVal(20.206688945020474),
                ast.NumVal(38.30000037757679)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.837500000000001),
                    ast.CompOpType.GT),
                ast.NumVal(36.40634951405711),
                ast.NumVal(19.57067132709245)),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert utils.cmp_exprs(actual, expected)


def test_regression_with_negative_values():
    estimator = lightgbm.LGBMRegressor(n_estimators=3, random_state=1,
                                       max_depth=1)
    utils.get_regression_w_missing_values_model_trainer()(estimator)

    assembler = assemblers.LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(0.0),
                    ast.CompOpType.GT),
                ast.NumVal(155.96889994777868),
                ast.NumVal(147.72971715548434)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.00780560282464346),
                    ast.CompOpType.GT),
                ast.NumVal(4.982244683562974),
                ast.NumVal(-2.978315963345233)),
            ast.BinNumOpType.ADD),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(8),
                ast.NumVal(-0.0010539205031971832),
                ast.CompOpType.LTE),
            ast.NumVal(-3.488666332734598),
            ast.NumVal(3.670539900363904)),
        ast.BinNumOpType.ADD)

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
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(12),
                                ast.NumVal(19.23),
                                ast.CompOpType.GT),
                            ast.NumVal(4.0050691250),
                            ast.NumVal(4.0914737728)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(12),
                                ast.NumVal(15.065),
                                ast.CompOpType.GT),
                            ast.NumVal(-0.0420531079),
                            ast.NumVal(0.0202891577)),
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
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(19.23),
                        ast.CompOpType.GT),
                    ast.NumVal(0.6623996001),
                    ast.NumVal(0.6684477608)),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(15.065),
                        ast.CompOpType.GT),
                    ast.NumVal(0.1405782705),
                    ast.NumVal(0.1453764991)),
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
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(11.655),
                    ast.CompOpType.GT),
                ast.NumVal(4.5671830654),
                ast.NumVal(4.6516575813)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.725),
                    ast.CompOpType.GT),
                ast.NumVal(-0.0348178434),
                ast.NumVal(0.0549301624)),
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
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.8375),
                    ast.CompOpType.GT),
                ast.NumVal(3.1481886430),
                ast.NumVal(3.1123367238)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.725),
                    ast.CompOpType.GT),
                ast.NumVal(-0.0113689739),
                ast.NumVal(0.0153551274)),
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
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(23),
                                ast.NumVal(868.2),
                                ast.CompOpType.GT),
                            ast.NumVal(0.5280025563),
                            ast.NumVal(1.2662661130)),
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
                        ast.NumVal(-1.3862943611),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV)

    expected = ast.VectorVal([sigmoid] * 3)

    assert utils.cmp_exprs(actual, expected)
