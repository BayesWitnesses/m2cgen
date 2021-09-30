import pytest
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import RANSACRegressor
from sklearn.tree import DecisionTreeRegressor

from m2cgen import ast
from m2cgen.assemblers import RANSACModelAssembler

from tests.utils import cmp_exprs


def test_ransac_custom_base_estimator():
    base_estimator = DecisionTreeRegressor(random_state=1, max_depth=1)
    estimator = RANSACRegressor(base_estimator=base_estimator, random_state=1)
    estimator.fit([[1], [2]], [1, 2])

    assembler = RANSACModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(1.5),
            ast.CompOpType.LTE),
        ast.NumVal(1.0),
        ast.NumVal(2.0))

    assert cmp_exprs(actual, expected)


def test_ransac_unknown_base_estimator():
    base_estimator = DummyRegressor()
    estimator = RANSACRegressor(base_estimator=base_estimator, random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = RANSACModelAssembler(estimator)

    with pytest.raises(NotImplementedError, match="Model 'sklearn_DummyRegressor' is not supported"):
        assembler.assemble()
