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

    assert ast.count_exprs(ast.SubroutineExpr(ast.NumVal(1))) == 1


def test_count_exprs_exclude_list():
    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinExpr, ast.NumVal}
    ) == 0

    assert ast.count_exprs(
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        exclude_list={ast.BinNumExpr}
    ) == 2
