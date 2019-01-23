import numpy as np
from sklearn.datasets import load_boston

from m2cgen import ast


def train_model(estimator, n_params, random_state=13):
    """
    Trains test model with specified number of features.
    """
    boston = load_boston()

    X = boston.data.astype(np.float32)
    y = boston.target

    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset, :n_params], y[:offset]

    estimator.fit(X_train, y_train)


def cmp_exprs(left, right):
    """Recursively compares two ast expressions."""

    if isinstance(left, np.float32) and isinstance(right, np.float32):
        assert np.isclose(left, right)
        return True

    if not isinstance(left, ast.Expr) and not isinstance(right, ast.Expr):
        assert left == right
        return True

    if isinstance(left, ast.Expr) and isinstance(right, ast.Expr):
        # Only compare attributes which don't start with __
        attrs_to_compare = filter(
            lambda attr_name: not attr_name.startswith('__'), dir(left))

        for attr_name in attrs_to_compare:
            assert cmp_exprs(
                getattr(left, attr_name), getattr(right, attr_name))

        return True

    return False
