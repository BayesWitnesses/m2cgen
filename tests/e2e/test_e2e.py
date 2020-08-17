from sys import setrecursionlimit

import lightgbm as lgb
import lightning.classification as light_clf
import lightning.regression as light_reg
import numpy as np
import pytest
import statsmodels.api as sm
import xgboost as xgb
from sklearn import ensemble, linear_model, svm, tree
from statsmodels.regression.process_regression import ProcessMLE

from tests import utils
from tests.e2e import executors

RECURSION_LIMIT = 5500

# pytest marks
PYTHON = pytest.mark.python
JAVA = pytest.mark.java
C = pytest.mark.c_lang
GO = pytest.mark.go_lang
JAVASCRIPT = pytest.mark.javascript
VISUAL_BASIC = pytest.mark.visual_basic
C_SHARP = pytest.mark.c_sharp
POWERSHELL = pytest.mark.powershell
R = pytest.mark.r_lang
PHP = pytest.mark.php
DART = pytest.mark.dart
HASKELL = pytest.mark.haskell
RUBY = pytest.mark.ruby
F_SHARP = pytest.mark.f_sharp
RUST = pytest.mark.rust
ELIXIR = pytest.mark.elixir
REGRESSION = pytest.mark.regr
REGRESSION_WITH_MISSING_VALUES = pytest.mark.regr_missing_val
CLASSIFICATION_WITH_MISSING_VALUES = pytest.mark.clf_missing_val
CLASSIFICATION = pytest.mark.clf


# Set of helper functions to make parametrization less verbose.
def regression(model, test_fraction=0.02):
    return (
        model,
        utils.get_regression_model_trainer(test_fraction),
        REGRESSION,
    )


def classification(model, test_fraction=0.02):
    return (
        model,
        utils.get_classification_model_trainer(test_fraction),
        CLASSIFICATION,
    )


def classification_binary(model, test_fraction=0.02):
    return (
        model,
        utils.get_binary_classification_model_trainer(test_fraction),
        CLASSIFICATION,
    )


def regression_random(model, test_fraction=0.02):
    return (
        model,
        utils.get_regression_random_data_model_trainer(test_fraction),
        REGRESSION,
    )


def classification_random(model, test_fraction=0.02):
    return (
        model,
        utils.get_classification_random_data_model_trainer(test_fraction),
        CLASSIFICATION,
    )


def classification_binary_random(model, test_fraction=0.02):
    return (
        model,
        utils.get_classification_binary_random_data_model_trainer(test_fraction),
        CLASSIFICATION,
    )


def regression_bounded(model, test_fraction=0.02):
    return (
        model,
        utils.get_bounded_regression_model_trainer(test_fraction),
        REGRESSION,
    )


def regression_w_missing_values(model, test_fraction=0.02):
    return (
        model,
        utils.get_regression_w_missing_values_model_trainer(test_fraction),
        REGRESSION_WITH_MISSING_VALUES,
    )


def classification_random_w_missing_values(model, test_fraction=0.02):
    return (
        model,
        utils.get_classification_random_w_missing_values_model_trainer(test_fraction),
        CLASSIFICATION_WITH_MISSING_VALUES,
    )


def classification_binary_random_w_missing_values(model, test_fraction=0.02):
    return (
        model,
        utils.get_classification_binary_random_w_missing_values_model_trainer(test_fraction),
        CLASSIFICATION_WITH_MISSING_VALUES,
    )


# Absolute tolerance. Used in np.isclose to compare 2 values.
# We compare 6 decimal digits.
ATOL = 1.e-6

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)
XGBOOST_PARAMS = dict(base_score=0.6, n_estimators=10, random_state=RANDOM_SEED)
XGBOOST_HIST_PARAMS = dict(base_score=0.6, n_estimators=10, tree_method="hist", random_state=RANDOM_SEED)
XGBOOST_PARAMS_LINEAR = dict(base_score=0.6, n_estimators=10, feature_selector="shuffle",
                             booster="gblinear", random_state=RANDOM_SEED)
XGBOOST_PARAMS_RF = dict(base_score=0.6, n_estimators=10, random_state=RANDOM_SEED)
XGBOOST_PARAMS_BOOSTED_RF = dict(base_score=0.6, n_estimators=5, num_parallel_tree=3, subsample=0.8,
                                 colsample_bynode=0.8, learning_rate=1.0, random_state=RANDOM_SEED)
XGBOOST_PARAMS_LARGE = dict(base_score=0.6, n_estimators=100, max_depth=12, random_state=RANDOM_SEED)
XGBOOST_PARAMS_HUGE = dict(base_score=0.6, n_estimators=500, max_depth=12, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_DART = dict(n_estimators=10, boosting_type='dart', max_drop=30, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_GOSS = dict(n_estimators=10, boosting_type='goss',
                            top_rate=0.3, other_rate=0.2, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_RF = dict(n_estimators=10, boosting_type='rf',
                          subsample=0.7, subsample_freq=1, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_EXTRA_TREES = dict(n_estimators=10, extra_trees=True, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_LARGE = dict(n_estimators=100, num_leaves=100, max_depth=64, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_HUGE = dict(n_estimators=500, num_leaves=100, max_depth=64, random_state=RANDOM_SEED)
SVC_PARAMS = dict(random_state=RANDOM_SEED, decision_function_shape="ovo")
STATSMODELS_LINEAR_REGULARIZED_PARAMS = dict(method="elastic_net", alpha=7, L1_wt=0.2)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
        (executors.CExecutor, C),
        (executors.GoExecutor, GO),
        (executors.JavascriptExecutor, JAVASCRIPT),
        (executors.VisualBasicExecutor, VISUAL_BASIC),
        (executors.CSharpExecutor, C_SHARP),
        (executors.PowershellExecutor, POWERSHELL),
        (executors.RExecutor, R),
        (executors.PhpExecutor, PHP),
        (executors.DartExecutor, DART),
        (executors.HaskellExecutor, HASKELL),
        (executors.RubyExecutor, RUBY),
        (executors.FSharpExecutor, F_SHARP),
        (executors.RustExecutor, RUST),
        (executors.ElixirExecutor, ELIXIR),
    ],

    # These models will be tested against each language specified in the previous list.
    [
        # LightGBM
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS)),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS)),

        # LightGBM (DART)
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_DART)),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_DART)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_DART)),

        # LightGBM (GOSS)
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_GOSS)),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_GOSS)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_GOSS)),

        # LightGBM (RF)
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_RF)),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_RF)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_RF)),

        # LightGBM (Extra Trees)
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_EXTRA_TREES)),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_EXTRA_TREES)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_EXTRA_TREES)),

        # LightGBM (Large Trees)
        regression_random(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_LARGE)),
        classification_random(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_LARGE)),
        classification_binary_random(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_LARGE)),

        # LightGBM (Missing values during train)
        regression_w_missing_values(lgb.LGBMRegressor(**LIGHTGBM_PARAMS)),
        classification_random_w_missing_values(lgb.LGBMClassifier(**LIGHTGBM_PARAMS)),
        classification_binary_random_w_missing_values(lgb.LGBMClassifier(**LIGHTGBM_PARAMS)),

        # LightGBM (Huge Trees)
        regression_random(lgb.LGBMRegressor(**LIGHTGBM_PARAMS_HUGE)),
        classification_random(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_HUGE)),
        classification_binary_random(lgb.LGBMClassifier(**LIGHTGBM_PARAMS_HUGE)),

        # LightGBM (Different Objectives)
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="mse", reg_sqrt=True)),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="mae")),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="huber", alpha=0.5)),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="fair", fair_c=0.5)),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="poisson", poisson_max_delta_step=0.2)),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="quantile", alpha=0.2)),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="mape")),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="gamma")),
        regression(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="tweedie", tweedie_variance_power=1.7)),
        regression(lgb.LGBMRegressor(
            **LIGHTGBM_PARAMS,
            objective=lambda _, __: (
                np.ones(len(utils.get_regression_model_trainer().y_train)),
                np.ones(len(utils.get_regression_model_trainer().y_train))))),
        regression_bounded(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="xentropy")),
        regression_bounded(lgb.LGBMRegressor(**LIGHTGBM_PARAMS, objective="xentlambda")),
        classification(lgb.LGBMClassifier(**LIGHTGBM_PARAMS, objective="ovr", sigmoid=0.5)),
        classification_binary(lgb.LGBMClassifier(**LIGHTGBM_PARAMS, sigmoid=1.5)),

        # XGBoost
        regression(xgb.XGBRegressor(**XGBOOST_PARAMS)),
        classification(xgb.XGBClassifier(**XGBOOST_PARAMS)),
        classification_binary(xgb.XGBClassifier(**XGBOOST_PARAMS)),

        # XGBoost (tree method "hist")
        regression(xgb.XGBRegressor(**XGBOOST_HIST_PARAMS), test_fraction=0.2),
        classification(xgb.XGBClassifier(**XGBOOST_HIST_PARAMS), test_fraction=0.2),
        classification_binary(xgb.XGBClassifier(**XGBOOST_HIST_PARAMS), test_fraction=0.2),

        # XGBoost (LINEAR)
        regression(xgb.XGBRegressor(**XGBOOST_PARAMS_LINEAR)),
        classification(xgb.XGBClassifier(**XGBOOST_PARAMS_LINEAR)),
        classification_binary(xgb.XGBClassifier(**XGBOOST_PARAMS_LINEAR)),

        # XGBoost (RF)
        regression(xgb.XGBRFRegressor(**XGBOOST_PARAMS_RF)),
        classification(xgb.XGBRFClassifier(**XGBOOST_PARAMS_RF)),
        classification_binary(xgb.XGBRFClassifier(**XGBOOST_PARAMS_RF)),

        # XGBoost (Boosted Random Forests)
        regression(xgb.XGBRegressor(**XGBOOST_PARAMS_BOOSTED_RF)),
        classification(xgb.XGBClassifier(**XGBOOST_PARAMS_BOOSTED_RF)),
        classification_binary(xgb.XGBClassifier(**XGBOOST_PARAMS_BOOSTED_RF)),

        # XGBoost (Large Trees)
        regression_random(xgb.XGBRegressor(**XGBOOST_PARAMS_LARGE)),
        classification_random(xgb.XGBClassifier(**XGBOOST_PARAMS_LARGE)),
        classification_binary_random(xgb.XGBClassifier(**XGBOOST_PARAMS_LARGE)),

        # XGBoost (Huge Trees)
        regression_random(xgb.XGBRegressor(**XGBOOST_PARAMS_HUGE)),
        classification_random(xgb.XGBClassifier(**XGBOOST_PARAMS_HUGE)),
        classification_binary_random(xgb.XGBClassifier(**XGBOOST_PARAMS_HUGE)),

        # Sklearn Linear SVM
        regression(svm.LinearSVR(random_state=RANDOM_SEED)),
        classification(svm.LinearSVC(random_state=RANDOM_SEED)),
        classification_binary(svm.LinearSVC(random_state=RANDOM_SEED)),

        # Lightning Linear SVM
        regression(light_reg.LinearSVR(random_state=RANDOM_SEED)),
        classification(light_clf.LinearSVC(criterion="accuracy", random_state=RANDOM_SEED)),
        classification(light_clf.LinearSVC(criterion="auc", random_state=RANDOM_SEED)),
        classification_binary(light_clf.LinearSVC(criterion="accuracy", random_state=RANDOM_SEED)),
        classification_binary(light_clf.LinearSVC(criterion="auc", random_state=RANDOM_SEED)),

        # Sklearn SVM
        regression(svm.NuSVR(kernel="rbf")),
        regression(svm.OneClassSVM(kernel="rbf")),
        regression(svm.SVR(kernel="rbf")),

        classification(svm.NuSVC(kernel="rbf", **SVC_PARAMS)),
        classification(svm.OneClassSVM(kernel="rbf")),
        classification(svm.SVC(kernel="rbf", **SVC_PARAMS)),

        classification_binary(svm.NuSVC(kernel="rbf", **SVC_PARAMS)),
        classification_binary(svm.OneClassSVM(kernel="rbf")),
        classification_binary(svm.SVC(kernel="linear", **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="poly", C=1.5, degree=2, gamma=0.1, coef0=2.0, **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="rbf", **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="sigmoid", **SVC_PARAMS)),

        # Lightning SVM
        classification(light_clf.KernelSVC(kernel="rbf", random_state=RANDOM_SEED)),

        classification_binary(light_clf.KernelSVC(kernel="rbf", random_state=RANDOM_SEED)),
        classification_binary(light_clf.KernelSVC(kernel="linear", random_state=RANDOM_SEED)),
        classification_binary(light_clf.KernelSVC(
            kernel="poly", alpha=1.5, solver="cg", degree=2, gamma=0.1, coef0=2.0, random_state=RANDOM_SEED)),
        classification_binary(light_clf.KernelSVC(kernel="sigmoid", random_state=RANDOM_SEED)),
        classification_binary(light_clf.KernelSVC(kernel="cosine", random_state=RANDOM_SEED)),

        # Sklearn Linear Regression
        regression(linear_model.ARDRegression()),
        regression(linear_model.BayesianRidge()),
        regression(linear_model.ElasticNet(random_state=RANDOM_SEED)),
        regression(linear_model.ElasticNetCV(random_state=RANDOM_SEED)),
        regression(linear_model.GammaRegressor()),
        regression(linear_model.HuberRegressor()),
        regression(linear_model.Lars()),
        regression(linear_model.LarsCV()),
        regression(linear_model.Lasso(random_state=RANDOM_SEED)),
        regression(linear_model.LassoCV(random_state=RANDOM_SEED)),
        regression(linear_model.LassoLars()),
        regression(linear_model.LassoLarsCV()),
        regression(linear_model.LassoLarsIC()),
        regression(linear_model.LinearRegression()),
        regression(linear_model.OrthogonalMatchingPursuit()),
        regression(linear_model.OrthogonalMatchingPursuitCV()),
        regression(linear_model.PassiveAggressiveRegressor(random_state=RANDOM_SEED)),
        regression(linear_model.PoissonRegressor()),
        regression(linear_model.RANSACRegressor(
            base_estimator=tree.ExtraTreeRegressor(**TREE_PARAMS), random_state=RANDOM_SEED)),
        regression(linear_model.Ridge(random_state=RANDOM_SEED)),
        regression(linear_model.RidgeCV()),
        regression(linear_model.SGDRegressor(random_state=RANDOM_SEED)),
        regression(linear_model.TheilSenRegressor(random_state=RANDOM_SEED)),
        regression(linear_model.TweedieRegressor(power=0.0)),
        regression(linear_model.TweedieRegressor(power=1.0)),
        regression(linear_model.TweedieRegressor(power=1.5)),
        regression(linear_model.TweedieRegressor(power=2.0)),
        regression(linear_model.TweedieRegressor(power=3.0)),

        # Statsmodels Linear Regression
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(fit_constrained=dict(constraints=(np.eye(
                     utils.get_binary_classification_model_trainer()
                     .X_train.shape[-1])[0], [1]))))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(fit_regularized=STATSMODELS_LINEAR_REGULARIZED_PARAMS))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                family=sm.families.Binomial(
                    sm.families.links.cauchy())),
                 fit=dict(maxiter=2)))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                family=sm.families.Binomial(
                    sm.families.links.cloglog())),
                 fit=dict(maxiter=2)))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                family=sm.families.Binomial(
                    sm.families.links.logit())),
                 fit=dict(maxiter=2)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                fit_intercept=True, family=sm.families.Gaussian(
                    sm.families.links.identity()))))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                 fit_intercept=True, family=sm.families.Gaussian(
                     sm.families.links.inverse_power()))))),
        regression_bounded(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                 family=sm.families.InverseGaussian(
                     sm.families.links.inverse_squared()))))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                fit_intercept=True, family=sm.families.NegativeBinomial(
                    sm.families.links.nbinom())),
                 fit=dict(maxiter=2)))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                fit_intercept=True, family=sm.families.Poisson(
                    sm.families.links.log())),
                 fit=dict(maxiter=2)))),
        classification_binary(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                fit_intercept=True, family=sm.families.Poisson(
                    sm.families.links.sqrt())),
                 fit=dict(maxiter=2)))),
        regression_bounded(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                 family=sm.families.Tweedie(
                     sm.families.links.Power(-3)))))),
        regression_bounded(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLM,
            dict(init=dict(
                 fit_intercept=True, family=sm.families.Tweedie(
                     sm.families.links.Power(2)))))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLS,
            dict(init=dict(sigma=np.eye(
                len(utils.get_regression_model_trainer().y_train)) + 1)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLS,
            dict(init=dict(sigma=np.eye(
                len(utils.get_regression_model_trainer().y_train)) + 1),
                 fit_regularized=STATSMODELS_LINEAR_REGULARIZED_PARAMS))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLSAR,
            dict(init=dict(fit_intercept=True, rho=3)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLSAR,
            dict(iterative_fit=dict(maxiter=2)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.GLSAR,
            dict(fit_regularized=STATSMODELS_LINEAR_REGULARIZED_PARAMS))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.OLS,
            dict(init=dict(fit_intercept=True)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.OLS,
            dict(fit_regularized=STATSMODELS_LINEAR_REGULARIZED_PARAMS))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            ProcessMLE,
            dict(init=dict(exog_scale=np.ones(
                (len(utils.get_regression_model_trainer().y_train), 2)),
                           exog_smooth=np.ones(
                (len(utils.get_regression_model_trainer().y_train), 2)),
                           exog_noise=np.ones(
                (len(utils.get_regression_model_trainer().y_train), 2)),
                           time=np.kron(
                np.ones(
                    len(utils.get_regression_model_trainer().y_train) // 3),
                np.arange(3)),
                           groups=np.kron(
                np.arange(
                    len(utils.get_regression_model_trainer().y_train) // 3),
                np.ones(3))),
                 fit=dict(maxiter=2)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.QuantReg,
            dict(init=dict(fit_intercept=True)))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.WLS,
            dict(init=dict(fit_intercept=True, weights=np.arange(
                len(utils.get_regression_model_trainer().y_train)))))),
        regression(utils.StatsmodelsSklearnLikeWrapper(
            sm.WLS,
            dict(init=dict(fit_intercept=True, weights=np.arange(
                len(utils.get_regression_model_trainer().y_train))),
                 fit_regularized=STATSMODELS_LINEAR_REGULARIZED_PARAMS))),

        # Lightning Linear Regression
        regression(light_reg.AdaGradRegressor(random_state=RANDOM_SEED)),
        regression(light_reg.CDRegressor(random_state=RANDOM_SEED)),
        regression(light_reg.FistaRegressor()),
        regression(light_reg.SAGARegressor(random_state=RANDOM_SEED)),
        regression(light_reg.SAGRegressor(random_state=RANDOM_SEED)),
        regression(light_reg.SDCARegressor(random_state=RANDOM_SEED)),
        regression(light_reg.SGDRegressor(
            loss='epsilon_insensitive',  # default results in NANs in coefs_
            random_state=RANDOM_SEED)),

        # Sklearn Linear Classifiers
        classification(linear_model.LogisticRegression(random_state=RANDOM_SEED)),
        classification(linear_model.LogisticRegressionCV(random_state=RANDOM_SEED)),
        classification(linear_model.PassiveAggressiveClassifier(random_state=RANDOM_SEED)),
        classification(linear_model.Perceptron(random_state=RANDOM_SEED)),
        classification(linear_model.RidgeClassifier(random_state=RANDOM_SEED)),
        classification(linear_model.RidgeClassifierCV()),
        classification(linear_model.SGDClassifier(random_state=RANDOM_SEED)),

        classification_binary(linear_model.LogisticRegression(random_state=RANDOM_SEED)),
        classification_binary(linear_model.LogisticRegressionCV(random_state=RANDOM_SEED)),
        classification_binary(linear_model.PassiveAggressiveClassifier(random_state=RANDOM_SEED)),
        classification_binary(linear_model.Perceptron(random_state=RANDOM_SEED)),
        classification_binary(linear_model.RidgeClassifier(random_state=RANDOM_SEED)),
        classification_binary(linear_model.RidgeClassifierCV()),
        classification_binary(linear_model.SGDClassifier(random_state=RANDOM_SEED)),

        # Lightning Linear Classifiers
        classification(light_clf.AdaGradClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.CDClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.CDClassifier(penalty="l1/l2", multiclass=True, random_state=RANDOM_SEED)),
        classification(light_clf.FistaClassifier()),
        classification(light_clf.FistaClassifier(multiclass=True)),
        classification(light_clf.SAGAClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.SAGClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.SDCAClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.SGDClassifier(random_state=RANDOM_SEED)),
        classification(light_clf.SGDClassifier(multiclass=True, random_state=RANDOM_SEED)),

        classification_binary(light_clf.AdaGradClassifier(random_state=RANDOM_SEED)),
        classification_binary(light_clf.CDClassifier(random_state=RANDOM_SEED)),
        classification_binary(light_clf.FistaClassifier()),
        classification_binary(light_clf.SAGAClassifier(random_state=RANDOM_SEED)),
        classification_binary(light_clf.SAGClassifier(random_state=RANDOM_SEED)),
        classification_binary(light_clf.SDCAClassifier(random_state=RANDOM_SEED)),
        classification_binary(light_clf.SGDClassifier(random_state=RANDOM_SEED)),

        # Decision trees
        regression(tree.DecisionTreeRegressor(**TREE_PARAMS)),
        regression(tree.ExtraTreeRegressor(**TREE_PARAMS)),

        classification(tree.DecisionTreeClassifier(**TREE_PARAMS)),
        classification(tree.ExtraTreeClassifier(**TREE_PARAMS)),

        classification_binary(tree.DecisionTreeClassifier(**TREE_PARAMS)),
        classification_binary(tree.ExtraTreeClassifier(**TREE_PARAMS)),


        # Random forest
        regression(ensemble.ExtraTreesRegressor(**FOREST_PARAMS)),
        regression(ensemble.RandomForestRegressor(**FOREST_PARAMS)),

        classification(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),
        classification(ensemble.RandomForestClassifier(**FOREST_PARAMS)),

        classification_binary(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),
        classification_binary(ensemble.RandomForestClassifier(**FOREST_PARAMS)),
    ],
    [
        (R, REGRESSION_WITH_MISSING_VALUES),
        (R, CLASSIFICATION_WITH_MISSING_VALUES),
        (ELIXIR, REGRESSION_WITH_MISSING_VALUES),
        (ELIXIR, CLASSIFICATION_WITH_MISSING_VALUES),
    ]

    # Following is the list of extra tests for languages/models which are not fully supported yet.

    # <empty>
)
def test_e2e(estimator, executor_cls, model_trainer, is_fast, global_tmp_dir):
    setrecursionlimit(RECURSION_LIMIT)

    X_test, y_pred_true, fitted_estimator = model_trainer(estimator)
    executor = executor_cls(fitted_estimator)

    idxs_to_test = [0] if is_fast else range(len(X_test))

    executor.prepare_global(global_tmp_dir=global_tmp_dir)
    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            y_pred_executed = np.array(y_pred_executed, dtype=y_pred_true.dtype, copy=False)
            print(f"expected={y_pred_true[idx]}, actual={y_pred_executed}")
            res = np.isclose(y_pred_true[idx], y_pred_executed, atol=ATOL)
            assert res if isinstance(res, bool) else res.all()
