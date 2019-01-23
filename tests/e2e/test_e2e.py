import numpy as np
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


def exec_e2e_test(estimator, executor_cls):
    X_test, y_pred_true = utils.train_model(estimator)
    executor = executor_cls(estimator)
    y_pred_executed = executor.predict(X_test[0])

    print(y_pred_true[0], y_pred_executed)
    assert np.isclose(y_pred_true[0], y_pred_executed)


def test_java_linear():
    estimator = linear_model.LinearRegression()
    exec_e2e_test(estimator, executors.JavaExecutor)


def test_java_tree():
    estimator = tree.DecisionTreeRegressor()
    exec_e2e_test(estimator, executors.JavaExecutor)


def test_java_ensemble():
    estimator = ensemble.RandomForestRegressor(n_estimators=10)
    exec_e2e_test(estimator, executors.JavaExecutor)
