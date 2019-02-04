import contextlib
import shutil
import subprocess
import tempfile
import numpy as np

from sklearn import datasets
from sklearn.ensemble import forest
from sklearn.utils import shuffle
from sklearn.linear_model.base import LinearClassifierMixin
from sklearn.tree import DecisionTreeClassifier

from m2cgen import ast


def cmp_exprs(left, right):
    """Recursively compares two ast expressions."""

    if isinstance(left, ast.VectorVal) and isinstance(right, ast.Expr):
        left_exprs = left.exprs
        right_exprs = right.exprs
        assert len(left_exprs) == len(right_exprs)
        for l, r in zip(left_exprs, right_exprs):
            assert cmp_exprs(l, r)
        return True

    if not isinstance(left, ast.Expr) and not isinstance(right, ast.Expr):
        assert left == right, str(left) + " != " + str(right)
        return True

    if isinstance(left, ast.Expr) and isinstance(right, ast.Expr):
        assert isinstance(left, type(right)), (
            "Expected instance of {}, received {}".format(
                type(right), type(left)))

        # Only compare attributes which don't start with __
        attrs_to_compare = filter(
            lambda attr_name: not attr_name.startswith('__'), dir(left))

        for attr_name in attrs_to_compare:
            assert cmp_exprs(
                getattr(left, attr_name), getattr(right, attr_name))

        return True

    return False


def assert_code_equal(actual, expected):
    assert actual.strip() == expected.strip()


def train_model_regression(estimator, test_fraction=0.1):
    return _train_model(estimator, datasets.load_boston(), test_fraction)


def train_model_classification(estimator, test_fraction=0.1):
    return _train_model(estimator, datasets.load_iris(), test_fraction)


def train_model_classification_binary(estimator, test_fraction=0.1):
    return _train_model(estimator, datasets.load_breast_cancer(),
                        test_fraction)


def _train_model(estimator, dataset, test_fraction):
    X, y = shuffle(dataset.data, dataset.target, random_state=13)

    offset = int(X.shape[0] * (1 - test_fraction))
    X_train, y_train = X[:offset], y[:offset]
    X_test = X[offset:]

    estimator.fit(X_train, y_train)

    if isinstance(estimator, LinearClassifierMixin):
        y_pred = estimator.decision_function(X_test)
    elif isinstance(estimator, DecisionTreeClassifier):
        y_pred = estimator.predict_proba(X_test.astype(np.float32))
    elif isinstance(estimator, forest.ForestClassifier):
        y_pred = estimator.predict_proba(X_test)
    else:
        y_pred = estimator.predict(X_test)

    return X_test, y_pred


@contextlib.contextmanager
def tmp_dir():
    dirpath = tempfile.mkdtemp()

    try:
        yield dirpath
    finally:
        shutil.rmtree(dirpath)


def predict_from_commandline(exec_args):
    result = subprocess.Popen(exec_args, stdout=subprocess.PIPE)
    items = result.stdout.read().decode("utf-8").strip().split(" ")
    if len(items) == 1:
        return float(items[0])
    else:
        return [float(i) for i in items]
