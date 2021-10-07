import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.regression.process_regression import ProcessMLE

from m2cgen import assemblers, ast

from tests import utils


def test_wo_const():
    estimator = utils.StatsmodelsSklearnLikeWrapper(sm.GLS, {})
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.09519078450227643),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.048952926782237956),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.007485539189808044),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.7302631809978273),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-2.5078200782168034),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.891794660307579),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.008663096157185936),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.9742684875268565),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1591703441858682),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.009351831548409096),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.36395034626096245),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.014529018124980565),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.437443877026267),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_w_const():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLS,
        dict(init=dict(fit_intercept=True)))
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.1086131135490779),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.046461486329934965),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.027432259970185422),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.6160671309537693),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-17.51793656329748),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(3.7674418196771957),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-2.1581753172923886e-05),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-1.4711768622633619),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.29567671400629103),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.012233831527258853),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.9220356453705244),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.009038220462695548),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.5425830337142312),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(36.36708074657767),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_unknown_constant_position():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLS,
        dict(init=dict(hasconst=True)))
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    with pytest.raises(ValueError, match="Unknown constant position"):
        assemblers.StatsmodelsModelAssemblerSelector(estimator)


def test_unknown_model():

    class ValidGLS(sm.GLS):
        pass

    estimator = utils.StatsmodelsSklearnLikeWrapper(ValidGLS, {})
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    with pytest.raises(NotImplementedError, match="Model 'ValidGLS' is not supported"):
        assemblers.StatsmodelsModelAssemblerSelector(estimator)


def test_processmle():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        ProcessMLE,
        dict(init=dict(exog_scale=np.ones(
            (len(utils.get_regression_model_trainer().y_train), 2)),
                       exog_smooth=np.ones(
            (len(utils.get_regression_model_trainer().y_train), 2)),
                       exog_noise=np.ones(
            (len(utils.get_regression_model_trainer().y_train), 2)),
                       time=np.kron(
            np.ones(len(utils.get_regression_model_trainer().y_train) // 3),
            np.arange(3)),
                       groups=np.kron(
            np.arange(len(utils.get_regression_model_trainer().y_train) // 3),
            np.ones(3))),
             fit=dict(maxiter=1)))
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.ProcessMLEModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.0980302102110356),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.04863869398287732),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.009514054355147874),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.977113829322681),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-2.6048073854474705),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.887987153279099),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.008183580358672775),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.996428929917054),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1618353156581333),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.009213049690188308),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.3634816838591863),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.014700492832969888),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.4384298738156768),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_glm_logit_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Binomial(
                sm.families.links.logit())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.SigmoidExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(-0.8567815987),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_glm_power_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(3))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.PowExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(0.0020808009),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.NumVal(0.3333333333))

    assert utils.cmp_exprs(actual, expected)


def test_glm_negative_power_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(-3))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.PowExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.BinNumExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(71.0542398846),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.NumVal(0.3333333333)),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_glm_inverse_power_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(-1))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(3.0460921844),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_glm_inverse_squared_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(-2))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.SqrtExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.BinNumExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(15.1237331741),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD)),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_glm_sqr_power_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(2))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.SqrtExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(0.0154915480),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_glm_identity_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(
                sm.families.links.Power(1))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2], [3]], [0.1, 0.2, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(0.0),
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(0.0791304348),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_glm_sqrt_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Poisson(
                sm.families.links.sqrt())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.PowExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(0.2429239017),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.NumVal(2))

    assert utils.cmp_exprs(actual, expected)


def test_glm_log_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Poisson(
                sm.families.links.log())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(-1.0242053933),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_glm_cloglog_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Binomial(
                sm.families.links.cloglog())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.ExpExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.ExpExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.8914468745),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD)),
                ast.BinNumOpType.SUB)),
        ast.BinNumOpType.SUB)

    assert utils.cmp_exprs(actual, expected)


def test_glm_negativebinomial_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.NegativeBinomial(
                sm.families.links.nbinom())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(-1.0),
        ast.BinNumExpr(
            ast.NumVal(1.0),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-1.1079583217),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.SUB),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_glm_cauchy_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Binomial(
                sm.families.links.cauchy())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.BinNumExpr(
            ast.AtanExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        ast.FeatureRef(0),
                        ast.NumVal(-0.7279996905393095),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD)),
            ast.NumVal(3.141592653589793),
            ast.BinNumOpType.DIV),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_glm_unknown_link_func():

    class ValidPowerLink(sm.families.links.Power):
        pass

    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(ValidPowerLink(2))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)

    with pytest.raises(ValueError, match="Unsupported link function 'ValidPowerLink'"):
        assembler.assemble()
