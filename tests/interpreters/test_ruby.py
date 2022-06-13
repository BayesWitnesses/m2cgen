from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import RubyInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
def score(input)
    if 1.0 == input[0]
        var0 = 2.0
    else
        var0 = 3.0
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
def score(input)
    (input[0]).fdiv(-2.0) * 2.0
end
"""

    interpreter = RubyInterpreter()
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
    if op2 == ast.BinNumOpType.DIV:
        op_code_line = "(1.0).fdiv(1.0)"
    else:
        op_code_line = f"1.0 {op2.value} 1.0"
    if op1 not in {ast.BinNumOpType.ADD, ast.BinNumOpType.MUL, ast.BinNumOpType.DIV}:
        op_code_line = f"({op_code_line})"
    if op1 == ast.BinNumOpType.DIV:
        op_code_line = f"(1.0).fdiv({op_code_line})"
    else:
        op_code_line = f"1.0 {op1.value} {op_code_line}"
    expected_code1 = f"""
def score(input)
    {op_code_line}
end
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
    if op1 == ast.BinNumOpType.DIV:
        op_code_line = "(1.0).fdiv(1.0)"
    else:
        op_code_line = f"1.0 {op1.value} 1.0"
    if op2 == ast.BinNumOpType.DIV:
        op_code_line = f"({op_code_line}).fdiv(1.0)"
    else:
        op_code_line = f"{op_code_line} {op2.value} 1.0"
    expected_code2 = f"""
def score(input)
    {op_code_line}
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if 1.0 == 1.0
        var1 = 1.0
    else
        var1 = 2.0
    end
    if var1 + 2.0 >= (1.0).fdiv(2.0)
        var0 = 1.0
    else
        var0 = input[0]
    end
    var0
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if 1.0 == 1.0
        var1 = 1.0
    else
        var1 = 2.0
    end
    if 1.0 == var1 + 2.0
        if 1.0 == 1.0
            var2 = 1.0
        else
            var2 = 2.0
        end
        if 1.0 == var2 + 2.0
            var0 = input[2]
        else
            var0 = 2.0
        end
    else
        var0 = 2.0
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
def score(input)
    [3.0, 4.0]
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if 1.0 != 1.0
        var0 = [1.0, 2.0]
    else
        var0 = [3.0, 4.0]
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
def score(input)
    add_vectors([1.0, 2.0], [3.0, 4.0])
end
def add_vectors(v1, v2)
    v1.zip(v2).map { |x, y| x + y }
end
def mul_vector_number(v1, num)
    v1.map { |i| i * num }
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
def score(input)
    mul_vector_number([1.0, 2.0], 1.0)
end
def add_vectors(v1, v2)
    v1.zip(v2).map { |x, y| x + y }
end
def mul_vector_number(v1, num)
    v1.map { |i| i * num }
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
def score(input)
    (-1.0).abs()
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
def score(input)
    Math.exp(1.0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
def score(input)
    2.0 ** 3.0
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.sqrt(2.0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.tanh(2.0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.log(2.0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    log1p(2.0)
end
def log1p(x)
    if x == 0.0
        return 0.0
    end
    if x == -1.0
        return -Float::INFINITY
    end
    if x < -1.0
        return Float::NAN
    end
    x_abs = x.abs
    if x_abs < 0.5 * Float::EPSILON
        return x
    end
    if (x > 0.0 && x < 1e-8) || (x > -1e-9 && x < 0.0)
        return x * (1.0 - x * 0.5)
    end
    if x_abs < 0.375
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
        return x * (1.0 - x * chebyshev_broucke(x / 0.375, coeffs))
    end
    return Math.log(1.0 + x)
end
def chebyshev_broucke(x, coeffs)
    b2 = b1 = b0 = 0.0
    x2 = x * 2
    coeffs.reverse_each do |i|
        b2 = b1
        b1 = b0
        b0 = x2 * b1 - b2 + i
    end
    (b0 - b2) * 0.5
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.atan(2.0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
def score(input)
    softmax([2.0, 3.0])
end
def softmax(x)
    m = x.max
    exps = []
    s = 0.0
    x.each_with_index do |v, i|
        exps[i] = Math.exp(v - m)
        s += exps[i]
    end
    exps.map { |i| i / s }
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    sigmoid(2.0)
end
def sigmoid(x)
    if x < 0.0
        z = Math.exp(x)
        return z / (1.0 + z)
    end
    1.0 / (1.0 + Math.exp(-x))
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
def score(input)
    var0 = Math.exp(1.0)
    (var0).fdiv(var0)
end
"""

    interpreter = RubyInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = RubyInterpreter()

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
