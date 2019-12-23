import sys
import lightgbm
import pytest
import numpy as np
import xgboost
from sklearn import linear_model, svm
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RECURSION_LIMIT = 5000


# pytest marks
PYTHON = pytest.mark.python
JAVA = pytest.mark.java
C = pytest.mark.c
GO = pytest.mark.go
JAVASCRIPT = pytest.mark.javascript
VISUAL_BASIC = pytest.mark.visual_basic
C_SHARP = pytest.mark.c_sharp
POWERSHELL = pytest.mark.powershell
REGRESSION = pytest.mark.regr
CLASSIFICATION = pytest.mark.clf


# Set of helper functions to make parametrization less verbose.
def regression(model):
    return (
        model,
        utils.train_model_regression,
        REGRESSION,
    )


def classification(model):
    return (
        model,
        utils.train_model_classification,
        CLASSIFICATION,
    )


def classification_binary(model):
    return (
        model,
        utils.train_model_classification_binary,
        CLASSIFICATION,
    )


def regression_random(model):
    return (
        model,
        utils.train_model_regression_random_data,
        REGRESSION,
    )


def classification_random(model):
    return (
        model,
        utils.train_model_classification_random_data,
        CLASSIFICATION,
    )


def classification_binary_random(model):
    return (
        model,
        utils.train_model_classification_binary_random_data,
        CLASSIFICATION,
    )


# Absolute tolerance. Used in np.isclose to compare 2 values.
# We compare 6 decimal digits.
ATOL = 1.e-6

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)
XGBOOST_PARAMS = dict(base_score=0.6, n_estimators=10,
                      random_state=RANDOM_SEED)
XGBOOST_PARAMS_LINEAR = dict(base_score=0.6, n_estimators=10,
                             feature_selector="shuffle", booster="gblinear",
                             random_state=RANDOM_SEED)
LIGHTGBM_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_DART = dict(n_estimators=10, boosting_type='dart',
                            max_drop=30, random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_GOSS = dict(n_estimators=10, boosting_type='goss',
                            top_rate=0.3, other_rate=0.2,
                            random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_RF = dict(n_estimators=10, boosting_type='rf',
                          subsample=0.7, subsample_freq=1,
                          random_state=RANDOM_SEED)
SVC_PARAMS = dict(random_state=RANDOM_SEED, decision_function_shape="ovo")

XGBOOST_PARAMS_LARGE = dict(base_score=0.6, n_estimators=100, max_depth=12,
                            random_state=RANDOM_SEED)
LIGHTGBM_PARAMS_LARGE = dict(n_estimators=100, num_leaves=100, max_depth=64,
                             random_state=RANDOM_SEED)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
        (executors.CExecutor, C),
        (executors.GoExecutor, GO),
        (executors.JavascriptExecutor, JAVASCRIPT),
        (executors.VisualBasicExecutor, VISUAL_BASIC),
        (executors.CSharpExecutor, C_SHARP),
        (executors.PowershellExecutor, POWERSHELL),
    ],

    # These models will be tested against each language specified in the
    # previous list.
    [
        # LightGBM
        regression(lightgbm.LGBMRegressor(**LIGHTGBM_PARAMS)),
        classification(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS)),
        classification_binary(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS)),

        # LightGBM (DART)
        regression(lightgbm.LGBMRegressor(**LIGHTGBM_PARAMS_DART)),
        classification(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_DART)),
        classification_binary(lightgbm.LGBMClassifier(
            **LIGHTGBM_PARAMS_DART)),

        # LightGBM (GOSS)
        regression(lightgbm.LGBMRegressor(**LIGHTGBM_PARAMS_GOSS)),
        classification(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_GOSS)),
        classification_binary(lightgbm.LGBMClassifier(
            **LIGHTGBM_PARAMS_GOSS)),

        # LightGBM (RF)
        regression(lightgbm.LGBMRegressor(**LIGHTGBM_PARAMS_RF)),
        classification(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_RF)),
        classification_binary(lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_RF)),

        # LightGBM (Large Trees)
        regression_random(
            lightgbm.LGBMRegressor(**LIGHTGBM_PARAMS_LARGE)),
        classification_random(
            lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_LARGE)),
        classification_binary_random(
            lightgbm.LGBMClassifier(**LIGHTGBM_PARAMS_LARGE)),

        # XGBoost
        regression(xgboost.XGBRegressor(**XGBOOST_PARAMS)),
        classification(xgboost.XGBClassifier(**XGBOOST_PARAMS)),
        classification_binary(xgboost.XGBClassifier(**XGBOOST_PARAMS)),

        # XGBoost (LINEAR)
        regression(xgboost.XGBRegressor(**XGBOOST_PARAMS_LINEAR)),
        classification(xgboost.XGBClassifier(**XGBOOST_PARAMS_LINEAR)),
        classification_binary(xgboost.XGBClassifier(**XGBOOST_PARAMS_LINEAR)),

        # XGBoost (Large Trees)
        regression_random(
            xgboost.XGBRegressor(**XGBOOST_PARAMS_LARGE)),
        classification_random(
            xgboost.XGBClassifier(**XGBOOST_PARAMS_LARGE)),
        classification_binary_random(
            xgboost.XGBClassifier(**XGBOOST_PARAMS_LARGE)),

        # Linear SVM
        regression(svm.LinearSVR(random_state=RANDOM_SEED)),
        classification(svm.LinearSVC(random_state=RANDOM_SEED)),
        classification_binary(svm.LinearSVC(random_state=RANDOM_SEED)),

        # SVM
        regression(svm.SVR(kernel="rbf")),
        regression(svm.NuSVR(kernel="rbf")),
        classification_binary(svm.SVC(kernel="rbf", **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="linear", **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="poly", degree=2, **SVC_PARAMS)),
        classification_binary(svm.SVC(kernel="sigmoid", **SVC_PARAMS)),
        classification_binary(svm.NuSVC(kernel="rbf", **SVC_PARAMS)),
        classification(svm.SVC(kernel="rbf", **SVC_PARAMS)),
        classification(svm.NuSVC(kernel="rbf", **SVC_PARAMS)),

        # Linear Regression
        regression(linear_model.LinearRegression()),
        regression(linear_model.HuberRegressor()),
        regression(linear_model.ElasticNet(random_state=RANDOM_SEED)),
        regression(linear_model.ElasticNetCV(random_state=RANDOM_SEED)),
        regression(linear_model.TheilSenRegressor(random_state=RANDOM_SEED)),
        regression(linear_model.Lars()),
        regression(linear_model.LarsCV()),
        regression(linear_model.Lasso(random_state=RANDOM_SEED)),
        regression(linear_model.LassoCV(random_state=RANDOM_SEED)),
        regression(linear_model.LassoLars()),
        regression(linear_model.LassoLarsCV()),
        regression(linear_model.LassoLarsIC()),
        regression(linear_model.OrthogonalMatchingPursuit()),
        regression(linear_model.OrthogonalMatchingPursuitCV()),
        regression(linear_model.Ridge(random_state=RANDOM_SEED)),
        regression(linear_model.RidgeCV()),
        regression(linear_model.BayesianRidge()),
        regression(linear_model.ARDRegression()),
        regression(linear_model.SGDRegressor(random_state=RANDOM_SEED)),
        regression(linear_model.PassiveAggressiveRegressor(
            random_state=RANDOM_SEED)),

        # Logistic Regression
        classification(linear_model.LogisticRegression(
            random_state=RANDOM_SEED)),
        classification(linear_model.LogisticRegressionCV(
            random_state=RANDOM_SEED)),
        classification(linear_model.RidgeClassifier(random_state=RANDOM_SEED)),
        classification(linear_model.RidgeClassifierCV()),
        classification(linear_model.SGDClassifier(random_state=RANDOM_SEED)),

        classification_binary(linear_model.LogisticRegression(
            random_state=RANDOM_SEED)),
        classification_binary(linear_model.LogisticRegressionCV(
            random_state=RANDOM_SEED)),
        classification_binary(linear_model.RidgeClassifier(
            random_state=RANDOM_SEED)),
        classification_binary(linear_model.RidgeClassifierCV()),
        classification_binary(linear_model.SGDClassifier(
            random_state=RANDOM_SEED)),

        # Decision trees
        regression(tree.DecisionTreeRegressor(**TREE_PARAMS)),
        regression(tree.ExtraTreeRegressor(**TREE_PARAMS)),

        classification(tree.DecisionTreeClassifier(**TREE_PARAMS)),
        classification(tree.ExtraTreeClassifier(**TREE_PARAMS)),

        classification_binary(tree.DecisionTreeClassifier(**TREE_PARAMS)),
        classification_binary(tree.ExtraTreeClassifier(**TREE_PARAMS)),


        # Random forest
        regression(ensemble.RandomForestRegressor(**FOREST_PARAMS)),
        regression(ensemble.ExtraTreesRegressor(**FOREST_PARAMS)),

        classification(ensemble.RandomForestClassifier(**FOREST_PARAMS)),
        classification(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),

        classification_binary(
            ensemble.RandomForestClassifier(**FOREST_PARAMS)),
        classification_binary(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),
    ],

    # Following is the list of extra tests for languages/models which are
    # not fully supported yet.

    # <empty>
)
def test_e2e(estimator, executor_cls, model_trainer,
             is_fast, global_tmp_dir):
    sys.setrecursionlimit(RECURSION_LIMIT)

    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    idxs_to_test = [0] if is_fast else range(len(X_test))

    executor.prepare_global(global_tmp_dir=global_tmp_dir)
    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed, atol=ATOL)
            assert res if isinstance(res, bool) else res.all()
