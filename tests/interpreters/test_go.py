from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import GoInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
func score(input []float64) float64 {
    var var0 float64
    if 1.0 == input[0] {
        var0 = 2.0
    } else {
        var0 = 3.0
    }
    return var0
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
func score(input []float64) float64 {
    return input[0] / -2.0 * 2.0
}
"""

    interpreter = GoInterpreter()
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
func score(input []float64) float64 {{
    return {op_code_line}
}}
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
func score(input []float64) float64 {{
    return 1.0 {op1.value} 1.0 {op2.value} 1.0
}}
"""

    interpreter = GoInterpreter()
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
func score(input []float64) float64 {
    var var0 float64
    var var1 float64
    if 1.0 == 1.0 {
        var1 = 1.0
    } else {
        var1 = 2.0
    }
    if var1 + 2.0 >= 1.0 / 2.0 {
        var0 = 1.0
    } else {
        var0 = input[0]
    }
    return var0
}
"""

    interpreter = GoInterpreter()
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
func score(input []float64) float64 {
    var var0 float64
    var var1 float64
    if 1.0 == 1.0 {
        var1 = 1.0
    } else {
        var1 = 2.0
    }
    if 1.0 == var1 + 2.0 {
        var var2 float64
        if 1.0 == 1.0 {
            var2 = 1.0
        } else {
            var2 = 2.0
        }
        if 1.0 == var2 + 2.0 {
            var0 = input[2]
        } else {
            var0 = 2.0
        }
    } else {
        var0 = 2.0
    }
    return var0
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
func score(input []float64) []float64 {
    return []float64{3.0, 4.0}
}
"""

    interpreter = GoInterpreter()
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
func score(input []float64) []float64 {
    var var0 []float64
    if 1.0 != 1.0 {
        var0 = []float64{1.0, 2.0}
    } else {
        var0 = []float64{3.0, 4.0}
    }
    return var0
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
func score(input []float64) []float64 {
    return addVectors([]float64{1.0, 2.0}, []float64{3.0, 4.0})
}
func addVectors(v1, v2 []float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] + v2[i]
    }
    return result
}
func mulVectorNumber(v1 []float64, num float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] * num
    }
    return result
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
func score(input []float64) []float64 {
    return mulVectorNumber([]float64{1.0, 2.0}, 1.0)
}
func addVectors(v1, v2 []float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] + v2[i]
    }
    return result
}
func mulVectorNumber(v1 []float64, num float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] * num
    }
    return result
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Abs(-1.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Exp(1.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Pow(2.0, 3.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Sqrt(2.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Tanh(2.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Log(2.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Log1p(2.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return math.Atan(2.0)
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
import "math"
func score(input []float64) []float64 {
    return softmax([]float64{2.0, 3.0})
}
func softmax(x []float64) []float64 {
    size := len(x)
    result := make([]float64, size)
    max := x[0]
    for _, v := range x {
        if (v > max) {
            max = v
        }
    }
    sum := 0.0
    for i := 0; i < size; i++ {
        result[i] = math.Exp(x[i] - max)
        sum += result[i]
    }
    for i := 0; i < size; i++ {
        result[i] /= sum
    }
    return result
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
import "math"
func score(input []float64) float64 {
    return sigmoid(2.0)
}
func sigmoid(x float64) float64 {
    if (x < 0.0) {
        z := math.Exp(x)
        return z / (1.0 + z)
    }
    return 1.0 / (1.0 + math.Exp(-x))
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
import "math"
func score(input []float64) float64 {
    var var0 float64
    var0 = math.Exp(1.0)
    return var0 / var0
}
"""

    interpreter = GoInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = GoInterpreter()

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
