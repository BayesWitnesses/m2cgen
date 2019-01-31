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


def exec_e2e_test(estimator, executor_cls, model_trainer, is_fast):
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


@pytest.mark.parametrize("estimator,executor_cls,model_trainer", [
    # Java
    pytest.param(
            linear_model.LinearRegression(),
            executors.JavaExecutor,
            utils.train_model_regression,
            marks=[JAVA, REGRESSION],
    ),
    pytest.param(
            linear_model.LogisticRegression(),
            executors.JavaExecutor,
            utils.train_model_classification,
            marks=[JAVA, CLASSIFICATION],
    ),
    pytest.param(
            linear_model.LogisticRegression(),
            executors.JavaExecutor,
            utils.train_model_classification_binary,
            marks=[JAVA, CLASSIFICATION],
    ),
    pytest.param(
            tree.DecisionTreeRegressor(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_regression,
            marks=[JAVA, REGRESSION],
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification,
            marks=[JAVA, CLASSIFICATION, pytest.mark.qwerty2],
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification_binary,
            marks=[JAVA, CLASSIFICATION],
    ),
    pytest.param(
            ensemble.RandomForestRegressor(n_estimators=10,
                                           random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_regression,
            marks=[JAVA, REGRESSION],
    ),

    # Python
    pytest.param(
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification_binary,
            marks=[JAVA, CLASSIFICATION],
    ),
    pytest.param(
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            executors.JavaExecutor,
            utils.train_model_classification,
            marks=[JAVA, CLASSIFICATION],
    ),
    pytest.param(
            linear_model.LinearRegression(),
            executors.PythonExecutor,
            utils.train_model_regression,
            marks=[PYTHON, REGRESSION],
    ),
    pytest.param(
            tree.DecisionTreeRegressor(random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_regression,
            marks=[PYTHON, REGRESSION],
    ),
    pytest.param(
            ensemble.RandomForestRegressor(n_estimators=10,
                                           random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_regression,
            marks=[PYTHON, REGRESSION],
    ),
    pytest.param(
            linear_model.LogisticRegression(),
            executors.PythonExecutor,
            utils.train_model_classification,
            marks=[PYTHON, CLASSIFICATION],
    ),
    pytest.param(
            linear_model.LogisticRegression(),
            executors.PythonExecutor,
            utils.train_model_classification_binary,
            marks=[PYTHON, CLASSIFICATION],
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_classification,
            marks=[PYTHON, CLASSIFICATION],
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_classification_binary,
            marks=[PYTHON, CLASSIFICATION],
    ),
    pytest.param(
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_classification_binary,
            marks=[PYTHON, CLASSIFICATION],
    ),
    pytest.param(
            ensemble.RandomForestClassifier(n_estimators=10,
                                            random_state=RANDOM_SEED),
            executors.PythonExecutor,
            utils.train_model_classification,
            marks=[PYTHON, CLASSIFICATION],
    ),

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
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.CExecutor,
            utils.train_model_classification,
            marks=[C, CLASSIFICATION, pytest.mark.qwerty],
    ),
    pytest.param(
            tree.DecisionTreeClassifier(random_state=RANDOM_SEED),
            executors.CExecutor,
            utils.train_model_classification_binary,
            marks=[C, CLASSIFICATION, pytest.mark.qwerty],
    ),
])
def test_e2e(estimator, executor_cls, model_trainer, is_fast):
    exec_e2e_test(estimator, executor_cls, model_trainer, is_fast)
