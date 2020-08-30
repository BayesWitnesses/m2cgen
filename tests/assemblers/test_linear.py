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
            ast.NumVal(-0.0940752519),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0461122112),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0034800646),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.9669908485),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-2.1264724710),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.9738064897),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0062638276),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.9385894841),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1568975632),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0091548228),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.3949784315),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0135685532),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.4392385223),
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
            ast.NumVal(-0.1082106941),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0444969007),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.0189847585),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.7998640040),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-16.7498366967),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(3.9040863643),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0014333844),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-1.4436181595),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.2868165881),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0118539736),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.9449930750),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0083181952),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.5415938640),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(35.5746356887),
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
            ast.NumVal(-0.0915126856),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0455368812),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0092227692),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.8566616798),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-2.1208777964),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.9725253309),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0061566965),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.9414114075),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1522429507),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0092123938),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.3928508764),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0134405151),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.4364996490),
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
            ast.NumVal(-0.0610645819),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0856563713),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0562044566),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.2804204925),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.1359261760),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(1.6307305501),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0866147265),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.0726894150),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0435440193),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0077364839),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.2902775116),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0229879957),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.7614706871),
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
            ast.NumVal(0.1605265174),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.1045225083),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.6237391536),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.1680225811),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.0011013688),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(-0.0027528486),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0058878714),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.0023719811),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0019944105),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.0009924456),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0003994860),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0124697033),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.0123674096),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(13),
            ast.NumVal(-0.2844204905),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(14),
            ast.NumVal(0.0000273704),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(15),
            ast.NumVal(-0.0007498013),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(16),
            ast.NumVal(-0.0010784399),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(17),
            ast.NumVal(-0.0001848694),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(18),
            ast.NumVal(0.0000632254),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(19),
            ast.NumVal(-0.0000369618),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(20),
            ast.NumVal(0.1520223021),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(21),
            ast.NumVal(0.0925348635),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(22),
            ast.NumVal(0.4861047372),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(23),
            ast.NumVal(-0.2798670185),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(24),
            ast.NumVal(0.0009925506),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(25),
            ast.NumVal(-0.0103414976),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(26),
            ast.NumVal(-0.0155024577),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(27),
            ast.NumVal(-0.0038881538),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(28),
            ast.NumVal(0.0010126166),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(29),
            ast.NumVal(0.0002312558),
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
                            ast.NumVal(0.0895848274),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(0.3258329434),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(-0.4900856238),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.2214482506),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1074247041),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.1693225196),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.0357417324),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.0161614171),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1825063678),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.2185655665),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.3053017646),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(0.2175198459),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)
