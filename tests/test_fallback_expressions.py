import pytest

from m2cgen import ast
from m2cgen.interpreters import CInterpreter, PythonInterpreter

from tests.utils import assert_code_equal


def test_required_funs_without_fallbacks():
    expr = ast.LogExpr(
        ast.PowExpr(
            ast.NumVal(1.0), ast.NumVal(-2.0)))

    interpreter = PythonInterpreter()

    interpreter.power_function_name = NotImplemented
    with pytest.raises(NotImplementedError, match="Power function is not provided"):
        interpreter.interpret(expr)

    interpreter.logarithm_function_name = NotImplemented
    with pytest.raises(NotImplementedError, match="Logarithm function is not provided"):
        interpreter.interpret(expr)


def test_abs_fallback_expr():
    expr = ast.AbsExpr(ast.NumVal(-2.0))

    interpreter = CInterpreter()
    interpreter.abs_function_name = NotImplemented

    expected_code = """
double score(double * input) {
    double var0;
    double var1;
    var1 = -2.0;
    if (var1 < 0.0) {
        var0 = 0.0 - var1;
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
    if var1 > 44.0:
        var0 = 1.0
    else:
        if var1 < -44.0:
            var0 = -1.0
        else:
            var0 = 1.0 - 2.0 / (math.exp(2.0 * var1) + 1.0)
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
    var2 = 1.0 + var1
    var3 = var2 - 1.0
    if var3 == 0.0:
        var0 = var1
    else:
        var0 = var1 * math.log(var2) / var3
    return var0
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_fallback_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    interpreter = PythonInterpreter()
    interpreter.atan_function_name = NotImplemented

    expected_code = """
 def score(input):
    var1 = 2.0
    var2 = abs(var1)
    if var2 > 2.414213562373095:
        var0 = 1.0 / var2
    else:
        if var2 > 0.66:
            var0 = (var2 - 1.0) / (var2 + 1.0)
        else:
            var0 = var2
    var3 = var0
    var4 = var3 * var3
    if var2 > 2.414213562373095:
        var5 = -1.0
    else:
        var5 = 1.0
    if var2 <= 0.66:
        var6 = 0.0
    else:
        if var2 > 2.414213562373095:
            var6 = 1.5707963267948968
        else:
            var6 = 0.7853981633974484
    if var1 < 0.0:
        var7 = -1.0
    else:
        var7 = 1.0
    return ((var3 * var4 * (var4 * (var4 * (var4 * (var4 * -0.8750608600031904 - 16.157537187333652) - 75.00855792314705) - 122.88666844901361) - 64.85021904942025) / (194.5506571482614 + var4 * (485.3903996359137 + var4 * (432.88106049129027 + var4 * (165.02700983169885 + var4 * (24.858464901423062 + var4))))) + var3) * var5 + var6) * var7
"""  # noqa: E501

    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_fallback_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    class InterpreterWithoutSoftmax(PythonInterpreter):
        softmax_function_name = NotImplemented

        def interpret_softmax_expr(self, expr, **kwargs):
            return super(PythonInterpreter, self).interpret_softmax_expr(
                expr, **kwargs)

    interpreter = InterpreterWithoutSoftmax()

    expected_code = """
import math
def score(input):
    var0 = math.exp(2.0)
    var1 = math.exp(3.0)
    var2 = (var0 + var1)
    return [var0 / var2, var1 / var2]
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_fallback_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    class InterpreterWithoutSigmoid(PythonInterpreter):
        sigmoid_function_name = NotImplemented

        def interpret_sigmoid_expr(self, expr, **kwargs):
            return super(PythonInterpreter, self).interpret_sigmoid_expr(
                expr, **kwargs)

    interpreter = InterpreterWithoutSigmoid()

    expected_code = """
import math
def score(input):
    return 1.0 / (1.0 + math.exp(0.0 - 2.0))
"""

    assert_code_equal(interpreter.interpret(expr), expected_code)
