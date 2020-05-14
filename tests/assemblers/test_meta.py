import pytest
from sklearn import linear_model
from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor

from m2cgen import assemblers, ast
from tests import utils


def test_ransac_custom_base_estimator():
    base_estimator = DecisionTreeRegressor()
    estimator = linear_model.RANSACRegressor(
        base_estimator=base_estimator,
        random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.RANSACModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(2.5),
            ast.CompOpType.LTE),
        ast.NumVal(2.0),
        ast.NumVal(3.0))

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=NotImplementedError, strict=True)
def test_ransac_unknown_base_estimator():
    base_estimator = DummyRegressor()
    estimator = linear_model.RANSACRegressor(
        base_estimator=base_estimator,
        random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.RANSACModelAssembler(estimator)
    assembler.assemble()
