from m2cgen import ast
from m2cgen import interpreters
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    var var0;
    if ((1) == (input[0])) {
        var0 = 2;
    } else {
        var0 = 3;
    }
    return var0;
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return ((input[0]) / (-2)) * (2);
}
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
function score(input) {
    var var0;
    var var1;
    if ((1) == (1)) {
        var1 = 1;
    } else {
        var1 = 2;
    }
    if (((var1) + (2)) >= ((1) / (2))) {
        var0 = 1;
    } else {
        var0 = input[0];
    }
    return var0;
}
"""

    interpreter = interpreters.JavascriptInterpreter()

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
function score(input) {
    var var0;
    var var1;
    if ((1) == (1)) {
        var1 = 1;
    } else {
        var1 = 2;
    }
    if ((1) == ((var1) + (2))) {
        var var2;
        if ((1) == (1)) {
            var2 = 1;
        } else {
            var2 = 2;
        }
        if ((1) == ((var2) + (2))) {
            var0 = input[2];
        } else {
            var0 = 2;
        }
    } else {
        var0 = 2;
    }
    return var0;
}
"""

    interpreter = interpreters.JavascriptInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
function score(input) {
    return [3, 4];
}
"""

    interpreter = interpreters.JavascriptInterpreter()
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
function score(input) {
    var var0;
    if ((1) == (1)) {
        var0 = [1, 2];
    } else {
        var0 = [3, 4];
    }
    return var0;
}
"""

    interpreter = interpreters.JavascriptInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return addVectors([1, 2], [3, 4]);
}
function addVectors(v1, v2) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
function mulVectorNumber(v1, num) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
function divVectorNumber(v1, num) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] / num;
    }
    return result;
}
"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return mulVectorNumber([1, 2], 1);
}
function addVectors(v1, v2) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
function mulVectorNumber(v1, num) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
function divVectorNumber(v1, num) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] / num;
    }
    return result;
}
"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return Math.exp(1.0);
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return Math.pow(2.0, 3.0);
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    return Math.tanh(2.0);
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    interpreter = interpreters.JavascriptInterpreter()

    expected_code = """
function score(input) {
    var var0;
    var0 = Math.exp(1.0);
    return (var0) / (var0);
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
