import contextlib
import functools
import itertools
import shutil
import subprocess
import tempfile

import numpy as np
import pytest
import statsmodels.api as sm

from lightgbm import LGBMClassifier
from lightning.impl.base import BaseClassifier as LightBaseClassifier
from sklearn import datasets
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.ensemble._forest import ForestClassifier, BaseForest
from sklearn.model_selection import train_test_split
from sklearn.linear_model._base import LinearClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree._classes import BaseDecisionTree
from sklearn.svm import SVC, NuSVC
from sklearn.svm._base import BaseLibSVM
from xgboost import XGBClassifier

from m2cgen import ast
from m2cgen.assemblers import _get_full_model_name
from m2cgen.interpreters.utils import format_float


class StatsmodelsSklearnLikeWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, model, params):
        self.model = model
        self.params = params
        # mock class module and name to show appropriate model name in tests
        self.__class__.__module__ = model.__module__
        self.__class__.__name__ = model.__name__

    def fit(self, X, y):
        init_params = self.params.get("init", {})
        self.fit_intercept_ = init_params.pop("fit_intercept", False)
        if self.fit_intercept_:
            X = sm.add_constant(X)
        est = self.model(y, X, **init_params)
        if "fit_regularized" in self.params:
            self.fitted_model_ = est.fit_regularized(
                **self.params["fit_regularized"])
        elif "iterative_fit" in self.params:
            self.fitted_model_ = est.iterative_fit(
                **self.params["iterative_fit"])
        elif "fit_constrained" in self.params:
            self.fitted_model_ = est.fit_constrained(
                **self.params["fit_constrained"])
        else:
            self.fitted_model_ = est.fit(**self.params.get("fit", {}))
        # mock class module and name to show appropriate model name in tests
        self.__class__.__module__ = type(self.fitted_model_).__module__
        self.__class__.__name__ = type(self.fitted_model_).__name__
        return self.fitted_model_

    def predict(self, X):
        if self.fit_intercept_:
            X = sm.add_constant(X)
        return self.fitted_model_.predict(X)


class ModelTrainer:

    _class_instances = {}

    def __init__(self, dataset_name, test_fraction):
        self.dataset_name = dataset_name
        self.test_fraction = test_fraction
        additional_test_data = None
        np.random.seed(seed=7)
        if dataset_name == "boston":
            self.name = "train_model_regression"
            self.X, self.y = datasets.load_boston(return_X_y=True)
        elif dataset_name == "boston_y_bounded":
            self.name = "train_model_regression_bounded"
            self.X, self.y = datasets.load_boston(return_X_y=True)
            self.y = np.arctan(self.y) / np.pi + 0.5  # (0; 1)
        elif dataset_name == "diabetes":
            self.name = "train_model_regression_w_missing_values"
            self.X, self.y = datasets.load_diabetes(return_X_y=True)
            additional_test_data = np.array([
                [np.NaN] * self.X.shape[1],
            ])
        elif dataset_name == "iris":
            self.name = "train_model_classification"
            self.X, self.y = datasets.load_iris(return_X_y=True)
        elif dataset_name == "breast_cancer":
            self.name = "train_model_classification_binary"
            self.X, self.y = datasets.load_breast_cancer(return_X_y=True)
        elif dataset_name == "regression_rnd":
            self.name = "train_model_regression_random_data"
            N = 1000
            self.X = np.random.random(size=(N, 200))
            self.y = np.random.random(size=(N,))
        elif dataset_name == "classification_rnd":
            self.name = "train_model_classification_random_data"
            N = 1000
            self.X = np.random.random(size=(N, 200))
            self.y = np.random.randint(3, size=(N,))
        elif dataset_name == "classification_rnd_w_missing_values":
            self.name = "train_model_classification_rnd_w_missing_values"
            N = 100
            self.X = np.random.random(size=(N, 20)) - 0.5
            self.y = np.random.randint(3, size=(N,))
            additional_test_data = np.array([
                [np.NaN] * self.X.shape[1],
            ])
        elif dataset_name == "classification_binary_rnd":
            self.name = "train_model_classification_binary_random_data"
            N = 1000
            self.X = np.random.random(size=(N, 200))
            self.y = np.random.randint(2, size=(N,))
        elif dataset_name == "classification_binary_rnd_w_missing_values":
            self.name = \
                "train_model_classification_binary_rnd_w_missing_values"
            N = 100
            self.X = np.random.random(size=(N, 20)) - 0.5
            self.y = np.random.randint(2, size=(N,))
            additional_test_data = np.array([
                [np.NaN] * self.X.shape[1],
            ])
        else:
            raise ValueError(f"Unknown dataset name: {dataset_name}")

        (self.X_train, self.X_test,
         self.y_train, _) = train_test_split(
            self.X, self.y, test_size=test_fraction, random_state=15)
        if additional_test_data is not None:
            self.X_test = np.vstack((additional_test_data, self.X_test))

    @classmethod
    def get_instance(cls, dataset_name, test_fraction=0.02):
        key = f"{dataset_name} {test_fraction}"
        if key not in cls._class_instances:
            cls._class_instances[key] = ModelTrainer(
                dataset_name, test_fraction)
        return cls._class_instances[key]

    def __call__(self, estimator):
        fitted_estimator = estimator.fit(self.X_train, self.y_train)

        if isinstance(estimator, (LinearClassifierMixin, SVC, NuSVC,
                                  LightBaseClassifier)):
            y_pred = estimator.decision_function(self.X_test)
        elif isinstance(
                estimator,
                (ForestClassifier, DecisionTreeClassifier,
                 XGBClassifier, LGBMClassifier)):
            y_pred = estimator.predict_proba(self.X_test)
        else:
            y_pred = estimator.predict(self.X_test)

        # Some models force input data to be particular type
        # during prediction phase in their native Python libraries.
        # For correct comparison of testing results we mimic the same behavior
        if isinstance(estimator, (BaseDecisionTree, BaseForest)):
            self.X_test = self.X_test.astype(np.float32, copy=False)
        elif isinstance(estimator, BaseLibSVM):
            self.X_test = self.X_test.astype(np.float64, copy=False)

        return self.X_test, y_pred, fitted_estimator


def cmp_exprs(left, right):
    """Recursively compares two ast expressions."""

    if isinstance(left, ast.VectorVal) and isinstance(right, ast.Expr):
        left_exprs = left.exprs
        right_exprs = right.exprs
        assert len(left_exprs) == len(right_exprs)
        for left_expr, right_expr in zip(left_exprs, right_exprs):
            assert cmp_exprs(left_expr, right_expr)
        return True

    if not isinstance(left, ast.Expr) and not isinstance(right, ast.Expr):
        if _is_float(left) and _is_float(right):
            comp_res = np.isclose(left, right)
        else:
            comp_res = left == right
        assert comp_res, f"{left} != {right}"
        return True

    if isinstance(left, ast.Expr) and isinstance(right, ast.Expr):
        assert isinstance(left, type(right)), (
            f"Expected instance of {type(right)}, received {type(left)}")

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


get_regression_model_trainer = functools.partial(
    ModelTrainer.get_instance, "boston")


get_classification_model_trainer = functools.partial(
    ModelTrainer.get_instance, "iris")


get_binary_classification_model_trainer = functools.partial(
    ModelTrainer.get_instance, "breast_cancer")


get_regression_random_data_model_trainer = functools.partial(
    ModelTrainer.get_instance, "regression_rnd")


get_classification_random_data_model_trainer = functools.partial(
    ModelTrainer.get_instance, "classification_rnd")


get_classification_binary_random_data_model_trainer = functools.partial(
    ModelTrainer.get_instance, "classification_binary_rnd")


get_bounded_regression_model_trainer = functools.partial(
    ModelTrainer.get_instance, "boston_y_bounded")


get_regression_w_missing_values_model_trainer = functools.partial(
    ModelTrainer.get_instance, "diabetes")


get_classification_random_w_missing_values_model_trainer = functools.partial(
    ModelTrainer.get_instance, "classification_rnd_w_missing_values")


get_classification_binary_random_w_missing_values_model_trainer = \
    functools.partial(
        ModelTrainer.get_instance,
        "classification_binary_rnd_w_missing_values")


@contextlib.contextmanager
def tmp_dir():
    dirpath = tempfile.mkdtemp()

    try:
        yield dirpath
    finally:
        shutil.rmtree(dirpath)


def verify_python_model_is_expected(model_code, input, expected_output):
    input_str = f"[{', '.join(map(str, input))}]"
    code = f"""
{model_code}
result = score({input_str})"""

    context = {}
    exec(code, context)

    assert np.isclose(context["result"], expected_output)


def predict_from_commandline(exec_args):
    result = subprocess.Popen(exec_args, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    if result.returncode != 0:
        raise Exception(
            f"Bad exit code ({result.returncode}), "
            f"stderr:\n{stderr.decode('utf-8')}")

    items = stdout.decode("utf-8").strip().split(" ")

    if len(items) == 1:
        return np.float64(items[0])
    else:
        return [np.float64(i) for i in items]


def cartesian_e2e_params(executors_with_marks, models_with_trainers_with_marks,
                         skip_executor_trainer_pairs, *additional_params):
    result_params = list(additional_params)

    # Specifying None for additional parameters makes pytest to generate
    # automatic ids. If we don't do this pytest will throw exception that
    # number of parameters doesn't match number of provided ids
    ids = [None] * len(additional_params)

    prod = itertools.product(
        executors_with_marks, models_with_trainers_with_marks)

    for (executor, executor_mark), (model, trainer, trainer_mark) in prod:
        if (executor_mark, trainer_mark) in skip_executor_trainer_pairs:
            continue

        # Since we reuse the same model across multiple tests we want it
        # to be clean.
        model = clone(model)

        # We use custom id since pytest for some reason can't show name of
        # the model in the automatic id. Which sucks.
        ids.append(f"{_get_full_model_name(model)} - "
                   f"{executor_mark.name} - {trainer.name}")

        result_params.append(pytest.param(
            model, executor, trainer, marks=[executor_mark, trainer_mark],
        ))

    param_names = "estimator,executor_cls,model_trainer"

    def wrap(func):

        @pytest.mark.parametrize(param_names, result_params, ids=ids)
        @functools.wraps(func)
        def inner(*args, **kwarg):
            return func(*args, **kwarg)

        return inner

    return wrap


def _is_float(value):
    return isinstance(value, (float, np.floating))


def format_arg(value):
    if np.isnan(value):
        return "NaN"

    return format_float(value)
