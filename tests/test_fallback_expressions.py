from m2cgen import ast
from m2cgen.interpreters import PythonInterpreter

from tests.utils import assert_code_equal


def test_tanh_fallback_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    interpreter = PythonInterpreter()
    interpreter.tanh_function_name = NotImplemented

    expected_code = """
import math
def score(input):
    var1 = 2.0
    if (var1) > (44.0):
        var0 = 1.0
    else:
        if (var1) < (-44.0):
            var0 = -1.0
        else:
            var0 = (1.0) - ((2.0) / ((math.exp((2.0) * (var1))) + (1.0)))
    return var0
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_fallback_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    interpreter = PythonInterpreter()
    interpreter.sqrt_function_name = NotImplemented

    expected_code = """
import math
def score(input):
    return math.pow(2.0, 0.5)
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_fallback_expr():
    expr = ast.ExpExpr(ast.NumVal(2.0))

    interpreter = PythonInterpreter()
    interpreter.exponent_function_name = NotImplemented

    expected_code = """
import math
def score(input):
    return math.pow(2.718281828459045, 2.0)
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)
