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


def test_java_linear_regression():
    estimator = linear_model.LinearRegression()
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_regression)


def test_java_logistic_classification():
    estimator = linear_model.LogisticRegression()
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_classification)


def test_java_logistic_classification_binary():
    estimator = linear_model.LogisticRegression()
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_classification_binary)


def test_java_tree_regression():
    estimator = tree.DecisionTreeRegressor(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_regression)


def test_java_tree_classification():
    estimator = tree.DecisionTreeClassifier(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_classification)


def test_java_tree_classification_binary():
    estimator = tree.DecisionTreeClassifier(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_classification_binary)


def test_java_ensemble():
    estimator = ensemble.RandomForestRegressor(n_estimators=10,
                                               random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.JavaExecutor,
                  utils.train_model_regression)


def test_python_linear():
    estimator = linear_model.LinearRegression()
    exec_e2e_test(estimator, executors.PythonExecutor,
                  utils.train_model_regression)


def test_python_tree():
    estimator = tree.DecisionTreeRegressor(random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.PythonExecutor,
                  utils.train_model_regression)


def test_python_ensemble():
    estimator = ensemble.RandomForestRegressor(n_estimators=10,
                                               random_state=RANDOM_SEED)
    exec_e2e_test(estimator, executors.PythonExecutor,
                  utils.train_model_regression)
