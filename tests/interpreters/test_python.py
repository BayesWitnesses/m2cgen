from m2cgen import ast
from m2cgen import interpreters
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    interpreter = interpreters.PythonInterpreter()

    expected_code = """
def  score(input):
    if (1) == (input[0]):
        var0 = 2
    else:
        var0 = 3
    return var0
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.PythonInterpreter()

    expected_code = """
def  score(input):
    return ((input[0]) / (-2)) * (2)
    """

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
def  score(input):
    if (1) == (1):
        var1 = 1
    else:
        var1 = 2
    if ((var1) + (2)) >= ((1) / (2)):
        var0 = 1
    else:
        var0 = input[0]
    return var0
    """

    interpreter = interpreters.PythonInterpreter()

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
def  score(input):
    if (1) == (1):
        var1 = 1
    else:
        var1 = 2
    if (1) == ((var1) + (2)):
        if (1) == (1):
            var2 = 1
        else:
            var2 = 2
        if (1) == ((var2) + (2)):
            var0 = input[2]
        else:
            var0 = 2
    else:
        var0 = 2
    return var0
    """

    interpreter = interpreters.PythonInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.SubroutineExpr(
        ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1),
                ast.NumVal(1),
                ast.CompOpType.EQ),
            ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
            ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])))

    expected_code = """
import numpy as np
def  score(input):
    if (1) == (1):
        var0 = np.asarray([1, 2])
    else:
        var0 = np.asarray([3, 4])
    return var0
"""

    interpreter = interpreters.PythonInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.PythonInterpreter()

    expected_code = """
import numpy as np
def  score(input):
    return (np.asarray([1, 2])) * (np.asarray([3, 4]))
"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.PythonInterpreter()

    expected_code = """
import numpy as np
def  score(input):
    return (np.asarray([1, 2])) * (1)
"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomPythonInterpreter(interpreters.PythonInterpreter):
    depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = CustomPythonInterpreter()

    expected_code = """
def  score(input):
    var0 = (1) + ((1) + (1))
    return (1) + ((1) + (var0))"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomPythonInterpreter()

    expected_code = """
def  score(input):
    if (1) == (1):
        var0 = 1
    else:
        var1 = (1) == (1)
        if var1:
            var0 = 1
        else:
            var2 = (1) == (1)
            if var2:
                var0 = 1
            else:
                var3 = (1) == (1)
                if var3:
                    var0 = 1
                else:
                    var0 = 1
    return var0"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_expression():
    expr = ast.NumVal(1)
    for i in range(120):
        expr = ast.BinNumExpr(expr, ast.NumVal(1), ast.BinNumOpType.ADD)

    interpreter = interpreters.PythonInterpreter()

    result_code = interpreter.interpret(expr)
    result_code += """
result = score(None)
"""

    scope = {}
    exec(result_code, scope)

    assert scope["result"] == 121
