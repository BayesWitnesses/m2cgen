import pytest
import numpy as np
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RANDOM_SEED = 1234

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


def binary_classification(model):
    return (
        model,
        utils.train_model_classification_binary,
        CLASSIFICATION,
    )


linear_regressor = linear_model.LinearRegression()
logistic_regressor = linear_model.LogisticRegression()
decision_tree_regressor = tree.DecisionTreeRegressor()
decision_tree_classifier = tree.DecisionTreeClassifier(
    random_state=RANDOM_SEED)
random_forest_regressor = ensemble.RandomForestRegressor(
    n_estimators=10, random_state=RANDOM_SEED)
random_forest_classifier = ensemble.RandomForestClassifier(
    n_estimators=10, random_state=RANDOM_SEED)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
    ],

    # These models will be executed against each language specified in the
    # previous list
    [
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

        # Logistic Regression
        classification(logistic_regressor),
        binary_classification(logistic_regressor),
        classification(linear_model.LogisticRegressionCV()),
        binary_classification(linear_model.LogisticRegressionCV()),

        # Decision trees
        regression(decision_tree_regressor),
        classification(decision_tree_classifier),
        binary_classification(decision_tree_classifier),

        regression(tree.ExtraTreeRegressor()),
        classification(tree.ExtraTreeClassifier()),
        binary_classification(tree.ExtraTreeClassifier()),

        # Random forest
        regression(random_forest_regressor),
        classification(random_forest_classifier),
        binary_classification(random_forest_classifier),

        regression(ensemble.ExtraTreesRegressor(
            n_estimators=10, random_state=RANDOM_SEED)),
        classification(ensemble.ExtraTreesClassifier(
            n_estimators=10, random_state=RANDOM_SEED)),
        binary_classification(ensemble.ExtraTreesClassifier(
            n_estimators=10, random_state=RANDOM_SEED)),
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
        linear_regressor,
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
