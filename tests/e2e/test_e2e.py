import pytest
import numpy as np
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RANDOM_SEED = 1234


def exec_e2e_test(estimator, executor_cls, model_trainer):
    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    with executor.prepare_then_cleanup():
        for idx in range(len(X_test)):
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed)
            assert res if isinstance(res, bool) else res.all()


@pytest.mark.parametrize("estimator,executor_cls,model_trainer", [
    (
            linear_model.LinearRegression(),
            executors.JavaExecutor,
            utils.train_model_regression
    ),
    (
            linear_model.LogisticRegression(),
            executors.JavaExecutor,
            utils.train_model_classification
    ),
    (
            linear_model.LogisticRegression(),
            executors.JavaExecutor,
            utils.train_model_classification_binary
    ),
    (
            tree.DecisionTreeRegressor(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_regression
    ),
    (
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification
    ),
    (
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification_binary
    ),
    (
            ensemble.RandomForestRegressor(n_estimators=10,
                                           random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_regression
    ),
    (
            linear_model.LinearRegression(),
            executors.PythonExecutor,
            utils.train_model_regression
    ),
    (
            tree.DecisionTreeRegressor(random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_regression
    ),
    (
            ensemble.RandomForestRegressor(n_estimators=10,
                                           random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_regression
    ),
])
def test_e2e(estimator, executor_cls, model_trainer):
    exec_e2e_test(estimator, executor_cls, model_trainer)
