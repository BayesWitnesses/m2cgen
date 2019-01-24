import numpy as np
import pytest
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RANDOM_SEED = 1234


def exec_e2e_test(estimator, executor_cls):
    X_test, y_pred_true = utils.train_model(estimator)
    executor = executor_cls(estimator)

    for idx in range(len(X_test)):
        y_pred_executed = executor.predict(X_test[idx])
        print("expected={}, actual={}".format(y_pred_true[idx],
                                              y_pred_executed))
        assert np.isclose(y_pred_true[idx], y_pred_executed)


def test_java_linear():
    estimator = linear_model.LinearRegression()
    exec_e2e_test(estimator, executors.JavaExecutor)


def test_java_tree():
    estimator = tree.DecisionTreeRegressor(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor)


@pytest.mark.skip(reason="Random Forest assembler is broken")
def test_java_ensemble():
    estimator = ensemble.RandomForestRegressor(n_estimators=10,
                                               random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor)
