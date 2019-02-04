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


RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)


# Reusable models for e2e tests. They will be cloned on each execution.
linear_regressor = linear_model.LinearRegression()
logistic_regressor = linear_model.LogisticRegression()
decision_tree_regressor = tree.DecisionTreeRegressor(**TREE_PARAMS)
decision_tree_classifier = tree.DecisionTreeClassifier(**TREE_PARAMS)
random_forest_regressor = ensemble.RandomForestRegressor(**FOREST_PARAMS)
random_forest_classifier = ensemble.RandomForestClassifier(**FOREST_PARAMS)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
    ],

    # These models will be tested against each language specified in the
    # previous list.
    [
        # SVM
        regression(svm.LinearSVR(random_state=RANDOM_SEED)),
        classification(svm.LinearSVC(random_state=RANDOM_SEED)),
        classification_binary(svm.LinearSVC(random_state=RANDOM_SEED)),

        # Linear Regression
        regression(linear_regressor),
        regression(linear_model.HuberRegressor()),
        regression(linear_model.ElasticNet()),
        regression(linear_model.ElasticNetCV()),
        regression(linear_model.TheilSenRegressor()),
        regression(linear_model.Lars()),
        regression(linear_model.LarsCV()),
        regression(linear_model.Lasso()),
        regression(linear_model.LassoCV()),
        regression(linear_model.LassoLars()),
        regression(linear_model.LassoLarsIC()),
        regression(linear_model.OrthogonalMatchingPursuit()),
        regression(linear_model.OrthogonalMatchingPursuitCV()),
        regression(linear_model.Ridge()),
        regression(linear_model.RidgeCV()),
        regression(linear_model.BayesianRidge()),
        regression(linear_model.ARDRegression()),
        regression(linear_model.SGDRegressor()),
        regression(linear_model.PassiveAggressiveRegressor()),

        # Logistic Regression
        classification(logistic_regressor),
        classification(linear_model.LogisticRegressionCV()),
        classification(linear_model.RidgeClassifier()),
        classification(linear_model.RidgeClassifierCV()),
        classification(linear_model.SGDClassifier()),

        classification_binary(logistic_regressor),
        classification_binary(linear_model.LogisticRegressionCV()),
        classification_binary(linear_model.RidgeClassifier()),
        classification_binary(linear_model.RidgeClassifierCV()),
        classification_binary(linear_model.SGDClassifier()),


        # Decision trees
        regression(decision_tree_regressor),
        regression(tree.ExtraTreeRegressor()),

        classification(decision_tree_classifier),
        classification(tree.ExtraTreeClassifier()),

        classification_binary(decision_tree_classifier),
        classification_binary(tree.ExtraTreeClassifier()),


        # Random forest
        regression(random_forest_regressor),
        regression(ensemble.ExtraTreesRegressor(**FOREST_PARAMS)),

        classification(random_forest_classifier),
        classification(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),

        classification_binary(random_forest_classifier),
        classification_binary(ensemble.ExtraTreesClassifier(**FOREST_PARAMS)),
    ],

    # Following is the list of extra tests for languages/models which are
    # not fully supported yet.

    # C
    pytest.param(
        linear_regressor,
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        decision_tree_regressor,
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        random_forest_regressor,
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        logistic_regressor,
        executors.CExecutor,
        utils.train_model_classification_binary,
        marks=[C, CLASSIFICATION],
    )
)
def test_e2e(estimator, executor_cls, model_trainer, is_fast):
    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    idxs_to_test = [0] if is_fast else range(len(X_test))

    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed)
            assert res if isinstance(res, bool) else res.all()
