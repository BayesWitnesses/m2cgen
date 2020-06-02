from m2cgen import ast
from m2cgen.interpreters import FSharpInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
let score (input : double list) =
    let func0 =
        if ((1.0) = (input.[0])) then
            2.0
        else
            3.0
    func0
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
let score (input : double list) =
    ((input.[0]) / (-2.0)) * (2.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_dependable_condition():
    left = ast.BinNumExpr(
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(1),
                         ast.NumVal(1),
                         ast.CompOpType.EQ),
            ast.NumVal(1),
            ast.NumVal(2)),
        ast.NumVal(2),
        ast.BinNumOpType.ADD)

    right = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.DIV)
    bool_test = ast.CompExpr(left, right, ast.CompOpType.GTE)

    expr = ast.IfExpr(bool_test, ast.NumVal(1), ast.FeatureRef(0))

    expected_code = """
let score (input : double list) =
    let func0 =
        if ((1.0) = (1.0)) then
            1.0
        else
            2.0
    let func1 =
        if (((func0) + (2.0)) >= ((1.0) / (2.0))) then
            1.0
        else
            input.[0]
    func1
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_nested_condition():
    left = ast.BinNumExpr(
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(1),
                         ast.NumVal(1),
                         ast.CompOpType.EQ),
            ast.NumVal(1),
            ast.NumVal(2)),
        ast.NumVal(2),
        ast.BinNumOpType.ADD)

    bool_test = ast.CompExpr(ast.NumVal(1), left, ast.CompOpType.EQ)

    expr_nested = ast.IfExpr(bool_test, ast.FeatureRef(2), ast.NumVal(2))

    expr = ast.IfExpr(bool_test, expr_nested, ast.NumVal(2))

    expected_code = """
let score (input : double list) =
    let func0 =
        if ((1.0) = (1.0)) then
            1.0
        else
            2.0
    let func1 =
        if ((1.0) = ((func0) + (2.0))) then
            if ((1.0) = ((func0) + (2.0))) then
                input.[2]
            else
                2.0
        else
            2.0
    func1
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
let score (input : double list) =
    [3.0; 4.0]
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.IfExpr(
        ast.CompExpr(
            ast.NumVal(1),
            ast.NumVal(1),
            ast.CompOpType.EQ),
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]))

    expected_code = """
let score (input : double list) =
    let func0 =
        if ((1.0) = (1.0)) then
            [1.0; 2.0]
        else
            [3.0; 4.0]
    func0
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
let private addVectors v1 v2 = List.map2 (+) v1 v2
let private mulVectorNumber v1 num = List.map (fun i -> i * num) v1
let score (input : double list) =
    addVectors ([1.0; 2.0]) ([3.0; 4.0])
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
let private addVectors v1 v2 = List.map2 (+) v1 v2
let private mulVectorNumber v1 num = List.map (fun i -> i * num) v1
let score (input : double list) =
    mulVectorNumber ([1.0; 2.0]) (1.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomFSharpInterpreter(FSharpInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = CustomFSharpInterpreter()

    expected_code = """
let score (input : double list) =
    let func0 =
        (1.0) + ((1.0) + (1.0))
    (1.0) + ((1.0) + (func0))
    """

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomFSharpInterpreter()

    expected_code = """
let score (input : double list) =
    let func0 =
        if ((1.0) = (1.0)) then
            1.0
        else
            if ((1.0) = (1.0)) then
                1.0
            else
                if ((1.0) = (1.0)) then
                    1.0
                else
                    if ((1.0) = (1.0)) then
                        1.0
                    else
                        1.0
    func0
    """

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_not_reaching_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for i in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomFSharpInterpreter()

    expected_code = """
let score (input : double list) =
    let func0 =
        if (((1.0) + ((1.0) + (1.0))) = (1.0)) then
            1.0
        else
            if (((1.0) + ((1.0) + (1.0))) = (1.0)) then
                1.0
            else
                if (((1.0) + ((1.0) + (1.0))) = (1.0)) then
                    1.0
                else
                    if (((1.0) + ((1.0) + (1.0))) = (1.0)) then
                        1.0
                    else
                        1.0
    func0
    """

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_exceeding_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for i in range(4):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomFSharpInterpreter()

    expected_code = """
let score (input : double list) =
    let func0 =
        (1.0) + ((1.0) + (1.0))
    let func1 =
        (1.0) + ((1.0) + (1.0))
    let func2 =
        (1.0) + ((1.0) + (1.0))
    let func3 =
        (1.0) + ((1.0) + (1.0))
    let func4 =
        if (((1.0) + ((1.0) + (func0))) = (1.0)) then
            1.0
        else
            if (((1.0) + ((1.0) + (func1))) = (1.0)) then
                1.0
            else
                if (((1.0) + ((1.0) + (func2))) = (1.0)) then
                    1.0
                else
                    if (((1.0) + ((1.0) + (func3))) = (1.0)) then
                        1.0
                    else
                        1.0
    func4
    """

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
let score (input : double list) =
    abs (-1.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
let score (input : double list) =
    exp (1.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
let score (input : double list) =
    (2.0) ** (3.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
let score (input : double list) =
    sqrt (2.0)

"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
let score (input : double list) =
    tanh (2.0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
let score (input : double list) =
    let func0 =
        exp (1.0)
    (func0) / (func0)
"""

    interpreter = FSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
