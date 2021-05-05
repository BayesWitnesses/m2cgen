import pytest
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.process_regression import ProcessMLE
from lightning.regression import AdaGradRegressor
from lightning.classification import AdaGradClassifier
from sklearn import linear_model

from m2cgen import assemblers, ast
from tests import utils


def test_single_feature():
    estimator = linear_model.LinearRegression()
    estimator.coef_ = np.array([1])
    estimator.intercept_ = np.array([3])

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(3),
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(1),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_two_features():
    estimator = linear_model.LinearRegression()
    estimator.coef_ = np.array([1, 2])
    estimator.intercept_ = np.array([3])

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(3),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(1),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(2),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = linear_model.LogisticRegression()
    estimator.coef_ = np.array([[1, 2], [3, 4], [5, 6]])
    estimator.intercept_ = np.array([7, 8, 9])

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.VectorVal([
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(7),
                ast.BinNumExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(1),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(1),
                ast.NumVal(2),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(8),
                ast.BinNumExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(3),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(1),
                ast.NumVal(4),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(9),
                ast.BinNumExpr(
                    ast.FeatureRef(0),
                    ast.NumVal(5),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(1),
                ast.NumVal(6),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)


def test_binary_class():
    estimator = linear_model.LogisticRegression()
    estimator.coef_ = np.array([[1, 2]])
    estimator.intercept_ = np.array([3])

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(3),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(1),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(2),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_statsmodels_wo_const():
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


def test_statsmodels_w_const():
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


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_statsmodels_unknown_constant_position():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLS,
        dict(init=dict(hasconst=True)))
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    assembler.assemble()


def test_statsmodels_processmle():
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


def test_statsmodels_glm_logit_link_func():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Binomial(
                sm.families.links.logit())),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(1.0),
        ast.BinNumExpr(
            ast.NumVal(1.0),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.8567815987),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV)

    assert utils.cmp_exprs(actual, expected)


def test_statsmodels_glm_power_link_func():
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


def test_statsmodels_glm_negative_power_link_func():
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


def test_statsmodels_glm_inverse_power_link_func():
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


def test_statsmodels_glm_inverse_squared_link_func():
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


def test_statsmodels_glm_sqr_power_link_func():
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


def test_statsmodels_glm_identity_link_func():
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


def test_statsmodels_glm_sqrt_link_func():
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


def test_statsmodels_glm_log_link_func():
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


def test_statsmodels_glm_cloglog_link_func():
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


def test_statsmodels_glm_negativebinomial_link_func():
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


def test_statsmodels_glm_cauchy_link_func():
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


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_statsmodels_glm_unknown_link_func():

    class ValidPowerLink(sm.families.links.Power):
        pass

    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLM,
        dict(init=dict(
            family=sm.families.Tweedie(ValidPowerLink(2))),
             fit=dict(maxiter=1)))
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.StatsmodelsModelAssemblerSelector(estimator)
    assembler.assemble()


def test_sklearn_glm_identity_link_func():
    estimator = linear_model.TweedieRegressor(
        power=0, link="identity", max_iter=10)
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.SklearnGLMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(0.12),
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(0.02),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_sklearn_glm_log_link_func():
    estimator = linear_model.TweedieRegressor(
        power=1, link="log", fit_intercept=False, max_iter=10)
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.SklearnGLMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.0),
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.NumVal(-0.4619711397),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_sklearn_glm_unknown_link_func():
    estimator = linear_model.TweedieRegressor(
        power=1, link="this_link_func_does_not_exist", max_iter=10)
    estimator = estimator.fit([[1], [2]], [0.1, 0.2])

    assembler = assemblers.SklearnGLMModelAssembler(estimator)
    assembler.assemble()


def test_lightning_regression():
    estimator = AdaGradRegressor(random_state=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.08558826944690746),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0803724696787377),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.03516743076774846),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.26469178947134087),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.15651985221012488),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(1.5186399078028587),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.10089874009193693),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.011426237067026246),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0861987777487293),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0057791506839322574),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.3357752757550913),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.020189965076849486),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.7390647599317609),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_lightning_binary_class():
    estimator = AdaGradClassifier(random_state=1)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(0.16218889967390476),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.10012761963766906),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.6289276652681673),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.17618420156072845),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.0010492096607182045),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(-0.0029135563693806913),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.005923882409142498),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.0023293599172479755),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0020808828960210517),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.0009846430705550103),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0010399810925427265),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.011203056917272093),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.007271351370867731),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(13),
            ast.NumVal(-0.26333437096804224),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(14),
            ast.NumVal(1.8533543368532444e-05),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(15),
            ast.NumVal(-0.0008266341686278445),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(16),
            ast.NumVal(-0.0011090316301215724),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(17),
            ast.NumVal(-0.0001910857095336291),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(18),
            ast.NumVal(0.00010735116208006556),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(19),
            ast.NumVal(-4.076097659514017e-05),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(20),
            ast.NumVal(0.15300712110146406),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(21),
            ast.NumVal(0.06316277258339074),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(22),
            ast.NumVal(0.495291178977687),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(23),
            ast.NumVal(-0.29589136204657845),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(24),
            ast.NumVal(0.000771932729567487),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(25),
            ast.NumVal(-0.011877978242492428),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(26),
            ast.NumVal(-0.01678004536869617),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(27),
            ast.NumVal(-0.004070431062579625),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(28),
            ast.NumVal(0.001158641497209262),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(29),
            ast.NumVal(0.00010737287732588742),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_lightning_multi_class():
    estimator = AdaGradClassifier(random_state=1)
    utils.get_classification_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.VectorVal([
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(0.09686334892116512),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(0.32572202133211947),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(-0.48444233646554424),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.219719145605816),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1089136473832088),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.16956003333433572),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.0365531256007199),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.01016100116780896),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.16690339219780817),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.19466284646233858),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.2953585236360389),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(0.21288203082531384),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)
