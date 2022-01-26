import lightgbm as lgb
import numpy as np
import pytest

from m2cgen import ast
from m2cgen.assemblers import LightGBMModelAssembler

from tests import utils


def test_binary_classification():
    estimator = lgb.LGBMClassifier(n_estimators=2, random_state=1, max_depth=1)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.SigmoidExpr(
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
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = lgb.LGBMClassifier(n_estimators=1, random_state=1, max_depth=1)
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    num_expr = ast.NumVal(-1.0986122886681098)
    expected = ast.SoftmaxExpr([num_expr] * 3)

    assert utils.cmp_exprs(actual, expected)


def test_regression():
    estimator = lgb.LGBMRegressor(n_estimators=2, random_state=1, max_depth=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(8),
                ast.NumVal(1.0000000180025095e-35),
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
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_regression_random_forest():
    estimator = lgb.LGBMRegressor(boosting_type="rf", n_estimators=2, random_state=1,
                                  max_depth=1, subsample=0.7, subsample_freq=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.00780560282464346),
                    ast.CompOpType.GT),
                ast.NumVal(210.27118647591766),
                ast.NumVal(120.45454548930705)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(-0.007822672246629598),
                    ast.CompOpType.LTE),
                ast.NumVal(114.24161077349474),
                ast.NumVal(194.84868424576604)),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.5),
        ast.BinNumOpType.MUL)

    assert utils.cmp_exprs(actual, expected)


def test_regression_with_negative_values():
    estimator = lgb.LGBMRegressor(n_estimators=3, random_state=1, max_depth=1)
    utils.get_regression_w_missing_values_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
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
    estimator = lgb.LGBMRegressor(n_estimators=2, random_state=1, max_depth=1, objective="cross_entropy")
    utils.get_bounded_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SigmoidExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(-0.0028501970360456344),
                    ast.CompOpType.LTE),
                ast.NumVal(5.8325360677435345),
                ast.NumVal(5.891973988308211)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(-0.005612778088288765),
                    ast.CompOpType.LTE),
                ast.NumVal(-0.027170480653266372),
                ast.NumVal(0.026423953384869338)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_log1p_exp_output_transform():
    estimator = lgb.LGBMRegressor(n_estimators=2, random_state=1, max_depth=1, objective="cross_entropy_lambda")
    utils.get_bounded_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.Log1pExpr(
        ast.ExpExpr(
            ast.BinNumExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(8),
                        ast.NumVal(-0.0028501970360456344),
                        ast.CompOpType.LTE),
                    ast.NumVal(0.693713164308067),
                    ast.NumVal(0.694435273176687)),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(8),
                        ast.NumVal(-0.005612778088288765),
                        ast.CompOpType.LTE),
                    ast.NumVal(0.14830023030115363),
                    ast.NumVal(0.14902176200722345)),
                ast.BinNumOpType.ADD)))

    assert utils.cmp_exprs(actual, expected)


def test_maybe_sqr_output_transform():
    estimator = lgb.LGBMRegressor(n_estimators=2, random_state=1, max_depth=1, reg_sqrt=True, objective="regression_l1")
    utils.get_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    raw_output = ast.IdExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(1.0000000180025095e-35),
                    ast.CompOpType.GT),
                ast.NumVal(12.094032478332519),
                ast.NumVal(11.671793556213379)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(-0.00468258384360457),
                    ast.CompOpType.LTE),
                ast.NumVal(-0.18738342285156248),
                ast.NumVal(0.19059675216674812)),
            ast.BinNumOpType.ADD),
        to_reuse=True)

    expected = ast.BinNumExpr(
        ast.AbsExpr(raw_output),
        raw_output,
        ast.BinNumOpType.MUL)

    assert utils.cmp_exprs(actual, expected)


def test_exp_output_transform():
    estimator = lgb.LGBMRegressor(n_estimators=2, random_state=1, max_depth=1, objective="poisson")
    utils.get_regression_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.ExpExpr(
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(8),
                    ast.NumVal(1.0000000180025095e-35),
                    ast.CompOpType.GT),
                ast.NumVal(5.040167360736721),
                ast.NumVal(5.013324518244505)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.00780560282464346),
                    ast.CompOpType.GT),
                ast.NumVal(0.016475080997255653),
                ast.NumVal(-0.010346335106608635)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_unknown_output_transform():
    estimator = lgb.LGBMRanker(n_estimators=1, random_state=1)
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]), group=np.array([3]))

    assembler = LightGBMModelAssembler(estimator)

    with pytest.raises(ValueError, match="Unsupported objective function 'lambdarank'"):
        assembler.assemble()


def test_bin_class_sigmoid_output_transform():
    estimator = lgb.LGBMClassifier(n_estimators=1, random_state=1, max_depth=1, sigmoid=0.5)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.SigmoidExpr(
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
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class_sigmoid_output_transform():
    estimator = lgb.LGBMClassifier(n_estimators=1, random_state=1, max_depth=1, sigmoid=0.5, objective="ovr")
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = LightGBMModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.SigmoidExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            ast.NumVal(-1.3862943611),
            ast.BinNumOpType.MUL))

    expected = ast.VectorVal([sigmoid] * 3)

    assert utils.cmp_exprs(actual, expected)
