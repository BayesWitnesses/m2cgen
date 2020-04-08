from m2cgen import ast
from m2cgen.interpreters import HaskellInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    func0
    where
        func0 =
            if ((1) == ((input) !! (0)))
                then
                    2
                else
                    3
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    (((input) !! (0)) / (-2)) * (2)
"""

    interpreter = HaskellInterpreter()
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
module Model where
score :: [Double] -> Double
score input =
    func1
    where
        func0 =
            if ((1) == (1))
                then
                    1
                else
                    2
        func1 =
            if (((func0) + (2)) >= ((1) / (2)))
                then
                    1
                else
                    (input) !! (0)
"""

    interpreter = HaskellInterpreter()
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
module Model where
score :: [Double] -> Double
score input =
    func1
    where
        func0 =
            if ((1) == (1))
                then
                    1
                else
                    2
        func1 =
            if ((1) == ((func0) + (2)))
                then
                    if ((1) == ((func0) + (2)))
                        then
                            (input) !! (2)
                        else
                            2
                else
                    2
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
module Model where
score :: [Double] -> [Double]
score input =
    [3, 4]
"""

    interpreter = HaskellInterpreter()
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
module Model where
score :: [Double] -> [Double]
score input =
    func0
    where
        func0 =
            if ((1) == (1))
                then
                    [1, 2]
                else
                    [3, 4]
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
module Model where
addVectors :: [Double] -> [Double] -> [Double]
addVectors v1 v2 = zipWith (+) v1 v2
mulVectorNumber :: [Double] -> Double -> [Double]
mulVectorNumber v1 num = [i * num | i <- v1]
score :: [Double] -> [Double]
score input =
    addVectors ([1, 2]) ([3, 4])
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
module Model where
addVectors :: [Double] -> [Double] -> [Double]
addVectors v1 v2 = zipWith (+) v1 v2
mulVectorNumber :: [Double] -> Double -> [Double]
mulVectorNumber v1 num = [i * num | i <- v1]
score :: [Double] -> [Double]
score input =
    mulVectorNumber ([1, 2]) (1)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    exp (1.0)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    (2.0) ** (3.0)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    sqrt (2.0)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    tanh (2.0)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    (func0) / (func0)
    where
        func0 =
            exp (1.0)
"""

    interpreter = HaskellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
