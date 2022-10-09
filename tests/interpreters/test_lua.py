from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import LuaInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
function score(input)
    local ml = {}
    if 1.0 == input[1] then
        ml.var0 = 2.0
    else
        ml.var0 = 3.0
    end
    return ml.var0
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
function score(input)
    local ml = {}
    return input[1] / -2.0 * 2.0
end
"""

    interpreter = LuaInterpreter()
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
function score(input)
    local ml = {{}}
    return {op_code_line}
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
    expected_code2 = f"""
function score(input)
    local ml = {{}}
    return 1.0 {op1.value} 1.0 {op2.value} 1.0
end
"""

    interpreter = LuaInterpreter()
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
function score(input)
    local ml = {}
    if 1.0 == 1.0 then
        ml.var1 = 1.0
    else
        ml.var1 = 2.0
    end
    if ml.var1 + 2.0 >= 1.0 / 2.0 then
        ml.var0 = 1.0
    else
        ml.var0 = input[1]
    end
    return ml.var0
end
"""

    interpreter = LuaInterpreter()
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
function score(input)
    local ml = {}
    if 1.0 == 1.0 then
        ml.var1 = 1.0
    else
        ml.var1 = 2.0
    end
    if 1.0 == ml.var1 + 2.0 then
        if 1.0 == 1.0 then
            ml.var2 = 1.0
        else
            ml.var2 = 2.0
        end
        if 1.0 == ml.var2 + 2.0 then
            ml.var0 = input[3]
        else
            ml.var0 = 2.0
        end
    else
        ml.var0 = 2.0
    end
    return ml.var0
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
function score(input)
    local ml = {}
    return {3.0, 4.0}
end
"""

    interpreter = LuaInterpreter()
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
function score(input)
    local ml = {}
    if 1.0 ~= 1.0 then
        ml.var0 = {1.0, 2.0}
    else
        ml.var0 = {3.0, 4.0}
    end
    return ml.var0
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
function score(input)
    local ml = {}
    return add_vectors({1.0, 2.0}, {3.0, 4.0})
end
function add_vectors(v1, v2)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] + v2[i]
    end
    return result
end
function mul_vector_number(v1, num)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] * num
    end
    return result
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
function score(input)
    local ml = {}
    return mul_vector_number({1.0, 2.0}, 1.0)
end
function add_vectors(v1, v2)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] + v2[i]
    end
    return result
end
function mul_vector_number(v1, num)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] * num
    end
    return result
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.abs(-1.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.exp(1.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
function score(input)
    local ml = {}
    return 2.0 ^ 3.0
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.sqrt(2.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.tanh(2.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.log(2.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return log1p(2.0)
end
function log1p(x)
    if x == 0.0 then
        return 0.0
    end
    if x == -1.0 then
        return -inf
    end
    if x < -1.0 then
        return nan
    end
    local x_abs = math.abs(x)
    if x_abs < 0.5 * 4.94065645841247E-324 then
        return x
    end
    if (x > 0.0 and x < 1e-8) or (x > -1e-9 and x < 0.0) then
        return x * (1.0 - x * 0.5)
    end
    if x_abs < 0.375 then
        local coeffs = {
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
            -0.10324619158271569595141333961932e-15}
        return x * (1.0 - x * chebyshev_broucke(x / 0.375, coeffs))
    end
    return math.log(1.0 + x)
end

local function chebyshev_broucke(x, coeffs)
    local b0 = 0.0
    local b1 = 0.0
    local b2 = 0.0
    local x2 = x * 2
    for i = #coeffs - 1, 0, -1 do
        b2 = b1
        b1 = b0
        b0 = x2 * b1 - b2 + coeffs[i]
    end
    return (b0 - b2) * 0.5
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return math.atan(2.0)
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
function score(input)
    local ml = {}
    return softmax({2.0, 3.0})
end
function softmax(x)
    local size = #x
    local result = {}
    local max = x[1]
    for _, v in pairs(x) do
        if v > max then
            max = v
        end
    end
    local sum = 0.0
    for i = 1, size do
        result[i] = math.exp(x[i] - max)
        sum = sum + result[i]
    end
    for i = 1, size do
        result[i] = result[i] / sum
    end
    return result
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
function score(input)
    local ml = {}
    return sigmoid(2.0)
end
function sigmoid(x)
    if x < 0.0 then
        local z = math.exp(x)
        return z / (1.0 + z)
    end
    return 1.0 / (1.0 + math.exp(-x))
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
function score(input)
    local ml = {}
    ml.var0 = math.exp(1.0)
    return ml.var0 / ml.var0
end
"""

    interpreter = LuaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = LuaInterpreter()

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
