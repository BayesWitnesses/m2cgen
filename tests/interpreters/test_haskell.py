from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import HaskellInterpreter

from tests.utils import assert_code_equal


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
            if 1.0 == input !! 0 then
                2.0
            else
                3.0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
    input !! 0 / (-2.0) * 2.0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


@pytest.mark.parametrize("op1, op2", [
    *product((ast.BinNumOpType.ADD, ast.BinNumOpType.SUB), repeat=2),
    *product((ast.BinNumOpType.MUL, ast.BinNumOpType.DIV), repeat=2)
])
def test_associativity_in_bin_num_expr(op1, op2):
    expr1 = ast.BinNumExpr(
        left=ast.NumVal(1.0),
        right=ast.BinNumExpr(
            left=ast.NumVal(1.0),
            right=ast.NumVal(1.0),
            op=op2
        ),
        op=op1
    )
    if op1 in {ast.BinNumOpType.ADD, ast.BinNumOpType.MUL}:
        op_code_line = f"1.0 {op1.value} 1.0 {op2.value} 1.0"
    else:
        op_code_line = f"1.0 {op1.value} (1.0 {op2.value} 1.0)"
    expected_code1 = f"""
module Model where
score :: [Double] -> Double
score input =
    {op_code_line}
"""

    expr2 = ast.BinNumExpr(
        left=ast.BinNumExpr(
            left=ast.NumVal(1.0),
            right=ast.NumVal(1.0),
            op=op1
        ),
        right=ast.NumVal(1.0),
        op=op2
    )
    expected_code2 = f"""
module Model where
score :: [Double] -> Double
score input =
    1.0 {op1.value} 1.0 {op2.value} 1.0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr1), expected_code1)
    assert_code_equal(interpreter.interpret(expr2), expected_code2)


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
            if 1.0 == 1.0 then
                1.0
            else
                2.0
        func1 =
            if func0 + 2.0 >= 1.0 / 2.0 then
                1.0
            else
                input !! 0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
            if 1.0 == 1.0 then
                1.0
            else
                2.0
        func1 =
            if 1.0 == func0 + 2.0 then
                if 1.0 == func0 + 2.0 then
                    input !! 2
                else
                    2.0
            else
                2.0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
module Model where
score :: [Double] -> [Double]
score input =
    [3.0, 4.0]
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.IfExpr(
        ast.CompExpr(
            ast.NumVal(1),
            ast.NumVal(1),
            ast.CompOpType.NOT_EQ),
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]))

    expected_code = """
module Model where
score :: [Double] -> [Double]
score input =
    func0
    where
        func0 =
            if 1.0 /= 1.0 then
                [1.0, 2.0]
            else
                [3.0, 4.0]
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
module Model where
score :: [Double] -> [Double]
score input =
    addVectors ([1.0, 2.0]) ([3.0, 4.0])
addVectors :: [Double] -> [Double] -> [Double]
addVectors v1 v2 = zipWith (+) v1 v2
mulVectorNumber :: [Double] -> Double -> [Double]
mulVectorNumber v1 num = [i * num | i <- v1]
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
module Model where
score :: [Double] -> [Double]
score input =
    mulVectorNumber ([1.0, 2.0]) (1.0)
addVectors :: [Double] -> [Double] -> [Double]
addVectors v1 v2 = zipWith (+) v1 v2
mulVectorNumber :: [Double] -> Double -> [Double]
mulVectorNumber v1 num = [i * num | i <- v1]
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    abs ((-1.0))
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    exp (1.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    2.0 ** 3.0
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    sqrt (2.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    tanh (2.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    log (2.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    log1p (2.0)
log1p :: Double -> Double
log1p x
    | x == 0               = 0
    | x == -1              = -1 / 0
    | x < -1               = 0 / 0
    | x' < m_epsilon * 0.5 = x
    | (x > 0 && x < 1e-8) || (x > -1e-9 && x < 0)
                           = x * (1 - x * 0.5)
    | x' < 0.375           = x * (1 - x * chebyshevBroucke (x / 0.375) coeffs)
    | otherwise            = log (1 + x)
  where
    m_epsilon = encodeFloat (signif + 1) expo - 1.0
        where (signif, expo) = decodeFloat (1.0::Double)
    x' = abs x
    coeffs = [
         0.10378693562743769800686267719098e+1,
        -0.13364301504908918098766041553133e+0,
         0.19408249135520563357926199374750e-1,
        -0.30107551127535777690376537776592e-2,
         0.48694614797154850090456366509137e-3,
        -0.81054881893175356066809943008622e-4,
         0.13778847799559524782938251496059e-4,
        -0.23802210894358970251369992914935e-5,
         0.41640416213865183476391859901989e-6,
        -0.73595828378075994984266837031998e-7,
         0.13117611876241674949152294345011e-7,
        -0.23546709317742425136696092330175e-8,
         0.42522773276034997775638052962567e-9,
        -0.77190894134840796826108107493300e-10,
         0.14075746481359069909215356472191e-10,
        -0.25769072058024680627537078627584e-11,
         0.47342406666294421849154395005938e-12,
        -0.87249012674742641745301263292675e-13,
         0.16124614902740551465739833119115e-13,
        -0.29875652015665773006710792416815e-14,
         0.55480701209082887983041321697279e-15,
        -0.10324619158271569595141333961932e-15]
    chebyshevBroucke i = fini . foldr step (0, 0, 0)
        where
            step k (b0, b1, _) = ((k + i * 2 * b0 - b1), b0, b1)
            fini (b0, _, b2) = (b0 - b2) * 0.5
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    atan (2.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = r"""
module Model where
score :: [Double] -> [Double]
score input =
    softmax ([2.0, 3.0])
softmax :: [Double] -> [Double]
softmax x =
    let
        m = maximum x
        exps = map (\i -> exp (i - m)) x
        sumExps = sum exps
    in map (\i -> i / sumExps) exps
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = r"""
module Model where
score :: [Double] -> Double
score input =
    sigmoid (2.0)
sigmoid :: Double -> Double
sigmoid x
    | x < 0.0 = z / (1.0 + z)
    | otherwise = 1.0 / (1.0 + exp (-x))
  where
    z = exp x
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
module Model where
score :: [Double] -> Double
score input =
    func0 / func0
    where
        func0 =
            exp (1.0)
"""

    interpreter = HaskellInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = HaskellInterpreter()

    expr = ast.Expr()
    with pytest.raises(NotImplementedError, match="No handler found for 'Expr'"):
        interpreter.interpret(expr)

    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.ADD)
    with pytest.raises(NotImplementedError, match="Op 'ADD' is unsupported"):
        interpreter.interpret(expr)

    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.MUL)
    with pytest.raises(NotImplementedError, match="Op 'MUL' is unsupported"):
        interpreter.interpret(expr)
