from copy import deepcopy

import numpy as np
import pytest

from m2cgen import ast


def test_count_exprs():
    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD)
    ) == 3

    assert ast.count_exprs(
        ast.ExpExpr(ast.NumVal(2))
    ) == 2

    assert ast.count_exprs(
        ast.VectorVal([
            ast.NumVal(2),
            ast.TanhExpr(ast.NumVal(3))
        ])
    ) == 4

    assert ast.count_exprs(
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(2), ast.NumVal(0), ast.CompOpType.GT),
            ast.NumVal(3),
            ast.NumVal(4),
        )
    ) == 6

    assert ast.count_exprs(ast.NumVal(1)) == 1

    with pytest.raises(ValueError, match="Unexpected expression type 'VectorExpr'"):
        ast.count_exprs(ast.VectorExpr())


def test_count_exprs_exclude_list():
    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinExpr, ast.NumVal}
    ) == 0

    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinNumExpr}
    ) == 2


EXPR_WITH_ALL_EXPRS = ast.BinVectorNumExpr(
    ast.BinVectorExpr(
        ast.VectorVal([
            ast.AbsExpr(ast.NumVal(-2)),
            ast.AtanExpr(ast.NumVal(2)),
            ast.ExpExpr(ast.NumVal(2)),
            ast.LogExpr(ast.NumVal(2)),
            ast.Log1pExpr(ast.NumVal(2)),
            ast.SigmoidExpr(ast.NumVal(2)),
            ast.SqrtExpr(ast.NumVal(2)),
            ast.PowExpr(ast.NumVal(2), ast.NumVal(3)),
            ast.TanhExpr(ast.NumVal(1)),
            ast.BinNumExpr(
                ast.NumVal(0),
                ast.FeatureRef(0),
                ast.BinNumOpType.ADD)
        ]),
        ast.IdExpr(
            ast.SoftmaxExpr([
                ast.NumVal(1),
                ast.NumVal(2),
                ast.NumVal(3),
                ast.NumVal(4),
                ast.NumVal(5),
                ast.NumVal(6),
                ast.NumVal(7),
                ast.NumVal(8),
                ast.NumVal(9),
                ast.FeatureRef(1)
            ])),
        ast.BinNumOpType.SUB),
    ast.IfExpr(
        ast.CompExpr(ast.NumVal(2), ast.NumVal(0), ast.CompOpType.GT),
        ast.NumVal(3),
        ast.NumVal(4),
    ),
    ast.BinNumOpType.MUL)


def test_count_all_exprs_types():
    assert ast.count_exprs(EXPR_WITH_ALL_EXPRS) == 43


def test_exprs_equality():
    expr_copy = deepcopy(EXPR_WITH_ALL_EXPRS)
    assert EXPR_WITH_ALL_EXPRS == expr_copy


def test_exprs_hash():
    expr_copy = deepcopy(EXPR_WITH_ALL_EXPRS)
    assert hash(EXPR_WITH_ALL_EXPRS) == hash(expr_copy)


def test_exprs_str():
    assert str(EXPR_WITH_ALL_EXPRS) == """
BinVectorNumExpr(BinVectorExpr(VectorVal([
AbsExpr(NumVal(-2.0),to_reuse=False),
AtanExpr(NumVal(2.0),to_reuse=False),
ExpExpr(NumVal(2.0),to_reuse=False),
LogExpr(NumVal(2.0),to_reuse=False),
Log1pExpr(NumVal(2.0),to_reuse=False),
SigmoidExpr(NumVal(2.0),to_reuse=False),
SqrtExpr(NumVal(2.0),to_reuse=False),
PowExpr(NumVal(2.0),NumVal(3.0),to_reuse=False),
TanhExpr(NumVal(1.0),to_reuse=False),
BinNumExpr(NumVal(0.0),FeatureRef(0),ADD,to_reuse=False)]),
IdExpr(SoftmaxExpr(
NumVal(1.0),NumVal(2.0),NumVal(3.0),NumVal(4.0),NumVal(5.0),
NumVal(6.0),NumVal(7.0),NumVal(8.0),NumVal(9.0),FeatureRef(1),to_reuse=False),to_reuse=False),SUB),
IfExpr(CompExpr(NumVal(2.0),NumVal(0.0),GT),NumVal(3.0),NumVal(4.0)),MUL)
""".strip().replace("\n", "")


def test_num_val():
    assert type(ast.NumVal(1).value) == np.float64
    assert type(ast.NumVal(1, dtype=np.float32).value) == np.float32
    assert type(ast.NumVal(1, dtype=np.float64).value) == np.float64
    assert type(ast.NumVal(1, dtype=np.int8).value) == np.int8
    assert type(ast.NumVal(1, dtype=int).value) == int
