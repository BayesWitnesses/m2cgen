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


@utils.cartesian_e2e_params(
    # These are languages which support all models.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
    ],
    [
        # Linear Regression/Classification
        (
            linear_model.LinearRegression(),
            utils.train_model_regression,
            REGRESSION,
        ),
        (
            linear_model.LogisticRegression(),
            utils.train_model_classification_binary,
            CLASSIFICATION,
        ),
        (
            linear_model.LogisticRegression(),
            utils.train_model_classification,
            CLASSIFICATION,
        ),

        # Decision trees
        (
            tree.DecisionTreeRegressor(),
            utils.train_model_regression,
            REGRESSION,
        ),
        (
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            utils.train_model_classification,
            CLASSIFICATION,
        ),
        (
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            utils.train_model_classification_binary,
            CLASSIFICATION,
        ),

        # Random forest
        (
            ensemble.RandomForestRegressor(n_estimators=10,
                                           random_state=RANDOM_SEED),
            utils.train_model_regression,
            REGRESSION,
        ),
        (
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            utils.train_model_classification,
            CLASSIFICATION,
        ),
        (
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            utils.train_model_classification_binary,
            CLASSIFICATION,
        ),
    ],

    # C
    pytest.param(
        linear_model.LinearRegression(),
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        tree.DecisionTreeRegressor(random_state=RANDOM_SEED),
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        ensemble.RandomForestRegressor(n_estimators=10,
                                       random_state=RANDOM_SEED),
        executors.CExecutor,
        utils.train_model_regression,
        marks=[C, REGRESSION],
    ),
    pytest.param(
        linear_model.LogisticRegression(),
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
