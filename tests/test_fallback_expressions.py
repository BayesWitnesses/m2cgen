from m2cgen import ast
from m2cgen.interpreters import CInterpreter, PythonInterpreter

from tests.utils import assert_code_equal


def test_abs_fallback_expr():
    expr = ast.AbsExpr(ast.NumVal(-2.0))

    interpreter = CInterpreter()
    interpreter.abs_function_name = NotImplemented

    expected_code = """
#include <math.h>
double score(double * input) {
    double var0;
    double var1;
    var1 = -2.0;
    if ((var1) < (0.0)) {
        var0 = (0.0) - (var1);
    } else {
        var0 = var1;
    }
    return var0;
}
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)


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


def test_log1p_fallback_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    interpreter = PythonInterpreter()
    interpreter.log1p_function_name = NotImplemented

    expected_code = """
import math
def score(input):
    var1 = 2.0
    var2 = (1.0) + (var1)
    var3 = (var2) - (1.0)
    if (var3) == (0.0):
        var0 = var1
    else:
        var0 = ((var1) * (math.log(var2))) / (var3)
    return var0
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)
