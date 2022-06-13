from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import VisualBasicInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If 1.0 = inputVector(0) Then
        var0 = 2.0
    Else
        var0 = 3.0
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = inputVector(0) / -2.0 * 2.0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = {op_code_line}
End Function
End Module
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = 1.0 {op1.value} 1.0 {op2.value} 1.0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If 1.0 = 1.0 Then
        var1 = 1.0
    Else
        var1 = 2.0
    End If
    If var1 + 2.0 >= 1.0 / 2.0 Then
        var0 = 1.0
    Else
        var0 = inputVector(0)
    End If
    Score = var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
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
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    Dim var1 As Double
    If 1.0 = 1.0 Then
        var1 = 1.0
    Else
        var1 = 2.0
    End If
    If 1.0 = var1 + 2.0 Then
        Dim var2 As Double
        If 1.0 = 1.0 Then
            var2 = 1.0
        Else
            var2 = 2.0
        End If
        If 1.0 = var2 + 2.0 Then
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
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0() As Double
    If 1.0 <> 1.0 Then
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
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1.0
    var0(1) = 2.0
    Dim var1(1) As Double
    var1(0) = 3.0
    var1(1) = 4.0
    Score = AddVectors(var0, var1)
End Function
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
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 1.0
    var0(1) = 2.0
    Score = MulVectorNumber(var0, 1.0)
End Function
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
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = 2.0 ^ 3.0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = 2.0 ^ 0.5
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Tanh(2.0)
End Function
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
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Math.Log(2.0)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Log1p(2.0)
End Function
Function ChebyshevBroucke(ByVal x As Double, _
                          ByRef coeffs() As Double) As Double
    Dim b2 as Double
    Dim b1 as Double
    Dim b0 as Double
    Dim x2 as Double
    b2 = 0.0
    b1 = 0.0
    b0 = 0.0
    x2 = x * 2
    Dim i as Integer
    For i = UBound(coeffs) - 1 To 0 Step -1
        b2 = b1
        b1 = b0
        b0 = x2 * b1 - b2 + coeffs(i)
    Next i
    ChebyshevBroucke = (b0 - b2) * 0.5
End Function
Function Log1p(ByVal x As Double) As Double
    If x = 0.0 Then
        Log1p = 0.0
        Exit Function
    End If
    If x = -1.0 Then
        On Error Resume Next
        Log1p = -1.0 / 0.0
        Exit Function
    End If
    If x < -1.0 Then
        On Error Resume Next
        Log1p = 0.0 / 0.0
        Exit Function
    End If
    Dim xAbs As Double
    xAbs = Math.Abs(x)
    If xAbs < 0.5 * 4.94065645841247e-324 Then
        Log1p = x
        Exit Function
    End If
    If (x > 0.0 AND x < 1e-8) OR (x > -1e-9 AND x < 0.0) Then
        Log1p = x * (1.0 - x * 0.5)
        Exit Function
    End If
    If xAbs < 0.375 Then
        Dim coeffs(22) As Double
        coeffs(0)  =  0.10378693562743769800686267719098e+1
        coeffs(1)  = -0.13364301504908918098766041553133e+0
        coeffs(2)  =  0.19408249135520563357926199374750e-1
        coeffs(3)  = -0.30107551127535777690376537776592e-2
        coeffs(4)  =  0.48694614797154850090456366509137e-3
        coeffs(5)  = -0.81054881893175356066809943008622e-4
        coeffs(6)  =  0.13778847799559524782938251496059e-4
        coeffs(7)  = -0.23802210894358970251369992914935e-5
        coeffs(8)  =  0.41640416213865183476391859901989e-6
        coeffs(9)  = -0.73595828378075994984266837031998e-7
        coeffs(10) =  0.13117611876241674949152294345011e-7
        coeffs(11) = -0.23546709317742425136696092330175e-8
        coeffs(12) =  0.42522773276034997775638052962567e-9
        coeffs(13) = -0.77190894134840796826108107493300e-10
        coeffs(14) =  0.14075746481359069909215356472191e-10
        coeffs(15) = -0.25769072058024680627537078627584e-11
        coeffs(16) =  0.47342406666294421849154395005938e-12
        coeffs(17) = -0.87249012674742641745301263292675e-13
        coeffs(18) =  0.16124614902740551465739833119115e-13
        coeffs(19) = -0.29875652015665773006710792416815e-14
        coeffs(20) =  0.55480701209082887983041321697279e-15
        coeffs(21) = -0.10324619158271569595141333961932e-15
        Log1p = x * (1.0 - x * ChebyshevBroucke(x / 0.375, coeffs))
        Exit Function
    End If
    Log1p = Math.log(1.0 + x)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Atan(2.0)
End Function
Function Xatan(ByVal x As Double) As Double
    Dim z As Double
    z = x * x
    z = z * ((((-8.750608600031904122785e-01 * z _
                - 1.615753718733365076637e+01) * z _
               - 7.500855792314704667340e+01) * z _
              - 1.228866684490136173410e+02) * z _
             - 6.485021904942025371773e+01) _
        / (((((z + 2.485846490142306297962e+01) * z _
              + 1.650270098316988542046e+02) * z _
             + 4.328810604912902668951e+02) * z _
            + 4.853903996359136964868e+02) * z _
           + 1.945506571482613964425e+02)
    Xatan = x * z + x
End Function
Function Satan(ByVal x As Double) As Double
    Dim morebits as Double
    Dim tan3pio8 as Double
    morebits = 6.123233995736765886130e-17
    tan3pio8 = 2.41421356237309504880
    If x <= 0.66 Then
        Satan = Xatan(x)
        Exit Function
    End If
    If x > tan3pio8 Then
        Satan = 1.57079632679489661923132169163 - Xatan(1.0 / x) + morebits
        Exit Function
    End If
    Satan = 0.78539816339744830961566084581 + Xatan((x - 1) / (x + 1)) _
            + 3.061616997868382943065e-17
End Function
Function Atan(ByVal number As Double) As Double
    ' Implementation is taken from
    ' https://github.com/golang/go/blob/master/src/math/atan.go
    If number = 0.0 Then
        Atan = 0.0
        Exit Function
    End If
    If number > 0.0 Then
        Atan = Satan(number)
        Exit Function
    End If
    Atan = -Satan(-number)
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(1) As Double
    var0(0) = 2.0
    var0(1) = 3.0
    Score = Softmax(var0)
End Function
Function Softmax(ByRef x() As Double) As Double()
    Dim size As Integer
    size = UBound(x) - LBound(x)
    Dim result() As Double
    ReDim result(size)
    Dim max As Double
    max = x(LBound(x))
    Dim i As Integer
    For i = LBound(x) + 1 To UBound(x)
        If x(i) > max Then
            max = x(i)
        End If
    Next i
    Dim sum As Double
    sum = 0.0
    For i = LBound(x) To UBound(x)
        result(i) = Math.Exp(x(i) - max)
        sum = sum + result(i)
    Next i
    For i = LBound(x) To UBound(x)
        result(i) = result(i) / sum
    Next i
    Softmax = result
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score = Sigmoid(2.0)
End Function
Function Sigmoid(ByVal number As Double) As Double
    If number < 0.0 Then
        Dim z As Double
        z = Math.Exp(number)
        Sigmoid = z / (1.0 + z)
        Exit Function
    End If
    Sigmoid = 1.0 / (1.0 + Math.Exp(-number))
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    var0 = Math.Exp(1.0)
    Score = var0 / var0
End Function
End Module
"""

    interpreter = VisualBasicInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = VisualBasicInterpreter()

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
