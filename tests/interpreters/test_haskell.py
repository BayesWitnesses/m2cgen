from m2cgen import ast
from m2cgen.interpreters import PhpInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
<?php
function score(array $input) {
    $var0 = null;
    if ((1) === ($input[0])) {
        $var0 = 2;
    } else {
        $var0 = 3;
    }
    return $var0;
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
<?php
function score(array $input) {
    return (($input[0]) / (-2)) * (2);
}
"""

    interpreter = PhpInterpreter()
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
<?php
function score(array $input) {
    $var0 = null;
    $var1 = null;
    if ((1) === (1)) {
        $var1 = 1;
    } else {
        $var1 = 2;
    }
    if ((($var1) + (2)) >= ((1) / (2))) {
        $var0 = 1;
    } else {
        $var0 = $input[0];
    }
    return $var0;
}
"""

    interpreter = PhpInterpreter()
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
<?php
function score(array $input) {
    $var0 = null;
    $var1 = null;
    if ((1) === (1)) {
        $var1 = 1;
    } else {
        $var1 = 2;
    }
    if ((1) === (($var1) + (2))) {
        $var2 = null;
        if ((1) === (1)) {
            $var2 = 1;
        } else {
            $var2 = 2;
        }
        if ((1) === (($var2) + (2))) {
            $var0 = $input[2];
        } else {
            $var0 = 2;
        }
    } else {
        $var0 = 2;
    }
    return $var0;
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
<?php
function score(array $input) {
    return array(3, 4);
}
"""

    interpreter = PhpInterpreter()
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
<?php
function score(array $input) {
    $var0 = array();
    if ((1) === (1)) {
        $var0 = array(1, 2);
    } else {
        $var0 = array(3, 4);
    }
    return $var0;
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
<?php
function addVectors(array $v1, array $v2) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] + $v2[$i];
    }
    return $result;
}
function mulVectorNumber(array $v1, $num) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] * $num;
    }
    return $result;
}
function score(array $input) {
    return addVectors(array(1, 2), array(3, 4));
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
<?php
function addVectors(array $v1, array $v2) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] + $v2[$i];
    }
    return $result;
}
function mulVectorNumber(array $v1, $num) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] * $num;
    }
    return $result;
}
function score(array $input) {
    return mulVectorNumber(array(1, 2), 1);
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
<?php
function score(array $input) {
    return exp(1.0);
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
<?php
function score(array $input) {
    return pow(2.0, 3.0);
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
<?php
function score(array $input) {
    return tanh(2.0);
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
<?php
function score(array $input) {
    $var0 = null;
    $var0 = exp(1.0);
    return ($var0) / ($var0);
}
"""

    interpreter = PhpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
