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
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (1) = (input_vector(0)) Then
        var0 = 2
    Else
        var0 = 3
    End If
    score = var0
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
Function score(ByRef input_vector() As Double) As Double
    score = ((input_vector(0)) / (-2)) * (2)
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
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If (1) = (1) Then
        var1 = 1
    Else
        var1 = 2
    End If
    If ((var1) + (2)) >= ((1) / (2)) Then
        var0 = 1
    Else
        var0 = input_vector(0)
    End If
    score = var0
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
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If (1) = (1) Then
        var1 = 1
    Else
        var1 = 2
    End If
    If (1) = ((var1) + (2)) Then
        Dim var2 As Double
        If (1) = (1) Then
            var2 = 1
        Else
            var2 = 2
        End If
        If (1) = ((var2) + (2)) Then
            var0 = input_vector(2)
        Else
            var0 = 2
        End If
    Else
        var0 = 2
    End If
    score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_module_name():
    expr = ast.NumVal(1)

    expected_code = """
Module Test
Function score(ByRef input_vector() As Double) As Double
    score = 1
End Function
End Module
"""

    interpreter = VisualBasicInterpreter(module_name="Test")
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 3
    var0(1) = 4
    score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0() As Double
    If (1) = (1) Then
        Dim var1(1) As Double
        var1(0) = 1
        var1(1) = 2
        var0 = var1
    Else
        Dim var2(1) As Double
        var2(0) = 3
        var2(1) = 4
        var0 = var2
    End If
    score = var0
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
Function addVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    addVectors = result
End Function
Function mulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    mulVectorNumber = result
End Function
Function score(ByRef input_vector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1
    var0(1) = 2
    Dim var1(1) As Double
    var1(0) = 3
    var1(1) = 4
    score = addVectors(var0, var1)
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
Function addVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    addVectors = result
End Function
Function mulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    mulVectorNumber = result
End Function
Function score(ByRef input_vector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1
    var0(1) = 2
    score = mulVectorNumber(var0, 1)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
Module Model
Function score(ByRef input_vector() As Double) As Double
    score = Math.Exp(1.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
Module Model
Function score(ByRef input_vector() As Double) As Double
    score = (2.0) ^ (3.0)
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
    If number > 44.0 Then  ' exp(2*x) <= 2^127
        Tanh = 1.0
        Exit Function
    End If
    If number < -44.0 Then
        Tanh = -1.0
        Exit Function
    End If
    Tanh = (Math.Exp(2 * number) - 1) / (Math.Exp(2 * number) + 1)
End Function
Function score(ByRef input_vector() As Double) As Double
    score = Tanh(2.0)
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
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    var0 = Math.Exp(1.0)
    score = (var0) / (var0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
