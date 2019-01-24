import numpy as np
import pytest
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RANDOM_SEED = 1234


def exec_e2e_test(estimator, executor_cls, fail_fast):
    X_test, y_pred_true = utils.train_model(estimator)
    executor = executor_cls(estimator)

    failed_indexes = []

    for idx in range(len(X_test)):
        y_pred_executed = executor.predict(X_test[idx])
        print("expected={}, actual={}".format(y_pred_true[idx],
                                              y_pred_executed))

        if fail_fast:
            assert np.isclose(y_pred_true[idx], y_pred_executed)
        else:
            if not np.isclose(y_pred_true[idx], y_pred_executed):
                failed_indexes.append(idx)

    assert failed_indexes == []


def test_java_linear(xx):
    estimator = linear_model.LinearRegression()
    exec_e2e_test(estimator, executors.JavaExecutor, xx)


def test_java_tree(xx):
    estimator = tree.DecisionTreeRegressor(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor, xx)


@pytest.mark.skip(reason="Random Forest assembler is broken")
def test_java_ensemble(xx):
    estimator = ensemble.RandomForestRegressor(n_estimators=10,
                                               random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor, xx)
