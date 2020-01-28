from m2cgen import ast
from m2cgen.interpreters import PowershellInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if ((1) -eq ($InputVector[0])) {
        $var0 = 2
    } else {
        $var0 = 3
    }
    return $var0
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
function Score([double[]] $InputVector) {
    return (($InputVector[0]) / (-2)) * (2)
}
"""

    interpreter = PowershellInterpreter()
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
function Score([double[]] $InputVector) {
    [double]$var0 = 0
    [double]$var1 = 0
    if ((1) -eq (1)) {
        $var1 = 1
    } else {
        $var1 = 2
    }
    if ((($var1) + (2)) -ge ((1) / (2))) {
        $var0 = 1
    } else {
        $var0 = $InputVector[0]
    }
    return $var0
}
"""

    interpreter = PowershellInterpreter()
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
function Score([double[]] $InputVector) {
    [double]$var0 = 0
    [double]$var1 = 0
    if ((1) -eq (1)) {
        $var1 = 1
    } else {
        $var1 = 2
    }
    if ((1) -eq (($var1) + (2))) {
        [double]$var2 = 0
        if ((1) -eq (1)) {
            $var2 = 1
        } else {
            $var2 = 2
        }
        if ((1) -eq (($var2) + (2))) {
            $var0 = $InputVector[2]
        } else {
            $var0 = 2
        }
    } else {
        $var0 = 2
    }
    return $var0
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
function Score([double[]] $InputVector) {
    return @($(3), $(4))
}
"""

    interpreter = PowershellInterpreter()
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
function Score([double[]] $InputVector) {
    [double[]]$var0 = @(0)
    if ((1) -eq (1)) {
        $var0 = @($(1), $(2))
    } else {
        $var0 = @($(3), $(4))
    }
    return $var0
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
function Add-Vectors([double[]] $v1, [double[]] $v2) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] + $v2[$i]
    }
    return $result
}
function Mul-Vector-Number([double[]] $v1, [double] $num) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] * $num
    }
    return $result
}
function Div-Vector-Number([double[]] $v1, [double] $num) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] / $num
    }
    return $result
}
function Score([double[]] $InputVector) {
    return Add-Vectors $(@($(1), $(2))) $(@($(3), $(4)))
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
function Add-Vectors([double[]] $v1, [double[]] $v2) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] + $v2[$i]
    }
    return $result
}
function Mul-Vector-Number([double[]] $v1, [double] $num) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] * $num
    }
    return $result
}
function Div-Vector-Number([double[]] $v1, [double] $num) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] / $num
    }
    return $result
}
function Score([double[]] $InputVector) {
    return Mul-Vector-Number $(@($(1), $(2))) $(1)
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
function Score([double[]] $InputVector) {
    return [math]::Exp(1.0)
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
function Score([double[]] $InputVector) {
    return [math]::Pow(2.0, 3.0)
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
function Score([double[]] $InputVector) {
    return [math]::Tanh(2.0)
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
function Score([double[]] $InputVector) {
    [double]$var0 = 0
    $var0 = [math]::Exp(1.0)
    return ($var0) / ($var0)
}
"""

    interpreter = PowershellInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
