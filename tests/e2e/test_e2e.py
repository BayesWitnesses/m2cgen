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


# Absolute tolerance. Used in np.isclose to compare 2 values.
# We compare 6 decimal digits.
ATOL = 1.e-6

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)
XGBOOST_PARAMS = dict(base_score=0.6, n_estimators=10,
                      random_state=RANDOM_SEED)
LIGHT_GBM_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
        (executors.CExecutor, C),
        (executors.GoExecutor, GO),
    ],

    # These models will be tested against each language specified in the
    # previous list.
    [
        # LightGBM
        regression(lightgbm.LGBMRegressor(**LIGHT_GBM_PARAMS)),
        classification(lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS)),
        classification_binary(lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS)),

        # XGBoost
        regression(xgboost.XGBRegressor(**XGBOOST_PARAMS)),
        classification(xgboost.XGBClassifier(**XGBOOST_PARAMS)),
        classification_binary(xgboost.XGBClassifier(**XGBOOST_PARAMS)),

        # Linear SVM
        regression(svm.LinearSVR(random_state=RANDOM_SEED)),
        classification(svm.LinearSVC(random_state=RANDOM_SEED)),
        classification_binary(svm.LinearSVC(random_state=RANDOM_SEED)),

        # SVM
        regression(svm.SVR(kernel='rbf')),
        classification_binary(svm.SVC(kernel='rbf', random_state=RANDOM_SEED)),
        classification_binary(svm.SVC(kernel='linear',
                                      random_state=RANDOM_SEED)),
        classification_binary(svm.SVC(kernel='poly', degree=2,
                                      random_state=RANDOM_SEED)),
        classification_binary(svm.SVC(kernel='sigmoid',
                                      random_state=RANDOM_SEED)),

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
def test_e2e(estimator, executor_cls, model_trainer, is_fast):
    sys.setrecursionlimit(RECURSION_LIMIT)

    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    idxs_to_test = [0] if is_fast else range(len(X_test))

    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed, atol=ATOL)
            assert res if isinstance(res, bool) else res.all()
