import numpy as np

from sklearn.datasets import load_boston
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.utils import shuffle

from m2cgen import ast
from m2cgen.assemblers import LinearRegressionAssembler
from m2cgen.interpreters import JavaGenerator


def example_linear():
    boston = load_boston()

    X, y = shuffle(boston.data, boston.target, random_state=13)
    X = X.astype(np.float32)

    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    clf = linear_model.LinearRegression()

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Test score: " + str(y_pred[0]))

    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    print("Variance score: %.2f" % r2_score(y_test, y_pred))

    print("Coef", clf.coef_)
    print("Intercept", clf.intercept_)

    converter = LinearRegressionAssembler(clf)

    ast = converter.assemble()
    interpreter = JavaGenerator()
    print(interpreter.interpret(ast))


def example_with_if_confition():
    left = ast.BinNumExpr(
        ast.IfExpr(
            ast.BinBoolExpr(ast.NumVal(1),
                            ast.NumVal(1),
                            ast.BinBoolOpType.EQ),
            ast.NumVal(1),
            ast.NumVal(2)),
        ast.NumVal(2),
        ast.BinNumOpType.ADD)

    right = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.DIV)
    bool_test = ast.BinBoolExpr(left, right, ast.BinBoolOpType.GTE)

    expr = ast.IfExpr(bool_test, ast.NumVal(1), ast.NumVal(2))

    interpreter = JavaGenerator()
    print(interpreter.interpret(expr))


if __name__ == "__main__":
    example_linear()

    example_with_if_confition()
