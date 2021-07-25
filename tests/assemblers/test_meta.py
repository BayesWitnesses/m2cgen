import pytest
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import RANSACRegressor
from sklearn.tree import DecisionTreeRegressor

from m2cgen import ast
from m2cgen.assemblers import RANSACModelAssembler

from tests.utils import cmp_exprs


def test_ransac_custom_base_estimator():
    base_estimator = DecisionTreeRegressor()
    estimator = RANSACRegressor(base_estimator=base_estimator, random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = RANSACModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.IfExpr(
        ast.CompExpr(
            ast.FeatureRef(0),
            ast.NumVal(2.5),
            ast.CompOpType.LTE),
        ast.NumVal(2.0),
        ast.NumVal(3.0))

    assert cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=NotImplementedError, strict=True)
def test_ransac_unknown_base_estimator():
    base_estimator = DummyRegressor()
    estimator = RANSACRegressor(base_estimator=base_estimator, random_state=1)
    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = RANSACModelAssembler(estimator)
    assembler.assemble()
