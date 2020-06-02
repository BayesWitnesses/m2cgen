from m2cgen import ast
from m2cgen.interpreters import VisualBasicInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If (1.0) = (inputVector(0)) Then
        var0 = 2.0
    Else
        var0 = 3.0
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = ((inputVector(0)) / (-2.0)) * (2.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If (1.0) = (1.0) Then
        var1 = 1.0
    Else
        var1 = 2.0
    End If
    If ((var1) + (2.0)) >= ((1.0) / (2.0)) Then
        var0 = 1.0
    Else
        var0 = inputVector(0)
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If (1.0) = (1.0) Then
        var1 = 1.0
    Else
        var1 = 2.0
    End If
    If (1.0) = ((var1) + (2.0)) Then
        Dim var2 As Double
        If (1.0) = (1.0) Then
            var2 = 1.0
        Else
            var2 = 2.0
        End If
        If (1.0) = ((var2) + (2.0)) Then
            var0 = inputVector(2)
        Else
            var0 = 2.0
        End If
    Else
        var0 = 2.0
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_module_name():
    expr = ast.NumVal(1)

    expected_code = """
Module Test
Function Score(ByRef inputVector() As Double) As Double
    Score = 1.0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter(module_name="Test")
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 3.0
    var0(1) = 4.0
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.IfExpr(
        ast.CompExpr(
            ast.NumVal(1),
            ast.NumVal(1),
            ast.CompOpType.EQ),
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0() As Double
    If (1.0) = (1.0) Then
        Dim var1(1) As Double
        var1(0) = 1.0
        var1(1) = 2.0
        var0 = var1
    Else
        Dim var2(1) As Double
        var2(0) = 3.0
        var2(1) = 4.0
        var0 = var2
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
Module Model
Function AddVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    AddVectors = result
End Function
Function MulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    MulVectorNumber = result
End Function
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1.0
    var0(1) = 2.0
    Dim var1(1) As Double
    var1(0) = 3.0
    var1(1) = 4.0
    Score = AddVectors(var0, var1)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
Module Model
Function AddVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    AddVectors = result
End Function
Function MulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    MulVectorNumber = result
End Function
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1.0
    var0(1) = 2.0
    Score = MulVectorNumber(var0, 1.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Math.Abs(-1.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Math.Exp(1.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = (2.0) ^ (3.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = (2.0) ^ (0.5)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Tanh(ByVal number As Double) As Double
    ' Implementation is taken from
    ' https://github.com/golang/go/blob/master/src/math/tanh.go
    Dim z As Double
    z = Math.Abs(number)
    If z > 0.440148459655565271479942397125e+2 Then
        If number < 0 Then
            Tanh = -1.0
            Exit Function
        End If
        Tanh = 1.0
        Exit Function
    End If
    If z >= 0.625 Then
        z = 1 - 2 / (Math.Exp(2 * z) + 1)
        If number < 0 Then
            z = -z
        End If
        Tanh = z
        Exit Function
    End If
    If number = 0 Then
        Tanh = 0.0
        Exit Function
    End If
    Dim s As Double
    s = number * number
    z = number + number * s _
        * ((-0.964399179425052238628e+0 * s + -0.992877231001918586564e+2) _
           * s + -0.161468768441708447952e+4) _
        / (((s + 0.112811678491632931402e+3) _
            * s + 0.223548839060100448583e+4) _
           * s + 0.484406305325125486048e+4)
    Tanh = z
End Function
Function Score(ByRef inputVector() As Double) As Double
    Score = Tanh(2.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    var0 = Math.Exp(1.0)
    Score = (var0) / (var0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
