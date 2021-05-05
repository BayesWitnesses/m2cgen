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
                                ast.FeatureRef(20),
                                ast.NumVal(16.795),
                                ast.CompOpType.GT),
                            ast.NumVal(0.27502096830384837),
                            ast.NumVal(0.6391171126839048)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(27),
                                ast.NumVal(0.14205),
                                ast.CompOpType.GT),
                            ast.NumVal(-0.21340153096570616),
                            ast.NumVal(0.11583109256834748)),
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

    num_expr = ast.NumVal(-1.0986122886681098)
    expected = ast.SoftmaxExpr([num_expr] * 3)

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
                ast.FeatureRef(12),
                ast.NumVal(9.725),
                ast.CompOpType.GT),
            ast.NumVal(22.030283219508686),
            ast.NumVal(23.27840740210207)),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(5),
                ast.NumVal(6.8375),
                ast.CompOpType.GT),
            ast.NumVal(1.2777791671888081),
            ast.NumVal(-0.2686772850549309)),
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
                    ast.NumVal(9.605),
                    ast.CompOpType.GT),
                ast.NumVal(17.398543657369768),
                ast.NumVal(29.851408659650296)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.888),
                    ast.CompOpType.GT),
                ast.NumVal(37.2235298136268),
                ast.NumVal(19.948122884684025)),
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
                ast.NumVal(156.64462853604854),
                ast.NumVal(148.40956590509697)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.00780560282464346),
                    ast.CompOpType.GT),
                ast.NumVal(4.996373375352607),
                ast.NumVal(-3.1063596100284814)),
            ast.BinNumOpType.ADD),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(8),
                ast.NumVal(-0.0010539205031971832),
                ast.CompOpType.LTE),
            ast.NumVal(-3.5131100858883424),
            ast.NumVal(3.6285643795846214)),
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
                            ast.NumVal(4.002437528537838),
                            ast.NumVal(4.090096709787509)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(12),
                                ast.NumVal(14.895),
                                ast.CompOpType.GT),
                            ast.NumVal(-0.0417499606641773),
                            ast.NumVal(0.02069953712454655)),
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
                    ast.NumVal(0.6622623010380544),
                    ast.NumVal(0.6684065452877841)),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(15.145),
                        ast.CompOpType.GT),
                    ast.NumVal(0.1404975120475147),
                    ast.NumVal(0.14535916856709272)),
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
                    ast.NumVal(9.725),
                    ast.CompOpType.GT),
                ast.NumVal(4.569350528717041),
                ast.NumVal(4.663526439666748)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(11.655),
                    ast.CompOpType.GT),
                ast.NumVal(-0.04462450027465819),
                ast.NumVal(0.033305134773254384)),
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
                    ast.FeatureRef(12),
                    ast.NumVal(9.725),
                    ast.CompOpType.GT),
                ast.NumVal(3.1043985065105892),
                ast.NumVal(3.1318783133960197)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.8375),
                    ast.CompOpType.GT),
                ast.NumVal(0.028409619436010138),
                ast.NumVal(-0.0060740730485278754)),
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
                                ast.FeatureRef(20),
                                ast.NumVal(16.795),
                                ast.CompOpType.GT),
                            ast.NumVal(0.5500419366076967),
                            ast.NumVal(1.2782342253678096)),
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
