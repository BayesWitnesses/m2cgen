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


def test_count_exprs_exclude_list():
    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinExpr, ast.NumVal}
    ) == 0

    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinNumExpr}
    ) == 2


def test_count_all_exprs_types():
    expr = ast.BinVectorNumExpr(
        ast.BinVectorExpr(
            ast.VectorVal([
                ast.ExpExpr(ast.NumVal(2)),
                ast.SqrtExpr(ast.NumVal(2)),
                ast.PowExpr(ast.NumVal(2), ast.NumVal(3)),
                ast.TanhExpr(ast.NumVal(1)),
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.FeatureRef(0),
                    ast.BinNumOpType.ADD)
            ]),
            ast.VectorVal([
                ast.NumVal(1),
                ast.NumVal(2),
                ast.NumVal(3),
                ast.NumVal(4),
                ast.FeatureRef(1)
            ]),
            ast.BinNumOpType.SUB),
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(2), ast.NumVal(0), ast.CompOpType.GT),
            ast.NumVal(3),
            ast.NumVal(4),
        ),
        ast.BinNumOpType.MUL)

    assert ast.count_exprs(expr) == 27
