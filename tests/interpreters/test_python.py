from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import PythonInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
def score(input):
    if 1.0 == input[0]:
        var0 = 2.0
    else:
        var0 = 3.0
    return var0
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
def score(input):
    return input[0] / -2.0 * 2.0
"""

    interpreter = PythonInterpreter()
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
def score(input):
    return {op_code_line}
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
def score(input):
    return 1.0 {op1.value} 1.0 {op2.value} 1.0
"""

    interpreter = PythonInterpreter()
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
def score(input):
    if 1.0 == 1.0:
        var1 = 1.0
    else:
        var1 = 2.0
    if var1 + 2.0 >= 1.0 / 2.0:
        var0 = 1.0
    else:
        var0 = input[0]
    return var0
"""

    interpreter = PythonInterpreter()
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
def score(input):
    if 1.0 == 1.0:
        var1 = 1.0
    else:
        var1 = 2.0
    if 1.0 == var1 + 2.0:
        if 1.0 == 1.0:
            var2 = 1.0
        else:
            var2 = 2.0
        if 1.0 == var2 + 2.0:
            var0 = input[2]
        else:
            var0 = 2.0
    else:
        var0 = 2.0
    return var0
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
def score(input):
    return [3.0, 4.0]
"""

    interpreter = PythonInterpreter()
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
def score(input):
    if 1.0 != 1.0:
        var0 = [1.0, 2.0]
    else:
        var0 = [3.0, 4.0]
    return var0
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
def add_vectors(v1, v2):
    return [sum(i) for i in zip(v1, v2)]
def mul_vector_number(v1, num):
    return [i * num for i in v1]
def score(input):
    return add_vectors([1.0, 2.0], [3.0, 4.0])
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
def add_vectors(v1, v2):
    return [sum(i) for i in zip(v1, v2)]
def mul_vector_number(v1, num):
    return [i * num for i in v1]
def score(input):
    return mul_vector_number([1.0, 2.0], 1.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomPythonInterpreter(PythonInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    expected_code = """
def score(input):
    var0 = 1.0 + 1.0 + 1.0
    return 1.0 + 1.0 + var0
"""

    interpreter = CustomPythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_with_reused_bin_expr():
    reused_expr = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(1), ast.BinNumOpType.ADD, to_reuse=True)
    expr = ast.BinNumExpr(ast.NumVal(1), reused_expr, ast.BinNumOpType.ADD)
    expr = ast.BinNumExpr(expr, expr, ast.BinNumOpType.ADD)

    expected_code = """
def score(input):
    var0 = 1.0 + 1.0
    var1 = var0
    return 1.0 + var1 + 1.0 + var0
"""

    interpreter = CustomPythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
def score(input):
    if 1.0 == 1.0:
        var0 = 1.0
    else:
        if 1.0 == 1.0:
            var0 = 1.0
        else:
            if 1.0 == 1.0:
                var0 = 1.0
            else:
                if 1.0 == 1.0:
                    var0 = 1.0
                else:
                    var0 = 1.0
    return var0
"""

    interpreter = CustomPythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_not_reaching_threshold():
    expr = ast.NumVal(1)
    for _ in range(4):
        inner = ast.NumVal(1)
        for __ in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)
        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
def score(input):
    if 1.0 + 1.0 + 1.0 == 1.0:
        var0 = 1.0
    else:
        if 1.0 + 1.0 + 1.0 == 1.0:
            var0 = 1.0
        else:
            if 1.0 + 1.0 + 1.0 == 1.0:
                var0 = 1.0
            else:
                if 1.0 + 1.0 + 1.0 == 1.0:
                    var0 = 1.0
                else:
                    var0 = 1.0
    return var0
"""

    interpreter = CustomPythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_exceeding_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for _ in range(4):
            inner = ast.BinNumExpr(ast.NumVal(i), inner, ast.BinNumOpType.ADD)
        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
def score(input):
    var1 = 3.0 + 3.0 + 1.0
    if 3.0 + 3.0 + var1 == 1.0:
        var0 = 1.0
    else:
        var2 = 2.0 + 2.0 + 1.0
        if 2.0 + 2.0 + var2 == 1.0:
            var0 = 1.0
        else:
            var3 = 1.0 + 1.0 + 1.0
            if 1.0 + 1.0 + var3 == 1.0:
                var0 = 1.0
            else:
                var4 = 0.0 + 0.0 + 1.0
                if 0.0 + 0.0 + var4 == 1.0:
                    var0 = 1.0
                else:
                    var0 = 1.0
    return var0
"""

    interpreter = CustomPythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_expression():
    expr = ast.NumVal(1)
    for _ in range(120):
        expr = ast.BinNumExpr(expr, ast.NumVal(1), ast.BinNumOpType.ADD)

    interpreter = PythonInterpreter()

    result_code = interpreter.interpret(expr)
    result_code += """
result = score(None)
"""

    scope = {}
    exec(result_code, scope)

    assert scope["result"] == 121


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
def score(input):
    return abs(-1.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
import math
def score(input):
    return math.exp(1.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
import math
def score(input):
    return math.pow(2.0, 3.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
import math
def score(input):
    return math.sqrt(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
import math
def score(input):
    return math.tanh(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
import math
def score(input):
    return math.log(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
import math
def score(input):
    return math.log1p(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
import math
def score(input):
    return math.atan(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
import math
def softmax(x):
    m = max(x)
    exps = [math.exp(i - m) for i in x]
    s = sum(exps)
    for idx, _ in enumerate(exps):
        exps[idx] /= s
    return exps
def score(input):
    return softmax([2.0, 3.0])
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
import math
def sigmoid(x):
    if x < 0.0:
        z = math.exp(x)
        return z / (1.0 + z)
    return 1.0 / (1.0 + math.exp(-x))
def score(input):
    return sigmoid(2.0)
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
import math
def score(input):
    var0 = math.exp(1.0)
    return var0 / var0
"""

    interpreter = PythonInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = PythonInterpreter()

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
