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

    assembler = assemblers.StatsmodelsLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.0926871267),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0482139967),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0075524567),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.9965313383),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-3.0877925575),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.9546630146),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0073548271),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.9828206079),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1727389546),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0094218658),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.3931071261),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0149656744),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.4133835832),
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

    assembler = assemblers.StatsmodelsLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.1085910250),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0441988987),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.0174669054),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.8323210870),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-18.4837486980),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(3.8354955484),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0001409165),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-1.5040340047),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.3106174852),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0123066500),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.9736183985),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0094039648),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.5203427347),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(37.1353468527),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_statsmodels_unknown_constant_position():
    estimator = utils.StatsmodelsSklearnLikeWrapper(
        sm.GLS,
        dict(init=dict(hasconst=True)))
    _, __, estimator = utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.StatsmodelsLinearModelAssembler(estimator)
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
            ast.NumVal(-0.0932673973),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0480819091),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0063734439),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(2.7510656855),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(-3.0836268637),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(5.9605290000),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0077880716),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.9685365627),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1688777882),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0092446419),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(-0.3924930042),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.01506511708295605),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.4177000096),
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(-1.0),
        ast.BinNumExpr(
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
                                ast.NumVal(-1.1079583217),
                                ast.BinNumOpType.MUL),
                            ast.BinNumOpType.ADD),
                        ast.BinNumOpType.SUB)),
                ast.BinNumOpType.SUB),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.DIV)

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

    assembler = assemblers.StatsmodelsGLMModelAssembler(estimator)
    assembler.assemble()


def test_lightning_regression():
    estimator = AdaGradRegressor(random_state=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.0961163452),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.1574398180),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0251799219),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.1975142192),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.1189621635),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(1.2977018274),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.1192977978),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(0.0331955333),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.1433964513),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.0014943531),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.3116036672),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0258421936),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.7386996349),
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
            ast.NumVal(0.1617602138),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0931034793),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.6279180888),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.1856722189),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.0009999878),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(-0.0028974470),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.0059948515),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.0024173728),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0020429247),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.0009604400),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0010933747),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0078588761),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.0069150246),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(13),
            ast.NumVal(-0.2583249885),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(14),
            ast.NumVal(0.0000097479),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(15),
            ast.NumVal(-0.0007210600),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(16),
            ast.NumVal(-0.0011295195),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(17),
            ast.NumVal(-0.0001966115),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(18),
            ast.NumVal(0.0001358314),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(19),
            ast.NumVal(-0.0000378118),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(20),
            ast.NumVal(0.1555921773),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(21),
            ast.NumVal(0.0621307817),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(22),
            ast.NumVal(0.5138354949),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(23),
            ast.NumVal(-0.2418579612),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(24),
            ast.NumVal(0.0007953821),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(25),
            ast.NumVal(-0.0110760214),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(26),
            ast.NumVal(-0.0162178044),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(27),
            ast.NumVal(-0.0040277699),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(28),
            ast.NumVal(0.0015067033),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(29),
            ast.NumVal(0.0001536614),
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
                            ast.NumVal(0.0935146297),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(0.3213921354),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(-0.4855914264),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.2214295302),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1103262586),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.1662457692),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.0379823341),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.0128634938),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1685751402),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.2045901693),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.2932121798),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(0.2138148665),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)
