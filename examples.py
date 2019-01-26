import numpy as np

from sklearn.datasets import load_boston
from sklearn import linear_model
from sklearn import ensemble
from sklearn import tree
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.utils import shuffle

from m2cgen import exporters


def train_model(estimator):
    boston = load_boston()

    X, y = shuffle(boston.data, boston.target, random_state=13)
    X = X.astype(np.float32)

    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    estimator.fit(X_train, y_train)

    y_pred = estimator.predict(X_test)
    print("Test score: " + str(y_pred[0]))

    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    print("Variance score: %.2f" % r2_score(y_test, y_pred))


def print_model(defined_classes):
    print(defined_classes[0][1])


def example_linear():
    estimator = linear_model.LinearRegression()
    train_model(estimator)

    print("Coef", estimator.coef_)
    print("Intercept", estimator.intercept_)

    exporter = exporters.PythonExporter(estimator)
    print_model(exporter.export())


def example_tree():
    estimator = tree.DecisionTreeRegressor()
    train_model(estimator)

    exporter = exporters.PythonExporter(estimator)
    print_model(exporter.export())


def example_random_forest():
    estimator = ensemble.RandomForestRegressor(n_estimators=10)
    train_model(estimator)

    exporter = exporters.JavaExporter(estimator)
    print_model(exporter.export())


if __name__ == "__main__":
    example_linear()

    example_tree()

    example_random_forest()
