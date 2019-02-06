import pytest
import numpy as np
from sklearn import linear_model, svm
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


# pytest marks
PYTHON = pytest.mark.python
JAVA = pytest.mark.java
C = pytest.mark.c
REGRESSION = pytest.mark.regr
CLASSIFICATION = pytest.mark.clf


# Set of helper functions to make parametrization less verbose.
def regression(model, is_fast=False):
    return (
        model,
        utils.train_model_regression,
        REGRESSION,
        is_fast,
    )


def classification(model, is_fast=False):
    return (
        model,
        utils.train_model_classification,
        CLASSIFICATION,
        is_fast,
    )


def classification_binary(model, is_fast=False):
    return (
        model,
        utils.train_model_classification_binary,
        CLASSIFICATION,
        is_fast,
    )


# Absolute tolerance. Used in np.isclose to compare 2 values.
# We compare 6 decimal digits.
ATOL = 1.e-6

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
        (executors.CExecutor, C),
    ],

    # These models will be tested against each language specified in the
    # previous list.
    [
        # SVM
        # regression(svm.LinearSVR(random_state=RANDOM_SEED)),
        classification(svm.LinearSVC(random_state=RANDOM_SEED)),
        classification_binary(svm.LinearSVC(random_state=RANDOM_SEED)),

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


        # This a special case of the HUGE model. We want to verify that
        # even in such cases we generate code which works.
        regression(ensemble.RandomForestRegressor(n_estimators=100),
                   is_fast=True),
    ],

    # Following is the list of extra tests for languages/models which are
    # not fully supported yet.

    # <empty>
)
def test_e2e(estimator, executor_cls, model_trainer, is_fast_model, is_fast):
    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    # is_fast means that user used --flag.
    # is_fast_model means that this model is explicitly specified to run fast.
    is_fast = is_fast_model or is_fast

    idxs_to_test = [0] if is_fast else range(len(X_test))

    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed, atol=ATOL)
            assert res if isinstance(res, bool) else res.all()
